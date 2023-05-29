from typing import Union, Optional
import sys
import typer
from urllib.parse import quote
from rich import print_json, print
from rich.syntax import Syntax
from rich.prompt import Prompt
from rich.json import JSON
from rich.panel import Panel

from nettowel.cli._common import get_typer_app, auto_complete_paths
from nettowel.exceptions import (
    NettowelRestconfError,
)
from nettowel.restconf import send_request

app = get_typer_app(help="RESTCONF functions")


def _send_request(
    path: str,
    method: str,
    host: str,
    user: str,
    password: str,
    port: int,
    send_xml: bool,
    return_xml: bool,
    json: bool,
    raw: bool,
    verify: bool,
    data_file: Optional[typer.FileText] = None,
) -> None:
    try:
        if not user:
            user = Prompt.ask("Enter username")
        if not password:
            password = Prompt.ask(f"Enter password for user {user}", password=True)

        if data_file:
            if data_file == "-":
                data = sys.stdin.read()
            else:
                with open(data_file) as f:  # type: ignore
                    data = f.read()
        else:
            data = None

        result = send_request(
            method=method,
            url=f"https://{host}:{port}/restconf/data/{path}",
            username=user,
            password=password,
            send_xml=send_xml,
            return_xml=return_xml,
            verify=verify,
            data=data,
        )
        if raw:
            print(result)
        elif json:
            print_json(data=result)
        else:
            if return_xml:
                output: Union[Syntax, JSON] = Syntax(
                    result,
                    "xml",
                    line_numbers=True,
                    indent_guides=True,
                )
            else:
                output = JSON.from_data(result)
            print(
                Panel(
                    output,
                    title=f"[yellow][bold]{method}[/bold] {path}",
                    border_style="blue",
                )
            )
        raise typer.Exit(0)
    except NettowelRestconfError as exc:
        typer.echo(str(exc), err=True)
        if exc.server_msg:
            typer.echo(exc.server_msg, err=True)
        raise typer.Exit(1)


@app.command()
def get(
    ctx: typer.Context,
    path: str = typer.Argument(
        ..., help="RESTCONF path. Example: Cisco-IOS-XE-native:native/hostname"
    ),
    host: str = typer.Option(
        ..., help="Hostname or IP address", envvar="NETTOWEL_HOST"
    ),
    user: str = typer.Option(None, help="Username for login", envvar="NETTOWEL_USER"),
    password: str = typer.Option(
        None, help="Login password", envvar="NETTOWEL_PASSWORD"
    ),
    port: int = typer.Option(
        default=443, help="Connection Port", envvar="NETTOWEL_RESTCONF_PORT"
    ),
    send_xml: bool = typer.Option(
        False,
        "--send-xml",
        help="Send XML instead of JSON",
    ),
    return_xml: bool = typer.Option(
        False,
        "--return-xml",
        help="Recieve XML instead of JSON",
    ),
    verify: bool = typer.Option(
        False,
        "--no-verify",
        help="Ignore SSL certificate verification",
        envvar="NETTOWEL_VERIFY",
    ),
    json: bool = typer.Option(default=False, help="json output"),
    raw: bool = typer.Option(default=False, help="raw output"),
) -> None:
    _send_request(
        path=path,
        method="GET",
        host=host,
        user=user,
        password=password,
        port=port,
        send_xml=send_xml,
        return_xml=return_xml,
        json=json,
        raw=raw,
        verify=verify,
    )


@app.command()
def delete(
    ctx: typer.Context,
    path: str = typer.Argument(
        ..., help="RESTCONF path. Example: Cisco-IOS-XE-native:native/hostname"
    ),
    host: str = typer.Option(
        ..., help="Hostname or IP address", envvar="NETTOWEL_HOST"
    ),
    user: str = typer.Option(None, help="Username for login", envvar="NETTOWEL_USER"),
    password: str = typer.Option(
        None, help="Login password", envvar="NETTOWEL_PASSWORD"
    ),
    port: int = typer.Option(
        default=443, help="Connection Port", envvar="NETTOWEL_RESTCONF_PORT"
    ),
    send_xml: bool = typer.Option(
        False,
        "--send-xml",
        help="Send XML instead of JSON",
    ),
    return_xml: bool = typer.Option(
        False,
        "--return-xml",
        help="Recieve XML instead of JSON",
    ),
    verify: bool = typer.Option(
        False,
        "--no-verify",
        help="Ignore SSL certificate verification",
        envvar="NETTOWEL_VERIFY",
    ),
    json: bool = typer.Option(default=False, help="json output"),
    raw: bool = typer.Option(default=False, help="raw output"),
) -> None:
    _send_request(
        path=path,
        method="DELETE",
        host=host,
        user=user,
        password=password,
        port=port,
        send_xml=send_xml,
        return_xml=return_xml,
        json=json,
        verify=verify,
        raw=raw,
    )


@app.command()
def post(
    ctx: typer.Context,
    path: str = typer.Argument(
        ..., help="RESTCONF path. Example: Cisco-IOS-XE-native:native/hostname"
    ),
    data_file: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="DATA",
        help="Data to send. Use '-' to read from stdin",
        autocompletion=auto_complete_paths,
    ),
    host: str = typer.Option(
        ..., help="Hostname or IP address", envvar="NETTOWEL_HOST"
    ),
    user: str = typer.Option(None, help="Username for login", envvar="NETTOWEL_USER"),
    password: str = typer.Option(
        None, help="Login password", envvar="NETTOWEL_PASSWORD"
    ),
    port: int = typer.Option(
        default=443, help="Connection Port", envvar="NETTOWEL_RESTCONF_PORT"
    ),
    send_xml: bool = typer.Option(
        False,
        "--send-xml",
        help="Send XML instead of JSON",
    ),
    return_xml: bool = typer.Option(
        False,
        "--return-xml",
        help="Recieve XML instead of JSON",
    ),
    verify: bool = typer.Option(
        False,
        "--no-verify",
        help="Ignore SSL certificate verification",
        envvar="NETTOWEL_VERIFY",
    ),
    json: bool = typer.Option(default=False, help="json output"),
    raw: bool = typer.Option(default=False, help="raw output"),
) -> None:
    _send_request(
        path=path,
        method="POST",
        host=host,
        user=user,
        password=password,
        port=port,
        send_xml=send_xml,
        return_xml=return_xml,
        json=json,
        raw=raw,
        verify=verify,
        data_file=data_file,
    )


@app.command()
def PUT(
    ctx: typer.Context,
    path: str = typer.Argument(
        ..., help="RESTCONF path. Example: Cisco-IOS-XE-native:native/hostname"
    ),
    data_file: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="DATA",
        help="Data to send. Use '-' to read from stdin",
        autocompletion=auto_complete_paths,
    ),
    host: str = typer.Option(
        ..., help="Hostname or IP address", envvar="NETTOWEL_HOST"
    ),
    user: str = typer.Option(None, help="Username for login", envvar="NETTOWEL_USER"),
    password: str = typer.Option(
        None, help="Login password", envvar="NETTOWEL_PASSWORD"
    ),
    port: int = typer.Option(
        default=443, help="Connection Port", envvar="NETTOWEL_RESTCONF_PORT"
    ),
    send_xml: bool = typer.Option(
        False,
        "--send-xml",
        help="Send XML instead of JSON",
    ),
    return_xml: bool = typer.Option(
        False,
        "--return-xml",
        help="Recieve XML instead of JSON",
    ),
    verify: bool = typer.Option(
        False,
        "--no-verify",
        help="Ignore SSL certificate verification",
        envvar="NETTOWEL_VERIFY",
    ),
    json: bool = typer.Option(default=False, help="json output"),
    raw: bool = typer.Option(default=False, help="raw output"),
) -> None:
    _send_request(
        path=path,
        method="PUT",
        host=host,
        user=user,
        password=password,
        port=port,
        send_xml=send_xml,
        return_xml=return_xml,
        json=json,
        raw=raw,
        verify=verify,
        data_file=data_file,
    )


@app.command()
def patch(
    ctx: typer.Context,
    path: str = typer.Argument(
        ..., help="RESTCONF path. Example: Cisco-IOS-XE-native:native/hostname"
    ),
    data_file: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="DATA",
        help="Data to send. Use '-' to read from stdin",
        autocompletion=auto_complete_paths,
    ),
    host: str = typer.Option(
        ..., help="Hostname or IP address", envvar="NETTOWEL_HOST"
    ),
    user: str = typer.Option(None, help="Username for login", envvar="NETTOWEL_USER"),
    password: str = typer.Option(
        None, help="Login password", envvar="NETTOWEL_PASSWORD"
    ),
    port: int = typer.Option(
        default=443, help="Connection Port", envvar="NETTOWEL_RESTCONF_PORT"
    ),
    send_xml: bool = typer.Option(
        False,
        "--send-xml",
        help="Send XML instead of JSON",
    ),
    return_xml: bool = typer.Option(
        False,
        "--return-xml",
        help="Recieve XML instead of JSON",
    ),
    verify: bool = typer.Option(
        False,
        "--no-verify",
        help="Ignore SSL certificate verification",
        envvar="NETTOWEL_VERIFY",
    ),
    json: bool = typer.Option(default=False, help="json output"),
    raw: bool = typer.Option(default=False, help="raw output"),
) -> None:
    _send_request(
        path=path,
        method="PATCH",
        host=host,
        user=user,
        password=password,
        port=port,
        send_xml=send_xml,
        return_xml=return_xml,
        json=json,
        raw=raw,
        verify=verify,
        data_file=data_file,
    )


@app.command()
def head(
    ctx: typer.Context,
    path: str = typer.Argument(
        ..., help="RESTCONF path. Example: Cisco-IOS-XE-native:native/hostname"
    ),
    host: str = typer.Option(
        ..., help="Hostname or IP address", envvar="NETTOWEL_HOST"
    ),
    user: str = typer.Option(None, help="Username for login", envvar="NETTOWEL_USER"),
    password: str = typer.Option(
        None, help="Login password", envvar="NETTOWEL_PASSWORD"
    ),
    port: int = typer.Option(
        default=443, help="Connection Port", envvar="NETTOWEL_RESTCONF_PORT"
    ),
    send_xml: bool = typer.Option(
        False,
        "--send-xml",
        help="Send XML instead of JSON",
    ),
    return_xml: bool = typer.Option(
        False,
        "--return-xml",
        help="Recieve XML instead of JSON",
    ),
    verify: bool = typer.Option(
        False,
        "--no-verify",
        help="Ignore SSL certificate verification",
        envvar="NETTOWEL_VERIFY",
    ),
    json: bool = typer.Option(default=False, help="json output"),
    raw: bool = typer.Option(default=False, help="raw output"),
) -> None:
    _send_request(
        path=path,
        method="HEAD",
        host=host,
        user=user,
        password=password,
        port=port,
        send_xml=send_xml,
        return_xml=return_xml,
        json=json,
        raw=raw,
        verify=verify,
    )


@app.command()
def endcode(
    ctx: typer.Context,
    text: str = typer.Argument(..., help="Text to encode / quote"),
    json: bool = typer.Option(default=False, help="json output"),
    raw: bool = typer.Option(default=False, help="raw output"),
) -> None:
    result = quote(text, safe="")
    if json:
        print_json(data={"result": result})
    elif raw:
        print(result)
    else:
        print(Panel(result, title=f"[yellow]{text}", border_style="blue"))


if __name__ == "__main__":
    app()
