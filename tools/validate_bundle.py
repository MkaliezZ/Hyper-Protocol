"""Validate structure and declared snapshot consistency; never execute actions."""
from pathlib import Path
import json
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parents[1]


def validate_bundle(data, schema=None):
    if Draft202012Validator is None:
        raise RuntimeError('Optional validator dependency unavailable: jsonschema. See tools/README.md.')
    if schema is None:
        schema = json.loads((ROOT / 'schemas/task-bundle.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    structural = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: str(list(e.path)))
    if structural:
        return [{'code': 'SCHEMA_INVALID', 'path': '/'.join(map(str, e.path)), 'message': e.message} for e in structural]
    errors = []

    def error(code, path, message):
        errors.append({'code': code, 'path': path, 'message': message})

    def indexed(items, id_key, versioned=False):
        found = {}
        for item in items:
            key = (item[id_key], item['version']) if versioned else item[id_key]
            if key in found:
                error('DUPLICATE_IDENTITY', id_key, 'Identity and version must identify one record.')
            found[key] = item
        return found

    assets = indexed(data['assets'], 'asset_id', True)
    policies = indexed(data['policy_packs'], 'policy_id', True)
    capabilities = indexed(data['capabilities'], 'capability_id', True)
    decisions = indexed(data['decisions'], 'decision_id')
    indexed(data['runs'], 'run_id')

    def asset_for(reference, path):
        record = assets.get((reference['asset_id'], reference['version']))
        if record is None:
            error('REFERENCE_UNRESOLVED', path, 'Asset identity/version is not in this task snapshot.')
        return record

    def walk(value, path=''):
        if isinstance(value, dict):
            if set(value) == {'asset_id', 'version'}:
                asset_for(value, path)
            for key, child in value.items():
                walk(child, path + '/' + key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, path + '/' + str(index))

    walk(data)

    def policy_for(reference, path, require_selected=True):
        record = policies.get((reference['id'], reference['version']))
        if record is None:
            error('POLICY_UNRESOLVED', path, 'Referenced policy/version is absent.')
        elif require_selected and record['adoption'] != 'selected_for_task':
            error('POLICY_NOT_SELECTED', path, 'Presence or draft status does not select a policy for execution.')
        return record

    for key, pack in policies.items():
        if pack['adoption'] == 'selected_for_task' and not pack['selection_basis']:
            error('POLICY_SELECTION_UNRECORDED', str(key), 'Selected policy must record the task selection basis.')
        indexed(pack['rules'], 'rule_id')

    for index, cap in enumerate(data['capabilities']):
        for policy_ref in cap['policy_refs']:
            policy_for(policy_ref, f'capabilities/{index}/policy_refs', require_selected=False)

    for index, decision in enumerate(data['decisions']):
        prefix = f'decisions/{index}'
        packs = [policy_for(p, prefix + '/policy_refs') for p in decision['policy_refs']]
        known_rules = {r['rule_id']: r for p in packs if p for r in p['rules']}
        checks = indexed(decision['rule_checks'], 'rule_id')
        for rule_id, check in checks.items():
            if rule_id not in known_rules:
                error('RULE_UNRESOLVED', prefix + '/rule_checks', 'Rule is absent from bound policies.')
            if check['result'] == 'not_applicable' and not check['reason']:
                error('NOT_APPLICABLE_UNEXPLAINED', prefix + '/rule_checks', 'Not applicable requires a reason.')
            if check['result'] == 'met' and known_rules.get(rule_id, {}).get('evidence_required') and not check['evidence_refs']:
                error('RULE_EVIDENCE_MISSING', prefix + '/rule_checks', 'A met evidence-dependent rule needs evidence bindings.')
        if decision['judgment_status'] == 'meets_conditions':
            if not packs or not decision['evidence_refs'] or not decision['scope']:
                error('JUDGMENT_BASIS_MISSING', prefix, 'Meets conditions requires policy, scope and evidence.')
            for rule_id, rule in known_rules.items():
                check = checks.get(rule_id)
                if rule['kind'] == 'hard_gate' and (not check or check['result'] not in {'met', 'not_applicable'}):
                    error('HARD_GATE_UNSATISFIED', prefix, 'Unmet or unknown hard gates cannot be overridden by aggregate quality.')
        if decision['judgment_status'] == 'not_applicable' and not decision['rationale']:
            error('NOT_APPLICABLE_UNEXPLAINED', prefix, 'Not applicable judgment requires rationale.')
        for dimension, review in decision['reviews'].items():
            where = prefix + '/reviews/' + dimension
            if review['status'] == 'passed' and (not review['evidence_refs'] or not review['scope']):
                error('REVIEW_EVIDENCE_MISSING', where, 'Passed needs separate scope and evidence; runtime success is insufficient.')
            if review['status'] == 'passed' and review['reviewer_kind'] == 'not_recorded':
                error('REVIEWER_UNRECORDED', where, 'Passed review must identify reviewer kind.')
            if dimension == 'human_acceptance' and review['status'] == 'passed' and review['reviewer_kind'] != 'human':
                error('HUMAN_ACCEPTANCE_MISATTRIBUTED', where, 'Agent, code or model self-review is not human acceptance.')
            if review['status'] == 'not_applicable' and not review['reason']:
                error('NOT_APPLICABLE_UNEXPLAINED', where, 'Not applicable review requires a reason.')

    for index, run in enumerate(data['runs']):
        prefix = f'runs/{index}'
        capref = run['capability_ref']
        cap = capabilities.get((capref['id'], capref['version']))
        if cap is None:
            error('CAPABILITY_UNRESOLVED', prefix, 'Capability identity/version is absent.')
        for policy_ref in run['policy_refs']:
            policy_for(policy_ref, prefix + '/policy_refs')
        if run['execution_status'] in {'running', 'succeeded'}:
            bound_policies = {(p['id'], p['version']) for p in run['policy_refs']}
            if cap and not {(p['id'], p['version']) for p in cap['policy_refs']}.issubset(bound_policies):
                error('CAPABILITY_POLICY_UNBOUND', prefix, 'Execution must bind the capability-required policy versions.')
            auth = run['authorization_snapshot']
            if auth['status'] != 'granted' or not auth['basis'] or not auth['checked_at']:
                error('AUTHORIZATION_NOT_GRANTED', prefix, 'Running/succeeded needs a recorded granted authorization snapshot.')
            if cap and cap['action'] not in auth['scope']:
                error('ACTION_OUTSIDE_AUTHORIZATION', prefix, 'Capability action is outside declared authorization scope.')
            for asset_ref in run['input_refs']:
                record = assets.get((asset_ref['asset_id'], asset_ref['version']))
                if record and record['availability'] != 'available':
                    error('ASSET_UNAVAILABLE', prefix, 'Input was not available in this run snapshot.')
            if not run['executor'] or not run['started_at']:
                error('EXECUTOR_UNRECORDED', prefix, 'Running/succeeded needs executor and start time.')
        if run['execution_status'] == 'succeeded' and (not run['runtime_evidence_refs'] or not run['ended_at']):
            error('EXECUTION_EVIDENCE_MISSING', prefix, 'Succeeded needs terminal time and execution evidence.')
        if run['execution_status'] == 'failed' and not run['failure']:
            error('FAILURE_UNEXPLAINED', prefix, 'Failed must retain its failure reason.')

    delivery = data['delivery']
    for decision_id in delivery['decision_refs']:
        if decision_id not in decisions:
            error('DECISION_UNRESOLVED', 'delivery/decision_refs', 'Referenced decision is absent.')
    for index, claim in enumerate(delivery['claims']):
        if claim['kind'] == 'fact' and not claim['evidence_refs']:
            error('FACT_EVIDENCE_MISSING', f'delivery/claims/{index}', 'Important fact claims need scoped source evidence.')
    if delivery['status'] == 'completed':
        if data['nature'] == 'template':
            error('TEMPLATE_NOT_EXECUTION', 'delivery', 'An unfilled template cannot be completed.')
        if not data['scenario']['goal'] or not delivery['scope'] or not delivery['artifact_refs']:
            error('DELIVERY_BASIS_MISSING', 'delivery', 'Completed needs a task goal, scope and actual artifact bindings.')
        if delivery['blocking_gaps']:
            error('DELIVERY_HAS_BLOCKING_GAPS', 'delivery', 'Completed delivery still lists blocking gaps.')
        relevant = [decisions[i] for i in delivery['decision_refs'] if i in decisions]
        required = data['scenario']['required_reviews']
        if required and not relevant:
            error('REQUIRED_REVIEW_MISSING', 'delivery', 'Required reviews need bound decisions.')
        for decision in relevant:
            for dimension in required:
                review = decision['reviews'][dimension]
                if review['status'] not in {'passed', 'not_applicable'}:
                    error('REQUIRED_REVIEW_PENDING', 'delivery', 'A task-required review has not passed.')
            if data['scenario']['acceptance_level'] == 'reviewed_output' and decision['judgment_status'] != 'meets_conditions':
                error('REVIEWED_OUTPUT_NOT_READY', 'delivery', 'Reviewed output needs relevant judgments to meet conditions.')
        if data['scenario']['acceptance_level'] == 'reviewed_output' and not relevant:
            error('REVIEWED_OUTPUT_NOT_READY', 'delivery', 'Reviewed output requires a bound judgment.')
    return errors


def main():
    if len(sys.argv) != 2:
        print('Usage: python tools/validate_bundle.py <task-bundle.json>')
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
        errors = validate_bundle(data)
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({'valid': False, 'check_available': False, 'error': str(exc)}, ensure_ascii=True))
        return 2
    print(json.dumps({'valid': not errors, 'scope': 'schema_and_declared_snapshot_consistency_only', 'errors': errors}, ensure_ascii=True, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
