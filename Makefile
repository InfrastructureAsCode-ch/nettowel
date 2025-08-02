PROJECT=nettowel
CODE_DIRS=src/${PROJECT} tests
IMG_URL=https://raw.githubusercontent.com/InfrastructureAsCode-ch/nettowel/main/imgs/

# Run pytest
.PHONY: pytest
pytest:
	uv run pytest -vs ${ARGS}

# Check if the python code needs to be reformatted 
.PHONY: black
black:
	uv run black --check ${CODE_DIRS}

# Python type check
.PHONY: mypy
mypy:
	uv run mypy ${CODE_DIRS}

# Runn pytest, black and mypy
.PHONY: tests
tests: pytest black mypy

# use "make bump ARGS=patch" to bump the version. ARGS can be patch, minor or major.
.PHONY: bump
bump:
	uv version --bump ${ARGS}
	sed -i -E "s|\"\b[0-9]+.\b[0-9]+.\b[0-9]+\"  # From Makefile|\"`uv version --short`\"  # From Makefile|g" src/${PROJECT}/__init__.py
	sed -i -E "s|\"\b[0-9]+.\b[0-9]+.\b[0-9]+\"  # From Makefile|\"`uv version --short`\"  # From Makefile|g" tests/test_${PROJECT}.py

# Used in the pipeline to change the image urls befor publishing it on pypi.org
.PHONY: fiximageurls
fiximageurls:
	sed -i "s|](imgs/|](${IMG_URL}|g" README.md

# Create a new tag and push it to origin. This will triger the pipeline and a new release will be published
.PHONY: tag
tag:
	git checkout main
	git pull
	git tag -a "v`uv version --short`" -m "Version v`uv version --short`"
	git push --tags
	git checkout -
