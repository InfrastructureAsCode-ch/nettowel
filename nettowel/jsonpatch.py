from typing import Any, List, Dict
from nettowel.logger import log
from nettowel._common import needs

_module = "jsonpatch"

try:
    from jsonpatch import JsonPatch

    log.debug("Successfully imported %s", _module)
    JSONPATCH_INSTALLED = True

except ImportError:
    log.warning("Failed to import %s", _module)
    JSONPATCH_INSTALLED = False


def create(src: Any, dst: Any) -> "JsonPatch":
    """Create a JSON patch [RFC 6902](http://tools.ietf.org/html/rfc6902)

    Args:
        src (any): Data source datastructure
        dst (any): Data destination datastructure

    Returns:
        JsonPatch: JsonPatch object containing the patch
    """
    needs(JSONPATCH_INSTALLED, "jsonpatch", _module)
    patch = JsonPatch.from_diff(src=src, dst=dst)
    return patch


def apply(patch: List[Dict[str, Any]], data: Any) -> Any:
    """Apply a JSON patch [RFC 6902](http://tools.ietf.org/html/rfc6902)

    Args:
        patch (list[dict]): List of patch instructions
        data (any): Data to apply the patch onto

    Returns:
        result: Updated data object
    """
    needs(JSONPATCH_INSTALLED, "jsonpatch", _module)
    jp = JsonPatch(patch)
    result = jp.apply(data)
    return result
