"""Exercise normal, partial and deliberately inconsistent synthetic records."""
from pathlib import Path
import json
import sys

from validate_bundle import validate_bundle, ROOT


def main():
    index = json.loads((ROOT / 'examples/index.json').read_text(encoding='utf-8'))
    failures = []
    for case in index['cases']:
        path = ROOT / 'examples' / case['path']
        data = json.loads(path.read_text(encoding='utf-8'))
        errors = validate_bundle(data)
        actual_valid = not errors
        codes = {e['code'] for e in errors}
        passed = actual_valid == case['expected_valid'] and (not case.get('expected_error') or case['expected_error'] in codes)
        print(('PASS ' if passed else 'FAIL ') + case['path'] + (' ' + ','.join(sorted(codes)) if codes else ''))
        if not passed:
            failures.append({'case': case, 'errors': errors})
    if failures:
        print(json.dumps(failures, ensure_ascii=True, indent=2))
        return 1
    print(f'{len(index["cases"])} synthetic validation cases passed; no independent Agent or domain acceptance implied.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc))
        raise SystemExit(2)
