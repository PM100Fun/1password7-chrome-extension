#!/usr/bin/env python3
"""Check or repair an existing Chrome native host allowlist; never read a vault."""
import argparse
import hashlib
import base64
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from datetime import datetime, timezone

HOST = '2bua8c4s2c.com.agilebits.1password'
ROOT = Path(__file__).resolve().parent.parent


def extension_id(manifest):
    digest = hashlib.sha256(base64.b64decode(manifest['key'], validate=True)).hexdigest()[:32]
    return ''.join(chr(ord('a') + int(c, 16)) for c in digest)


def prepare(path, identity):
    if not re.fullmatch('[a-p]{32}', identity):
        raise ValueError('Extension ID must contain exactly 32 letters a-p.')
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('name') != HOST or data.get('type') != 'stdio':
        raise ValueError('Wrong native host name or type; no changes made.')
    executable = Path(data.get('path', ''))
    if not executable.is_absolute() or not executable.is_file():
        raise ValueError('Native host executable is missing or not an absolute path.')
    origins = data.get('allowed_origins')
    if not isinstance(origins, list) or not all(isinstance(x, str) for x in origins):
        raise ValueError('allowed_origins must be an array of strings.')
    origin = f'chrome-extension://{identity}/'
    changed = origin not in origins
    if changed:
        origins.append(origin)
    return data, changed


def configure(path, identity, apply=False):
    path = path.expanduser().resolve(strict=True)
    data, changed = prepare(path, identity)
    if not changed:
        return 'OK: extension is already allowed; nothing changed.'
    if not apply:
        return 'MISSING: extension is not allowed. Re-run with --apply to back up and repair.'
    # An exclusive backup prevents accidental replacement of previous backups.
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = path.with_name(path.name + '.backup-' + stamp)
    with backup.open('xb') as out, path.open('rb') as source:
        shutil.copyfileobj(source, out)
    shutil.copystat(path, backup)
    fd, temporary = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            json.dump(data, out, ensure_ascii=False, indent=2)
            out.write('\n')
        os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return f'UPDATED: allowlist repaired. Backup: {backup}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host-file', type=Path, default=Path.home() / 'Library/Application Support/Google/Chrome/NativeMessagingHosts' / (HOST + '.json'))
    parser.add_argument('--extension-id', default=None, help='Defaults to the ID derived from manifest.json public key')
    parser.add_argument('--apply', action='store_true', help='Write the allowlist after creating a backup; otherwise read-only')
    args = parser.parse_args()
    try:
        identity = args.extension_id or extension_id(json.loads((ROOT / 'manifest.json').read_text()))
        result = configure(args.host_file, identity, args.apply)
        print(f'Extension ID: {identity}\n{result}')
        return 1 if result.startswith('MISSING:') else 0
    except (OSError, ValueError, KeyError) as error:
        print(f'ERROR: {error}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
