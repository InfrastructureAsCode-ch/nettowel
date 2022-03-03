import typer
from rich import print_json, print
from rich.markdown import Markdown
from rich.prompt import Prompt

from nettowel.cli._common import get_members, cleanup_dict
from nettowel.exceptions import NettowelDependencyMissing
from nettowel.netmiko import get_device_types, send_command

app = typer.Typer(help="Netmiko functions")


@app.command()
def cli(
    ctx: typer.Context,
    host: str = typer.Argument(..., help="Hostname or IP address"),
    cmd: str = typer.Argument(..., help="CLI command to execute on device"),
    device_type: str = typer.Option(..., help="Netmiko device type"),
    user: str = typer.Option(..., help="Username for login"),
    password: str = typer.Option(None, help="Login password"),
    port: int = typer.Option(default=22, help="Connection Port"),
    secret: str = typer.Option(default="", help="Enable secret"),
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        if not password:
            password = Prompt.ask(f"Enter password for user {user}", password=True)
        result = send_command(
            cmd=cmd,
            device_type=device_type,
            host=host,
            username=user,
            password=password,
            port=port,
            secret=secret,
        )
        if json:
            print_json(data={"cmd": cmd, "result": result})
        else:
            print(result)
        typer.Exit(0)

    except NettowelDependencyMissing as exc:
        typer.echo(exc)
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

    except NettowelDependencyMissing as exc:
        typer.echo(exc)
        typer.Exit(1)


if __name__ == "__main__":
    app()
