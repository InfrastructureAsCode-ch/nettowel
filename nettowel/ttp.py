from typing import Any
from nettowel._common import needs
from nettowel.logger import log

_module = "ttp"

try:
    from ttp import ttp

    log.debug("Successfully imported %s", _module)
    TTP_INSTALLED = True

except ImportError:
    log.warning("Failed to import %s", _module)
    TTP_INSTALLED = False


def render_template(
    data: str,
    template: str,
) -> Any:
    needs(TTP_INSTALLED, "TTP", _module)
    try:
        parser = ttp(data=data, template=template)
        parser.parse()
        results = parser.result(structure="flat_list")
    except Exception as exc:
        raise exc
    return results
