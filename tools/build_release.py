"""Produce a deterministic, self-contained Agent ZIP and validate its payload."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile

import yaml

from check_repository import ROOT, check_repository, payload_files


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def run(script, root):
    result = subprocess.run([sys.executable, str(root / 'tools' / script)], cwd=root,
                            capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def main():
    checks = check_repository()
    example_output = run('check_examples.py', ROOT)
    protocol = yaml.safe_load((ROOT / 'protocol.yaml').read_text(encoding='utf-8'))
    version = protocol['release_version']
    name = 'Hyper-Protocol-' + version + '-agent'
    report = {
        'release_version': version, 'protocol_version': protocol['protocol_version'],
        'scope': 'repository_structure_and_declared_snapshot_consistency',
        'repository_checks': checks,
        'synthetic_cases': 13, 'synthetic_result': 'passed',
        'not_established': ['independent_agent_execution', 'cross_model_compatibility',
                            'real_domain_quality', 'real_world_effectiveness', 'external_current_authorization'],
    }
    (ROOT / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    payloads = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in payload_files()}
    manifest = {
        'package_id': protocol['package_id'], 'english_name': 'Hyper Protocol',
        'protocol_id': protocol['protocol_id'], 'protocol_version': protocol['protocol_version'],
        'release_version': version, 'audience': 'agent', 'status': 'draft', 'entrypoint': 'AGENTS.md',
        'initial_read_order': ['AGENTS.md', 'protocol.yaml', 'CORE.md', 'profiles/catalog.yaml'],
        'load_policy': 'then_select_only_task_relevant_files', 'licenses': protocol['licenses'],
        'files': [{'path': path, 'size_bytes': len(data), 'sha256': sha(data)} for path, data in sorted(payloads.items())],
    }
    payloads['manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    payloads['SHA256SUMS.txt'] = ('\n'.join(sha(data) + '  ' + path for path, data in sorted(payloads.items())) + '\n').encode('utf-8')
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    archive = output / (name + '.zip')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path, data in sorted(payloads.items()):
            info = zipfile.ZipInfo(name + '/' + path, date_time=(2026, 11, 9, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(archive) as zf:
        assert zf.testzip() is None
        for row in manifest['files']:
            data = zf.read(name + '/' + row['path'])
            assert len(data) == row['size_bytes'] and sha(data) == row['sha256']
        for line in payloads['SHA256SUMS.txt'].decode('utf-8').splitlines():
            checksum, path = line.split('  ', 1)
            assert sha(zf.read(name + '/' + path)) == checksum

    qa_root = (ROOT / '.qa').resolve()
    qa_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=qa_root) as temporary:
        extraction = Path(temporary).resolve()
        assert extraction.is_relative_to(qa_root)
        with zipfile.ZipFile(archive) as zf:
            for member in zf.namelist():
                assert (extraction / member).resolve().is_relative_to(extraction)
            zf.extractall(extraction)
        extracted = extraction / name
        run('check_repository.py', extracted)
        run('check_examples.py', extracted)

    digest = sha(archive.read_bytes())
    archive.with_suffix('.zip.sha256').write_text(digest + '  ' + archive.name + '\n', encoding='utf-8', newline='\n')
    print(example_output, end='')
    print(json.dumps({'archive': archive.name, 'files': len(payloads), 'sha256': digest,
                      'zip_integrity': 'passed', 'extracted_repository_and_examples': 'passed'}, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, AssertionError, OSError, RuntimeError) as exc:
        print(str(exc))
        raise SystemExit(1)
