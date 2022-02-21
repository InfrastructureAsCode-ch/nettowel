from typing import Union
import typer
from rich import inspect as rich_inspect
from rich import print_json

from nettowel.cli._common import get_members, cleanup_dict

from ipaddress import ip_address, ip_network, IPv4Address, IPv6Address


app = typer.Typer(help="IP Address tools")


@app.command()
def ip_info(
    ctx: typer.Context,
    ip: str,
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        ip_obj: Union[IPv4Address, IPv6Address] = ip_address(ip)
        data = get_members(ip_obj)
        data.pop("packed")
        if json:
            print_json(data=cleanup_dict(data))
        else:
            rich_inspect(ip_obj)
        typer.Exit(0)

    except ValueError as exc:
        typer.echo(exc)
        typer.Exit(1)


@app.command()
def network_info(
    ctx: typer.Context,
    network: str,
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        net_obj = ip_network(network)
        data = get_members(net_obj)
        for key in ["broadcast_address", "hostmask", "netmask", "network_address"]:
            data[key] = str(data[key])

        if json:
            print_json(data=cleanup_dict(data))
        else:
            rich_inspect(net_obj)
        typer.Exit(0)

    except ValueError as exc:
        typer.echo(exc)
        typer.Exit(1)


if __name__ == "__main__":
    app()
