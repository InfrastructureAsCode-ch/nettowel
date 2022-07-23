from typing import IO, Any
import io
import ruamel.yaml


def load(f: IO[str]) -> Any:
    """YAML load data from stream

    Args:
        f (IO[str]): IO Stream with data

    Returns:
        Any: YAML Data
    """
    yaml = ruamel.yaml.YAML(typ="safe")
    return yaml.load(f)


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
