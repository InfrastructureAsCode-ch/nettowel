from typing import Any

try:
    from ttp import ttp

    TTP_INSTALLED = True

except ImportError:
    TTP_INSTALLED = False

NOT_INSTALLED = "TTP is not installed. Install it with pip: pip install nettowel[ttp]"


def render_template(
    template: str,
    data: str,
) -> Any:
    try:
        parser = ttp(data=data, template=template)
        parser.parse()

        results = parser.result()[0]
    except Exception as exc:
        raise exc
    return results
