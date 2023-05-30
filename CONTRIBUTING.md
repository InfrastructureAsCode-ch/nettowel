# Contributing to NetTowel

Contributions are highly welcomed and appreciated!

## Development Environment

NetTowel uses [poetry](https://python-poetry.org/docs/) for packaging and
dependency management.

### Tests

NetTowel uses [`pytest`](https://docs.pytest.org/) testing tool 
Run tests with the following command:

```
make pytest
```

Make sure to test new code and not break existing tests.

### Type Checking

NetTowel uses type annotations and `mypy` is used as a static type checker.
Run the following to type check NetTowel:

```
make mypy
```

Please add type annotations for all new code.

### Code Formatting

NetTowel uses [`black`](https://github.com/psf/black) for code formatting.
Run the following to check the formatting:

```
make black
```

### All Tests

Before pushing a commit all tests should be run. 
Run the following command:

```
make pytest
```

### Bump version

The version can be updated with the following command:
Steps: patch, minor, major, prepatch, preminor, premajor, prerelease.

```bash
make bump ARGS=patch
```

### Install branch from git with extras

To install a branch with `pip` and be able to specify the extras use the following command:

```bash
pip install git+https://github.com/InfrastructureAsCode-ch/nettowel.git@<branch_name>#egg=nettowel[<extras>]
```

Example:

```bash
pip install git+https://github.com/InfrastructureAsCode-ch/nettowel.git@develop#egg=nettowel[full]
```
