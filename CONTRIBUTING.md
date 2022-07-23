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
