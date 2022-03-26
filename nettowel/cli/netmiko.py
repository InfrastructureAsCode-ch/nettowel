from typing import Tuple
import typer
from rich import print_json, print
from rich.markdown import Markdown
from rich.prompt import Prompt

from nettowel.cli._common import get_typer_app
from nettowel.exceptions import (
    NettowelDependencyMissing,
    NettowelException,
    NettowelTimeoutError,
)
from nettowel.netmiko import get_device_types, send_command
from nettowel.netmiko import autodetect as netmiko_autodetect

app = get_typer_app(help="Netmiko functions")


@app.command()
def cli(
    ctx: typer.Context,
    host: str = typer.Argument(..., help="Hostname or IP address"),
    cmd: str = typer.Argument(..., help="CLI command to execute on device"),
    device_type: str = typer.Option(
        ..., help="Netmiko device type", envvar="NETTOWEL_DEVICE_TYPE"
    ),
    user: str = typer.Option(None, help="Username for login", envvar="NETTOWEL_USER"),
    password: str = typer.Option(
        None, help="Login password", envvar="NETTOWEL_PASSWORD"
    ),
    port: int = typer.Option(
        default=22, help="Connection Port", envvar="NETTOWEL_PORT"
    ),
    secret: str = typer.Option(
        default="", help="Enable secret", envvar="NETTOWEL_SECRET"
    ),
    use_textfsm: bool = typer.Option(
        False,
        "--use-textfsm",
        help="Use textFSM to get structured data",
        envvar="NETTOWEL_NETMIKO_TEXTFSM",
    ),
    use_ttp: bool = typer.Option(
        False,
        "--use-ttp",
        help="Use TTP to get structured data",
        envvar="NETTOWEL_NETMIKO_TTP",
    ),
    ttp_template: str = typer.Option(
        None,
        help="Use TTP Template. Use it with the `use_ttp` parameter",
        envvar="NETTOWEL_NETMIKO_TTP_TEMPLATE",
    ),
    use_genie: bool = typer.Option(
        False,
        "--use-genie",
        help="Use Genie to get structured data",
        envvar="NETTOWEL_NETMIKO_GENIE",
    ),
    ssh_config_file: str = typer.Option(
        None, help="SSH Config file", envvar="NETTOWEL_SSH_CONFIG"
    ),
    use_keys: bool = typer.Option(
        False,
        "--use-keys",
        help="Use provided SSH Key. Parameter `key_file` is used.",
        envvar="NETTOWEL_USE_KEY",
    ),
    key_file: str = typer.Option(
        None,
        help="SSH Key file. Use it with the `key_file` parameter",
        envvar="NETTOWEL_KEY_FILE",
    ),
    session_log: str = typer.Option(
        None, help="File to store session log", envvar="NETTOWEL_SESSION_LOG"
    ),
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        if not any([user, ssh_config_file]):
            user = Prompt.ask("Enter username")
        if not any([password, use_keys, ssh_config_file]):
            password = Prompt.ask(f"Enter password for user {user}", password=True)
        result = send_command(
            cmd=cmd,
            device_type=device_type,
            host=host,
            username=user,
            password=password,
            port=port,
            secret=secret,
            use_textfsm=use_textfsm,
            use_ttp=use_ttp,
            ttp_template=ttp_template,
            use_genie=use_genie,
            ssh_config_file=ssh_config_file,
            use_keys=use_keys,
            key_file=key_file,
            session_log=session_log,
        )
        if json:
            print_json(data={"cmd": cmd, "result": result})
        else:
            print(result)
        typer.Exit(0)

    except NettowelException as exc:
        typer.echo(str(exc), err=True)
        typer.Exit(1)


@app.command()
def device_types(
    ctx: typer.Context,
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        types = get_device_types()
        if json:
            print_json(data=types)
        else:
            output = Markdown("\n".join([f"- {x}" for x in types]))
            print(output)
        typer.Exit(0)

    except NettowelException as exc:
        typer.echo(str(exc), err=True)
        typer.Exit(1)


@app.command()
def autodetect(
    ctx: typer.Context,
    host: str = typer.Argument(..., help="Hostname or IP address"),
    user: str = typer.Option(None, help="Username for login", envvar="NETTOWEL_USER"),
    password: str = typer.Option(
        None, help="Login password", envvar="NETTOWEL_PASSWORD"
    ),
    port: int = typer.Option(
        default=22, help="Connection Port", envvar="NETTOWEL_PORT"
    ),
    secret: str = typer.Option(
        default="", help="Enable secret", envvar="NETTOWEL_SECRET"
    ),
    ssh_config_file: str = typer.Option(
        None, help="SSH Config file", envvar="NETTOWEL_SSH_CONFIG"
    ),
    use_keys: bool = typer.Option(
        False,
        "--use-keys",
        help="Use provided SSH Key. Parameter `key_file` is used.",
        envvar="NETTOWEL_USE_KEY",
    ),
    key_file: str = typer.Option(
        None,
        help="SSH Key file. Use it with the `key_file` parameter",
        envvar="NETTOWEL_KEY_FILE",
    ),
    session_log: str = typer.Option(
        None, help="File to store session log", envvar="NETTOWEL_SESSION_LOG"
    ),
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        if not any([user, ssh_config_file]):
            user = Prompt.ask("Enter username")
        if not any([password, use_keys, ssh_config_file]):
            password = Prompt.ask(f"Enter password for user {user}", password=True)
        result = netmiko_autodetect(
            host=host,
            username=user,
            password=password,
            port=port,
            secret=secret,
            ssh_config_file=ssh_config_file,
            use_keys=use_keys,
            key_file=key_file,
            session_log=session_log,
        )
        if json:
            print_json(data={"result": result})
        else:
            print(result)
        typer.Exit(0)

    except NettowelException as exc:
        typer.echo(str(exc), err=True)
        typer.Exit(1)


if __name__ == "__main__":
    app()
