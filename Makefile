init:
	pipenv install --ignore-pipfile

test:
	pipenv run pytest -vv

lint:
	pipenv run black --check models main create_folder utils tests
	pipenv run flake8 models main create_folder utils tests
	pipenv run mypy models main create_folder utils tests --no-incremental --ignore-missing-imports --check-untyped-defs

run:
	pipenv run -- main --filepath </Volumes/Media/Staging/> --tv_shows 0