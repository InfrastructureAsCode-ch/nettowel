from typing import IO, Any
import ruamel.yaml


def load(f: IO[str]) -> Any:
    yml = ruamel.yaml.YAML(typ="safe")
    return yml.load(f)
