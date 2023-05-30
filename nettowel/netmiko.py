from typing import Any, List, Optional
from nettowel._common import needs
from nettowel.logger import log
from nettowel.exceptions import NettowelTimeoutError

_module = "netmiko"

try:
    from netmiko import ConnectHandler, SSHDetect
    from netmiko.ssh_dispatcher import CLASS_MAPPER_BASE as NETMIKO_DEVICE_TYPES
    from netmiko.base_connection import BaseConnection
    from netmiko.ssh_exception import NetmikoTimeoutException

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
    username: Optional[str] = None,
    password: Optional[str] = None,
    port: int = 22,
    secret: str = "",
    use_textfsm: bool = False,
    use_ttp: bool = False,
    ttp_template: Optional[str] = None,
    use_genie: bool = False,
    ssh_config_file: Optional[str] = None,
    use_keys: bool = False,
    key_file: Optional[str] = None,
    session_log: Optional[str] = None,
) -> str:
    try:
        device: BaseConnection = ConnectHandler(
            device_type=device_type,
            host=host,
            username=username,
            password=password,
            port=port,
            secret=secret,
            ssh_config_file=ssh_config_file,
            use_keys=use_keys,
            key_file=key_file,
            session_log=session_log,
        )
        if not device.check_enable_mode():
            device.enable()

        return str(
            device.send_command(
                cmd,
                use_textfsm=use_textfsm,
                use_genie=use_genie,
                use_ttp=use_ttp,
                ttp_template=ttp_template,
            )
        )
    except NetmikoTimeoutException as esc:
        raise NettowelTimeoutError(str(esc))


def autodetect(
    host: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    port: int = 22,
    secret: str = "",
    ssh_config_file: Optional[str] = None,
    use_keys: bool = False,
    key_file: Optional[str] = None,
    session_log: Optional[str] = None,
) -> str:
    guesser = SSHDetect(
        device_type="autodetect",
        host=host,
        username=username,
        password=password,
        port=port,
        secret=secret,
        ssh_config_file=ssh_config_file,
        use_keys=use_keys,
        key_file=key_file,
        session_log=session_log,
    )
    return str(guesser.autodetect())
