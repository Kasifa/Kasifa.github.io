#!/usr/bin/env python3
"""Public-only verifier. No private checkout, credentials, or scientific execution."""
import hashlib, json, re, subprocess, sys
from pathlib import Path

# Exactly the two user-designated frozen PDFs; this is not a general PDF allowlist.
DESIGNATED_PAPER_PDFS = {
    'public/assets/papers/fixed-datum-three-direction-supply.pdf': (
        '2eb59ec64d977787c08e17a960d1b9737650ce38e8dd94074937a52cccc39ad5', 394514),
    'public/assets/papers/sparse-resupply-path-obstructions.pdf': (
        'c95d0a2bd9b80cc312dc0170f833f35f865e759de12377b230d02c74497462ca', 412415),
}

def digest(b):
    return hashlib.sha256(b).hexdigest()

def safe(path):
    p = Path(path)
    return not p.is_absolute() and '..' not in p.parts and ('\\' not in path)

def verify(root, manifest=None, tracked=False):
    root = Path(root).resolve()
    manifest = manifest or json.loads((root / 'public-file-manifest.json').read_text())
    if not (manifest['schema'] == 1 and manifest['policy'] in ['HISTORICAL_EXACT_PLUS_REVIEWED_OVERVIEWS', 'REVIEWED_SUMMARY_ONLY']):
        raise ValueError('validation failed')
    expected = {f['path']: f for f in manifest['files']}
    if not len(expected) == len(manifest['files']):
        raise ValueError('validation failed')
    if tracked:
        names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).decode().split('\x00')[:-1]
    else:
        names = [str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts and ('_site' not in p.relative_to(root).parts) and ('__pycache__' not in p.parts)]
    if not set(names) == set(expected) | {'public-file-manifest.json'}:
        raise ValueError('unapproved/missing file: ' + str(sorted(set(names) ^ (set(expected) | {'public-file-manifest.json'}))[:10]))
    for (name, f) in expected.items():
        if not (safe(name) and (not (root / name).is_symlink())):
            raise ValueError(name)
        data = (root / name).read_bytes()
        if not (digest(data) == f['sha256'] and len(data) == f['bytes']):
            raise ValueError('hash mismatch: ' + name)
        if not f['class'] in ['HISTORICAL_PUBLIC_EXCEPTION', 'REVIEWED_SITE_INFRASTRUCTURE', 'PUBLIC_PROGRESS_OVERVIEW', 'PUBLIC_PROGRESS_INDEX', 'REVIEWED_PUBLIC_SUMMARY', 'REVIEWED_DESIGNATED_PAPER_PDF']:
            raise ValueError(name)
        if manifest['policy']=='REVIEWED_SUMMARY_ONLY' and f['class']=='HISTORICAL_PUBLIC_EXCEPTION':
            raise ValueError('Historical detail is not permitted in the summary repository')
        if manifest['policy']=='REVIEWED_SUMMARY_ONLY' and name.lower().endswith('.pdf') and f['class'] != 'REVIEWED_DESIGNATED_PAPER_PDF':
            raise ValueError('PDF requires the exact designated-paper class: ' + name)
        if f['class'] == 'REVIEWED_DESIGNATED_PAPER_PDF':
            if DESIGNATED_PAPER_PDFS.get(name) != (f['sha256'], f['bytes']):
                raise ValueError('PDF differs from the exact user-designated paper: ' + name)
        elif f['class'] != 'HISTORICAL_PUBLIC_EXCEPTION':
            if not not name.endswith(('.map', '.zip', '.gz', '.npz', '.tar', '.pdf', '.csv', '.ndjson', '.tex')):
                raise ValueError(name)
    return {'status': 'PASS', 'files': len(expected), 'policy': manifest['policy']}
if __name__ == '__main__':
    print(json.dumps(verify(sys.argv[1] if len(sys.argv) > 1 else '.', tracked='--tracked' in sys.argv)))
