init:
	pipenv install --ignore-pipfile --dev

test:
	pipenv run pytest -vv

lint:
	pipenv run black --diff --check models.py main.py create_folder.py utils tests
	pipenv run flake8 models.py main.py create_folder.py utils tests
	pipenv run mypy models.py main.py create_folder.py utils tests --no-incremental --ignore-missing-imports --check-untyped-defs

run:
	pipenv run -- main --filepath </Volumes/Media/Staging/> --tv_shows 0