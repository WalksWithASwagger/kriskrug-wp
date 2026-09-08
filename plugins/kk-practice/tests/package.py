"""Build only production plugin files, with stable ZIP metadata."""
import hashlib
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
target = Path('/tmp/kk-practice-0.1.0.zip')
files = [root / 'kk-practice.php', *sorted((root / 'blocks/context-brief').iterdir())]
with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        item = zipfile.ZipInfo('kk-practice/' + str(path.relative_to(root)), (2026, 9, 6, 0, 0, 0))
        item.compress_type = zipfile.ZIP_DEFLATED
        item.external_attr = 0o644 << 16
        archive.writestr(item, path.read_bytes())
print(f'{target.name} sha256={hashlib.sha256(target.read_bytes()).hexdigest()}')
