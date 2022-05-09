PROJECT=nettowel
CODE_DIRS=${PROJECT} tests
IMG_URL=https://raw.githubusercontent.com/InfrastructureAsCode-ch/nettowel/main/imgs/

.PHONY: pytest
pytest:
	poetry run pytest -vs ${ARGS}

.PHONY: black
black:
	poetry run black --check ${CODE_DIRS}

.PHONY: mypy
mypy:
	poetry run mypy ${CODE_DIRS}

.PHONY: tests
tests: pytest black mypy

.PHONY: bump
bump:
	poetry version ${ARGS}
	sed -i -E "s|\"\b[0-9]+.\b[0-9]+.\b[0-9]+\"  # From Makefile|\"`poetry version -s`\"  # From Makefile|g" ${PROJECT}/__init__.py
	sed -i -E "s|\"\b[0-9]+.\b[0-9]+.\b[0-9]+\"  # From Makefile|\"`poetry version -s`\"  # From Makefile|g" tests/test_${PROJECT}.py

.PHONY: fiximageurls
fiximageurls:
	sed -i "s|](imgs/|](${IMG_URL}|g" README.md

.PHONY: tag
tag:
	git checkout main
	git pull
	git tag -a "v`poetry version -s`" -m "Version v`poetry version -s`"
	git push --tags
	git checkout -
