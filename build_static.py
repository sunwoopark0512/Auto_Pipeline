"""Simple build script to minify CSS and JS assets."""
from pathlib import Path

try:
    from csscompressor import compress as compress_css
except Exception:
    def compress_css(data: str) -> str:
        return ''.join(line.strip() for line in data.splitlines())

try:
    from jsmin import jsmin
except Exception:
    def jsmin(data: str) -> str:
        return ''.join(line.strip() for line in data.splitlines())

ASSETS_DIR = Path('assets')
STATIC_DIR = Path('static')

STATIC_DIR.joinpath('css').mkdir(parents=True, exist_ok=True)
STATIC_DIR.joinpath('js').mkdir(parents=True, exist_ok=True)
STATIC_DIR.joinpath('img').mkdir(parents=True, exist_ok=True)

for css_file in ASSETS_DIR.glob('css/*.css'):
    with open(css_file, 'r') as f:
        minified = compress_css(f.read())
    out_file = STATIC_DIR / 'css' / css_file.name
    with open(out_file, 'w') as f:
        f.write(minified)

for js_file in ASSETS_DIR.glob('js/*.js'):
    with open(js_file, 'r') as f:
        minified = jsmin(f.read())
    out_file = STATIC_DIR / 'js' / js_file.name
    with open(out_file, 'w') as f:
        f.write(minified)

for img_file in ASSETS_DIR.glob('img/*'):
    out_file = STATIC_DIR / 'img' / img_file.name
    if not out_file.exists():
        out_file.write_bytes(img_file.read_bytes())
