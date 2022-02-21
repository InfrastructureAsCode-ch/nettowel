import typer

from nettowel.cli.ip import app as ipaddress_app
from nettowel.cli.jinja import app as jinja_app

app = typer.Typer(help="Awesome collection of network automation functions")


app.add_typer(ipaddress_app, name="ipaddress")
app.add_typer(jinja_app, name="jinja")


def run() -> None:
    app()


if __name__ == "__main__":
    run()
