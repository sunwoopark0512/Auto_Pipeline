PY=python

lint:
pylint autopipe --fail-under 8.5
$(PY) -m mypy autopipe

schema-check:
$(PY) -m autopipe.schema_check data/generated_hooks.json
