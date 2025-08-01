from typing import Optional
from nettowel.logger import log
from nettowel._common import needs
from nettowel.exceptions import NettowelTimeoutError

_module = "ncclient"

try:
    from ncclient import manager, xml_

    log.debug("Successfully imported %s", _module)
    NCCLIENT_INSTALLED = True

except ImportError:
    log.warning("Failed to import %s", _module)
    NCCLIENT_INSTALLED = False


def get(
    host: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    port: int = 22,
    lock: bool = False,
    hostkey_verify: bool = True,
) -> str:
    try:
        with manager.connect(
            host=host,
            username=username,
            password=password,
            port=port,
            hostkey_verify=hostkey_verify,
        ) as m:
            try:
                if lock:
                    m.lock("running")
                _ = m.get_config(source="running")

                filter_interface = """
                <native>
                <interface>
                </interface>
                </native>"""

                _ = m.get(filter=("subtree", filter_interface))

                filter_exec_banner = """
                <native>
                <banner>
                <exec>
                </exec>
                </banner>
                </native>"""
                _ = m.get(filter=("subtree", filter_exec_banner))

                _ = m.get(filter=("xpath", "/native/banner/exec"))

                set_exec_banner = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <banner>
    <exec>
    <banner>
    test1234
    </banner>
    </exec>
    </banner>
  </native>
  </config>
    """
                _ = m.edit_config(
                    target="running", config=set_exec_banner, default_operation="merge"
                )

                del_exec_banner = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <banner>
    <exec operation="delete" />
    </banner>
  </native>
  </config>
    """
                result = m.edit_config(target="running", config=del_exec_banner)

                return str(result)

            finally:
                if lock:
                    m.unlock("running")

    except Exception as esc:
        # raise NettowelTimeoutError(str(esc))
        raise esc


filter = """
<isis xmls="clns-isis-oper">
</isis>
"""
