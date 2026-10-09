#!/usr/bin/env python3
"""Validate the exact PR diff using trusted configuration; never run submissions."""
import argparse
import fnmatch
import json
from pathlib import Path
import re
import subprocess
import sys
import yaml


def git(*args):
    return subprocess.check_output(['git', *args])


def validate(base, head, config):
    failures = []
    names = git('diff', '--no-renames', '--name-only', '-z', f'{base}...{head}').decode().split('\0')
    names = [p for p in names if p]
    total = 0
    prefix = config['practical_prefix']
    low, high = config['practical_range']
    pattern = re.compile(re.escape(prefix) + r'(\d{2})/' + (r'[^/]+/' if config['require_student_dir'] else '') + r'[^/]+$')
    if not names:
        failures.append('No changed submission files.')
    for name in names:
        if any(name == p.rstrip('/') or name.startswith(p.rstrip('/') + '/') for p in config['protected_paths']):
            failures.append(f'Protected path: {name}')
            continue
        match = pattern.fullmatch(name)
        if not match or not low <= int(match[1]) <= high:
            failures.append(f'Invalid submission path or practical number: {name}')
        # Deletions still undergo path/protected-path checks, but have no blob to inspect.
        entry = git('ls-tree', '-z', head, '--', name).decode()
        if not entry:
            continue
        mode, kind, oid = entry.split('\t', 1)[0].split()
        if mode not in ('100644', '100755') or kind != 'blob':
            failures.append(f'Only regular files are allowed: {name}')
            continue
        if Path(name).suffix.lower().lstrip('.') not in config['allowed_extensions']:
            failures.append(f'Disallowed extension: {name}')
        if any(fnmatch.fnmatchcase(part, pat) for part in name.split('/') for pat in config['prohibited_patterns']):
            failures.append(f'Prohibited file/directory: {name}')
        size = int(git('cat-file', '-s', oid))
        total += size
        if size > config['max_file_size_mb'] * 1024**2:
            failures.append(f'File exceeds size limit: {name}')
    if total > config['max_total_size_mb'] * 1024**2:
        failures.append('Total submission exceeds size limit.')
    return names, failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('base')
    parser.add_argument('head')
    parser.add_argument('--config', default=str(Path(__file__).resolve().parent.parent / 'submission-config.yml'))
    args = parser.parse_args()
    # Fail closed even if parsing, git, or validation crashes.
    Path('validation_result.txt').write_text('STATUS=FAIL\n')
    try:
        config = yaml.safe_load(Path(args.config).read_text())
        names, failures = validate(args.base, args.head, config)
    except Exception as exc:
        names, failures = [], [f'Validation could not complete: {exc}']
    status = 'FAIL' if failures else 'PASS'
    Path('validation_result.txt').write_text(f'STATUS={status}\nFILES={len(names)}\nFAILURES={len(failures)}\n')
    summary = f'### Validation Summary\n\n**Status:** {status}\n**Files checked:** {len(names)}\n\n'
    summary += '\n'.join('- ' + message for message in failures) if failures else 'All configured structure, extension, prohibited-path and size checks passed.'
    Path('validation_summary.md').write_text(summary + '\n')
    print(summary)
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
