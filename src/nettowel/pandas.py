from typing import Any
import io
from nettowel.logger import log
from nettowel._common import needs

_module = "pandas"

try:
    import pandas as pd

    log.debug("Successfully imported %s", _module)
    PANDA_INSTALLED = True

except ImportError:
    log.warning("Failed to import %s", _module)
    PANDA_INSTALLED = False


def normalize(input_data: Any, sep: str) -> str:
    """Normalize/flatten yaml or json data

    Args:
        data (any): Python datastructure
        sep (str): Separator

    Returns:
        str: Normalized data as csv
    """
    needs(PANDA_INSTALLED, "pandas", _module)
    df = pd.json_normalize(input_data, sep=sep)
    with io.StringIO() as f:
        df.to_csv(f)
        return f.getvalue()
