from typing import Any, List
from nettowel._common import needs
from nettowel.logging import log

_module = "netmiko"

try:
    from netmiko import ConnectHandler
    from netmiko.ssh_dispatcher import CLASS_MAPPER_BASE as NETMIKO_DEVICE_TYPES

    log.debug("Successfully imported %s", _module)
    NETMIKO_INSTALLED = True

except ImportError:
    log.warning("Failed to import %s", _module)
    NETMIKO_INSTALLED = False


def get_device_types() -> List[str]:
    needs(NETMIKO_INSTALLED, "Netmiko", _module)
    return list(NETMIKO_DEVICE_TYPES.keys())


def send_command(
    cmd: str,
    device_type: str,
    host: str,
    username: str,
    password: str,
    port: int = 22,
    secret: str = "",
) -> str:
    device = ConnectHandler(
        device_type=device_type,
        host=host,
        username=username,
        password=password,
        port=port,
        secret=secret,
    )
    return str(device.send_command(cmd))
