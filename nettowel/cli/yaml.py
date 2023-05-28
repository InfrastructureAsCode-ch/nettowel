import typer
from rich import print_json, print
from rich.panel import Panel
from rich.syntax import Syntax
from rich.json import JSON

from nettowel.cli._common import (
    auto_complete_paths,
    read_yaml,
    get_typer_app,
)
from nettowel.yaml import dump as yaml_dump
from nettowel.exceptions import NettowelInputError

app = get_typer_app(help="YAML functions")


@app.command()
def load(
    ctx: typer.Context,
    data_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="YAML",
        help="YAML Data",
        autocompletion=auto_complete_paths,
    ),
    json: bool = typer.Option(False, "--json", help="JSON output"),
    raw: bool = typer.Option(False, "--raw", help="Raw result output"),
) -> None:
    try:
        data = read_yaml(data_file_name)
        if json or raw:
            print_json(data=data)
        else:
            data_output = JSON.from_data(data)
            print(Panel(data_output, title="[yellow]Data", border_style="blue"))
        raise typer.Exit(0)
    except NettowelInputError as exc:
        typer.echo("Input is not valide", err=True)
        typer.echo(str(exc), err=True)
        raise typer.Exit(3)


@app.command()
def dump(
    ctx: typer.Context,
    data_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="YAML",
        help="YAML Data",
        autocompletion=auto_complete_paths,
    ),
    json: bool = typer.Option(False, "--json", help="JSON output"),
    raw: bool = typer.Option(False, "--raw", help="Raw result output"),
) -> None:
    try:
        data = read_yaml(data_file_name)
        result = yaml_dump(data).strip()
        if json:
            print_json(data={"yaml": result})
        elif raw:
            print(result)
        else:
            print(
                Panel(
                    Syntax(
                        result,
                        "yaml",
                        line_numbers=True,
                        indent_guides=True,
                    ),
                    border_style="blue",
                    title="[yellow]YAML",
                )
            )
        raise typer.Exit(0)
    except NettowelInputError as exc:
        typer.echo("Input is not valide", err=True)
        typer.echo(str(exc), err=True)
        raise typer.Exit(3)


if __name__ == "__main__":
    app()
