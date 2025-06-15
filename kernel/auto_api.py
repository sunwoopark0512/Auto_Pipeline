from fastapi import FastAPI
import importlib
import yaml
import pathlib

SPEC_PATH = pathlib.Path(__file__).resolve().parent.parent / 'saas.yaml'
MODULES_DIR = pathlib.Path(__file__).resolve().parent.parent / 'modules'


def load_spec(path: pathlib.Path = SPEC_PATH) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


app = FastAPI()


def register_routes(spec: dict) -> None:
    for mod in spec.get('modules', []):
        module = importlib.import_module(f"modules.{mod['name']}")
        fn = getattr(module, mod['name'])
        app.post(f"/{mod['name']}")(fn)


spec_data = load_spec()
register_routes(spec_data)
