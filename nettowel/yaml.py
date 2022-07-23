from typing import IO, Any
import io
import ruamel.yaml
from ruamel.yaml.error import MarkedYAMLError
from nettowel.exceptions import NettowelInputError


def load(f: IO[str]) -> Any:
    """YAML load data from stream

    Args:
        f (IO[str]): IO Stream with data

    Returns:
        Any: YAML Data
    """
    yaml = ruamel.yaml.YAML(typ="safe")
    try:
        return yaml.load(f)

    except MarkedYAMLError as exc:
        raise NettowelInputError(str(exc))


def dump(data: Any) -> str:
    """Dump data as YAML to stream

    Args:
        data: Data to dump as YAML

    Returns:
        str: YAML Data
    """
    stream = io.StringIO()
    yaml = ruamel.yaml.YAML(typ="safe")
    yaml.default_flow_style = False
    yaml.dump(data=data, stream=stream)
    return stream.getvalue()
