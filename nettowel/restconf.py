from typing import Any, List
from nettowel.logging import log
from nettowel.exceptions import NettowelRestconfError

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore

content_type = {
    "json": "application/yang-data+json",
    "xml": "application/yang-data+xml",
}
accept = {
    "json": "application/yang-data+json, application/yang-data.errors+json",
    "xml": "application/yang-data+xml, application/yang-data.errors+xml",
}


def send_request(
    method: str,
    url: str,
    username: str,
    password: str,
    data: str = None,
    verify: bool = True,
    send_xml: bool = False,
    return_xml: bool = False,
) -> Any:
    try:
        headers = {
            "Content-Type": content_type["xml"] if send_xml else content_type["json"],
            "Accept": accept["xml"] if return_xml else accept["json"],
        }
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            auth=(username, password),
            data=data,
            verify=verify,
        )
        response.raise_for_status()
        if response.status_code == 204:
            return "204 No Content"
        return response.json() if not return_xml else response.text
    except requests.exceptions.ConnectionError as exc:
        raise NettowelRestconfError(str(exc), None)
    except requests.exceptions.RequestException as exc:
        if exc.request:
            if not exc.response.text:
                response = None
            else:
                response = exc.response.text if return_xml else exc.response.json()
        else:
            response = None
        log.debug(response)
        raise NettowelRestconfError(str(exc), response)
