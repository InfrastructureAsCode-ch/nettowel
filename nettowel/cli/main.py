import typer

from nettowel.cli.ip import app as ipaddress_app
from nettowel.cli.jinja import app as jinja_app
from nettowel.cli.ttp import app as ttp_app
from nettowel.cli.textfsm import app as textfsm_app
from nettowel.cli.diff import app as diff_app
from nettowel.cli.yaml import app as yaml_app
from nettowel.cli.nornir import app as nornir_app
from nettowel.cli.napalm import app as napalm_app
from nettowel.cli.netmiko import app as netmiko_app
from nettowel.cli.scrapli import app as scrapli_app


app = typer.Typer(help="Awesome collection of network automation functions")

for subapp, name in [
    (ipaddress_app, "ipaddress"),
    (jinja_app, "jinja"),
    (ttp_app, "ttp"),
    (textfsm_app, "textFSM"),
    (diff_app, "diff"),
    (yaml_app, "yaml"),
    (nornir_app, "nornir"),
    (napalm_app, "napalm"),
    (netmiko_app, "netmiko"),
    (scrapli_app, "scrapli"),
]:
    app.add_typer(subapp, name=name)


def run() -> None:
    app()


if __name__ == "__main__":
    run()
