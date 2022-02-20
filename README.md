# nettowel
Collection of useful network automation functions 

## Install

```
git clone ....
cd nettowel
poetry install
poetry run nettowel --help
```

## Building CLI Docs

**At the moment `typer-cli` is not ready for typer 0.4.0**

```
typer nettowel/cli/main.py utils docs --name nettowel --output CLI.md
```
