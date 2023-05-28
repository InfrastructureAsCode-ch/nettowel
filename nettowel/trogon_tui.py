from typing import Any, List
from typer import Context, Typer
from typer.main import get_group

from nettowel._common import needs
from nettowel.logger import log
from nettowel.exceptions import NettowelTimeoutError

_module = "tui"

try:
    from trogon import Trogon

    log.debug("Successfully imported %s", _module)
    TROGON_INSTALLED = True

except ImportError:
    log.warning("Failed to import %s", _module)
    TROGON_INSTALLED = False


def run_trogon_tui(
    app: Typer,
    ctx: Context,
) -> None:
    needs(TROGON_INSTALLED, "Trogon", _module)
    Trogon(get_group(app), click_context=ctx).run()
