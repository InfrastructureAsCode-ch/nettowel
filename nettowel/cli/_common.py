from typing import Any, Dict, Optional, List
from rich import print_json


def get_members(obj: object, members: Optional[List[str]] = None) -> Dict[str, Any]:
    if members is None:
        members = [member for member in dir(obj) if not member.startswith("_")]
    return {x: getattr(obj, x) for x in members}


def cleanup_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if not callable(v)}
