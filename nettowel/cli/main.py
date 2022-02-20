from typing import NoReturn
import typer

from nettowel.cli.ip import app as ipaddress_app

app = typer.Typer(help="Awesome collection of network automation functions")


app.add_typer(ipaddress_app, name="ipaddress")


def run() -> NoReturn:
    app()


if __name__ == "__main__":
    run()
