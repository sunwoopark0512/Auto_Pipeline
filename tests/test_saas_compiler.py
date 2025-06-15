import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from kernel import saas_compiler  # noqa: E402


def test_generate_modules(tmp_path, monkeypatch):
    spec = {
        'modules': [
            {'name': 'foo', 'model': 'bar'},
        ]
    }
    temp_dir = tmp_path / 'modules'
    monkeypatch.setattr(saas_compiler, 'MODULES_DIR', temp_dir)
    saas_compiler.generate_modules(spec)
    generated = temp_dir / 'foo.py'
    assert generated.exists()
    module_spec = importlib.util.spec_from_file_location('foo', generated)
    mod = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(mod)
    assert hasattr(mod, 'foo')
