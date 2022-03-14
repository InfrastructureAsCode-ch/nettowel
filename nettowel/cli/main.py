import typer

from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.markdown import Markdown
from rich.console import Group
from rich import print

from nettowel import __version__ as version
from nettowel.cli._common import get_typer_app
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
from nettowel.cli.help import get_qrcode, HELP_MARKDOWN

app = get_typer_app(help="Awesome collection of network automation functions")

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


@app.command()
def help(
    ctx: typer.Context,
) -> None:
    qrcodes = []
    for title, data in [
        ("GitHub NetTowel", "https://github.com/InfrastructureAsCode-ch/nettowel"),
        ("@InfraAsCode", "https://twitter.com/InfraAsCode/with_replies"),
        ("infrastructureascode.ch", "https://infrastructureascode.ch/?from=nettowel"),
    ]:
        qrcodes.append(
            Panel(
                get_qrcode(data),
                title=f"[yellow][link={data}]{title}[/link]",
                border_style="blue",
            )
        )
    qr_panels = Columns(qrcodes, equal=True)
    title_panel = Panel(
        Text(f"NetTowel {version}", style="b yellow", justify="center"),
        border_style="yellow",
    )
    markdown = Markdown(HELP_MARKDOWN)
    top = Panel(
        Group(title_panel, markdown, qr_panels),
        title="[blue]Help",
        expand=False,
        border_style="green",
    )
    print(top)


def run() -> None:
    app()


if __name__ == "__main__":
    run()
