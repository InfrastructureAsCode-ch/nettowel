from typing import IO, Any
import ruamel.yaml


def load(f: IO[str]) -> Any:
    """YAML load data from stream

    Args:
        f (IO[str]): IO Stream with data

    Returns:
        Any: YAML Data
    """
    yml = ruamel.yaml.YAML(typ="safe")
    return yml.load(f)
