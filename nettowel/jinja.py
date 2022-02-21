from typing import Any
from nettowel._common import needs

try:
    from jinja2 import Environment, Undefined

    JINJA_INSTALLED = True

except ImportError:
    JINJA_INSTALLED = False

NOT_INSTALLED = (
    "Jinja2 is not installed. Install it with pip: pip install nettowel[jinja]"
)


@needs(JINJA_INSTALLED, NOT_INSTALLED)
def validate_template(template: str) -> None:
    pass


@needs(JINJA_INSTALLED, NOT_INSTALLED)
def render_template(
    template: str,
    data: Any,
    trim_blocks: bool = False,
    lstrip_blocks: bool = False,
    keep_trailing_newline: bool = False,
) -> str:
    jinja_env = Environment(
        trim_blocks=trim_blocks,
        lstrip_blocks=lstrip_blocks,
        keep_trailing_newline=keep_trailing_newline,
        # extensions=[],
        undefined=Undefined,
    )
    return jinja_env.from_string(template).render(**data)


@needs(JINJA_INSTALLED, NOT_INSTALLED)
def get_variables(template: str) -> None:
    pass
