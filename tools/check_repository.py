"""Check the public protocol's routes, contracts, profiles and text hygiene."""
from pathlib import Path
import json
import re
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit('Optional check dependency unavailable: ' + str(exc))

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_FILES = [
    'README.md', 'README.zh-CN.md', 'AGENTS.md', 'CORE.md', 'BOOTSTRAP.txt', 'CHANGELOG.md',
    'COMPATIBILITY.md', 'CONTRIBUTING.md', 'LICENSE', 'LICENSE-NOTE.md',
    'protocol.yaml', 'verification.json', '.gitignore', '.gitattributes',
]
PAYLOAD_DIRS = ['docs', 'profiles', 'schemas', 'templates', 'examples', 'tools', 'reference', 'LICENSES', '.github']


def payload_files(root=ROOT):
    files = []
    for name in PAYLOAD_FILES:
        path = root / name
        if not path.is_file():
            raise ValueError('Missing public file: ' + name)
        files.append(path)
    for name in PAYLOAD_DIRS:
        directory = root / name
        if not directory.is_dir():
            raise ValueError('Missing public directory: ' + name)
        files.extend(p for p in directory.rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts and p.suffix != '.pyc')
    return sorted(set(files))


def enum_lists(value):
    if isinstance(value, dict):
        if 'enum' in value:
            yield value['enum']
        for child in value.values():
            yield from enum_lists(child)
    elif isinstance(value, list):
        for child in value:
            yield from enum_lists(child)


def check_repository():
    protocol = yaml.safe_load((ROOT / 'protocol.yaml').read_text(encoding='utf-8'))
    schema = json.loads((ROOT / 'schemas/task-bundle.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    assert protocol['english_name'] == 'Hyper Protocol'
    assert protocol['protocol_id'] == 'hyper-protocol'
    assert protocol['protocol_version'] == schema['properties']['protocol_version']['const']
    assert protocol['licenses']['documentation'] == 'CC-BY-4.0'
    assert protocol['licenses']['code_and_machine_contracts'] == 'Apache-2.0'
    enums = list(enum_lists(schema))
    for name, values in protocol['vocabulary'].items():
        assert values in enums, 'Vocabulary/schema mismatch: ' + name
    for path in [protocol['entrypoint'], protocol['semantics'], protocol['schema']]:
        assert (ROOT / path).is_file(), 'Missing protocol route: ' + path
    for route in ('always', 'write_task_record', 'migrate_v01'):
        for path in protocol['load_routes'][route]:
            assert (ROOT / path).is_file(), 'Missing load route: ' + path

    catalog = yaml.safe_load((ROOT / 'profiles/catalog.yaml').read_text(encoding='utf-8'))
    validator = Draft202012Validator({'$schema': schema['$schema'], '$defs': schema['$defs'], '$ref': '#/$defs/policy_pack'})
    ids = set()
    for row in catalog['profiles']:
        profile = yaml.safe_load((ROOT / 'profiles' / row['path']).read_text(encoding='utf-8'))
        validator.validate(profile)
        assert profile['policy_id'] == row['profile_id']
        assert profile['version'] == row['version']
        assert profile['policy_id'] not in ids, 'Duplicate profile identity'
        assert profile['status'] == 'draft', 'Do not silently promote a domain draft'
        ids.add(profile['policy_id'])
    assert len(ids) == 12

    problems = []
    old_name = re.compile(r'hyper[ _-]+dimension[ _-]+protocol', re.I)
    host_path = re.compile(r'(?i)(?<![a-z0-9])[a-z]:[\\/]|fi' + r'le://|Admin' + r'istrator|\.codex[\\/]|\.agents[\\/]')
    secret = re.compile(r'ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
    checked_links = 0
    files = payload_files()
    for file in files:
        text = file.read_text(encoding='utf-8')
        relative = file.relative_to(ROOT).as_posix()
        if '\ufffd' in text or host_path.search(text):
            problems.append('Nonportable or invalid text: ' + relative)
        if old_name.search(text):
            problems.append('Outdated protocol name: ' + relative)
        if secret.search(text):
            problems.append('Credential-like content: ' + relative)
        if ('formal_open_license_' + 'not_yet_selected') in text:
            problems.append('Outdated license state: ' + relative)
        if file.suffix == '.json':
            json.loads(text)
        if file.suffix in {'.yaml', '.yml'}:
            yaml.safe_load(text)
        if file.suffix == '.md':
            if sum(line.startswith('```') for line in text.splitlines()) % 2:
                problems.append('Unbalanced Markdown fence: ' + relative)
            for match in re.finditer(r'\[[^\]]*\]\((?:<([^>]+)>|([^)]*))\)', text):
                target = (match.group(1) or match.group(2)).split('#', 1)[0]
                if not target or target.startswith(('https:', 'http:', 'mailto:')):
                    continue
                checked_links += 1
                resolved = (file.parent / target).resolve()
                if not resolved.is_relative_to(ROOT.resolve()) or not resolved.exists():
                    problems.append('Broken or escaping local link: ' + relative + ' -> ' + target)
    if problems:
        raise ValueError('\n'.join(problems))
    return {'files': len(files), 'local_links': checked_links, 'profiles': len(ids), 'schema': 'passed', 'text_scan': 'passed'}


if __name__ == '__main__':
    try:
        print(json.dumps(check_repository(), ensure_ascii=True, indent=2))
    except (ValueError, AssertionError, OSError) as exc:
        print(str(exc))
        raise SystemExit(1)
