"""Package editable sources and final artifacts, excluding caches and previews."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
import hashlib

ROOT = Path(__file__).resolve().parent
report = json.loads((ROOT / 'verification.json').read_text())
for name, metadata in report['documents'].items():
    document = ROOT / 'output/pdf' / f'{name}.pdf'
    assert hashlib.sha256(document.read_bytes()).hexdigest() == metadata['sha256']
paths = set()
for pattern in ('*.py', '*.tex', '*.json', 'README*', 'LICENSE', 'NOTICE', '.gitignore'):
    paths.update(ROOT.glob(pattern))
for directory in ('original', 'foundations', 'explanations', 'figures'):
    paths.update(p for p in (ROOT / directory).rglob('*') if p.is_file())
paths.update((ROOT / 'output/pdf').glob('*.pdf'))
assert len(list((ROOT / 'figures').glob('*.png'))) == report['figure_manifest']['count']
destination = ROOT / 'output/integer-multiplication-editable-package.zip'
with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
    for path in sorted(paths):
        archive.write(path, path.relative_to(ROOT))
with ZipFile(destination) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(paths)
print(f'Packaged {len(paths)} files: {destination}')
