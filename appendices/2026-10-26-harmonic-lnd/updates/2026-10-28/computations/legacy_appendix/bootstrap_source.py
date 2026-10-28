#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Historical pinned-source bootstrap; the consolidated suite uses its bundled offline snapshot instead.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Retrieve a pinned source dependency and verify every Git blob SHA-1.

This utility does not install packages or execute downloaded files.
An existing file with different bytes is never overwritten.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--from-repo', type=Path,
                    help='Copy the 11 pinned files from a local checkout instead of downloading')
args = parser.parse_args()
manifest = json.loads((ROOT / 'research' / 'source_manifest.json').read_text())
def git_hash(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

for item in manifest['files']:
    dest = ROOT / 'repo' / item['path']
    if dest.exists():
        if git_hash(dest.read_bytes()) != item['sha']:
            raise RuntimeError(f'Existing file differs: {dest}; move it before retrying.')
        print('Already verified:', item['path'])
        continue
    if args.from_repo is not None:
        data = (args.from_repo / item['path']).read_bytes()
    else:
        url = ('https://raw.githubusercontent.com/qft98romanov-hash/'
               f"abhyankar-moh-trefoil/{manifest['commit']}/{item['path']}")
        with urlopen(Request(url, headers={'User-Agent': 'Harmonic-LND-certificates'}), timeout=45) as response:
            data = response.read()
    if git_hash(data) != item['sha'] or len(data) != item['size']:
        raise RuntimeError(f"Source hash mismatch: {item['path']}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    print('Copied and verified:' if args.from_repo is not None else 'Downloaded and verified:', item['path'])
print('All source files match commit', manifest['commit'])
