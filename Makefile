setup:
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

lint:
	pre-commit run --all-files
