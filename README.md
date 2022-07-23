[![PyPI versions](https://img.shields.io/pypi/pyversions/nettowel.svg)](https://pypi.python.org/pypi/nettowel/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

# NetTowel
Collection of useful network automation functions 


> ⚠️ `nettowel` is under heavy construction and not production ready. Feedback is highly appreciated.


## Install

You can install it directly from pypi

```bash
pip install nettowel
```

To reduce the dependencies the extra dependencies are grouped

The following groups are available (more details in the pyproject.toml):

- full
- jinja
- ttp
- textfsm
- napalm
- netmiko
- scrapli
- nornir
- pandas

```bash
pip install nettowel[jinja]
pip install nettowel[full]
```

## Install from source

```
git clone ....
cd nettowel
poetry install
poetry run nettowel --help
```


## Help and shell auto-completion

Thanks to the library [typer](https://typer.tiangolo.com/), `nettowel` comes with a nice help and autocompletion install

![help](imgs/help.png)


## Features

Many features are not implemented yet and many features will come.



### Jinja2

#### render

![jinja rendering 1](imgs/jinja-render-3.png)

![jinja rendering 2](imgs/jinja-render-1.png)

#### validate

![jinja validate](imgs/jinja-validate.png)

#### variables

![jinja variables](imgs/jinja-variables.png)


### TTP

#### render

![ttp render](imgs/ttp-render.png)

### Netmiko

#### cli

![netmiko cli](imgs/netmiko-cli.png)

#### autodetect

![netmiko autodetect](imgs/netmiko-autodetect.png)

#### device-types

![netmiko device types](imgs/netmiko-device-types.png)


### RESTCONF

#### get

![restconf get](imgs/restconf-get.png)

#### patch, delete

![restconf patch delete](imgs/restconf-patch-delete.png)

#### post, put

![restconf post put](imgs/restconf-post-put.png)

### ipaddress

#### ip-info

![ip info](imgs/ip-info.png)

#### network-info

![network info](imgs/network-info.png)


### Help

![Help QRcode](imgs/nettowel-help.png)


### Settings

A `dotenv` file can be used as a settings file. The file can also be provided with the option `--dotenv`.

![environment settings](imgs/env-settings.png)


### Piping

![piping](imgs/piping.png)



## Building CLI Docs

**At the moment `typer-cli` is not ready for typer 0.4.0**

```
typer nettowel/cli/main.py utils docs --name nettowel --output CLI.md
```

## Contributing

### Run tests:

```bash
make tests
```


### Bump version:

Steps: patch, minor, major, prepatch, preminor, premajor, prerelease.

```bash
make bump ARGS=patch
```