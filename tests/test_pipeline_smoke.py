import importlib, pytest

MODULES = ['keyword_generator', 'content_writer', 'editor_seo_optimizer', 'qa_filter', 'run_pipeline']

@pytest.mark.parametrize('mod', MODULES)
def test_imports(mod):
    importlib.import_module(mod)
