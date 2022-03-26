from typing import Any, Tuple, Dict, Union
from nettowel.exceptions import NettowelDependencyMissing, NettowelSyntaxError
from nettowel.logging import log
from nettowel._common import needs

_module = "jinja2"

try:
    from jinja2 import Environment, Undefined, exceptions

    log.debug("Successfully imported %s", _module)
    JINJA_INSTALLED = True

except ImportError:
    log.warning("Failed to import %s", _module)
    JINJA_INSTALLED = False


def validate_template(template: str) -> Tuple[bool, Dict[str, Union[str, int, None]]]:
    """Validate jinja2 template

    Args:
        template (str): jinja2 template

    Returns:
        Tuple[bool, Dict[str, Union[str, int, None]]]: (True, {}) if template is valid. (False, {"message": ..., "lineno": ..., "line": ...})
    """
    needs(JINJA_INSTALLED, "Jinja2", _module)
    try:
        Environment().parse(template)
        return True, dict()
    except exceptions.TemplateSyntaxError as exc:
        try:
            line = template.splitlines()[exc.lineno - 1]
        except IndexError:
            line = ""

        result = {"message": exc.message, "lineno": exc.lineno, "line": line}

        return False, result


def render_template(
    template: str,
    data: Any,
    trim_blocks: bool = False,
    lstrip_blocks: bool = False,
    keep_trailing_newline: bool = False,
) -> str:
    """Rendering jinja2 template

    Args:
        template (str): Jinja template
        data (Any): Data to add to the rendering context. If data is not a dictionary it will be stored in one under the key 'data'
        trim_blocks (bool, optional): If this is set to True the first newline after a block is removed. Defaults to False.
        lstrip_blocks (bool, optional): If this is set to True leading spaces and tabs are stripped from the start of a line to a block. Defaults to False.
        keep_trailing_newline (bool, optional): Preserve the trailing newline when rendering templates. Defaults to False.

    Returns:
        str: Rendered template
    """
    needs(JINJA_INSTALLED, "Jinja2", _module)
    jinja_env = Environment(
        trim_blocks=trim_blocks,
        lstrip_blocks=lstrip_blocks,
        keep_trailing_newline=keep_trailing_newline,
        # extensions=[],
        undefined=Undefined,
    )
    if not isinstance(data, dict):
        data = {"data": data}

    try:
        return jinja_env.from_string(template).render(**data)
    except exceptions.TemplateSyntaxError as exc:
        raise NettowelSyntaxError(str(exc))


def get_variables(template: str) -> Any:
    """Get a list of variables with jinja2schema

    Args:
        template (str): Jinja template

    Raises:
        Exception: _description_

    Returns:
        Any: Return Dict with JSON Schema data
    """
    needs(JINJA_INSTALLED, "Jinja2", _module)
    try:
        from jinja2schema import infer, to_json_schema
    except ImportError:
        raise NettowelDependencyMissing("jinja2schema", _module)

    schema = infer(template)
    return to_json_schema(schema)
