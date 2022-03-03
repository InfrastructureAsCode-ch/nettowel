from typing import Any
from nettowel._common import needs

try:
    from ttp import ttp

    TTP_INSTALLED = True

except ImportError:
    TTP_INSTALLED = False


def render_template(
    data: str,
    template: str,
) -> Any:
    needs(TTP_INSTALLED, "TTP", "ttp")
    try:
        parser = ttp(data=data, template=template)
        parser.parse()
        results = parser.result(structure="flat_list")
    except Exception as exc:
        raise exc
    return results
