from typing import List

import typer
from rich import print_json, print
from rich.panel import Panel
from rich.columns import Columns
from rich.json import JSON

from nettowel.cli._common import (
    auto_complete_paths,
    read_yaml,
    get_typer_app,
)
from nettowel.exceptions import NettowelInputError


app = get_typer_app(help="JSON Patch [RFC 6902](http://tools.ietf.org/html/rfc6902)")


@app.command()
def create(
    ctx: typer.Context,
    src_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="src",
        help="Source data (YAML/JSON)",
        autocompletion=auto_complete_paths,
    ),
    dst_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="dst",
        help="Destination data (YAML/JSON)",
        autocompletion=auto_complete_paths,
    ),
    json: bool = typer.Option(False, "--json", help="JSON output"),
    raw: bool = typer.Option(False, "--raw", help="Raw result output"),
    only_result: bool = typer.Option(
        False, "--print-result-only", help="Only print the result"
    ),
) -> None:
    from nettowel import jsonpatch

    try:
        src = read_yaml(src_file_name)
        dst = read_yaml(dst_file_name)

        patch = jsonpatch.create(src=src, dst=dst)
        patch_str = patch.to_string()
        if json or raw:
            print_json(json=patch_str)
        else:
            panels: List[Panel] = []
            if not only_result:
                panels.append(
                    Panel(
                        JSON.from_data(src), title="[yellow]Source", border_style="blue"
                    )
                )
                panels.append(
                    Panel(
                        JSON.from_data(dst),
                        title="[yellow]Destrination",
                        border_style="blue",
                    )
                )
            panels.append(
                Panel(JSON(patch_str), title="[yellow]JSON Patch", border_style="blue")
            )
            print(Columns(panels, equal=True))
        raise typer.Exit(0)
    except NettowelInputError as exc:
        typer.echo("Input is not valide", err=True)
        typer.echo(str(exc), err=True)
        raise typer.Exit(3)


@app.command()
def apply(
    ctx: typer.Context,
    patch_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="patch",
        help="Patch opterations (list of mappings) (YAML/JSON)",
        autocompletion=auto_complete_paths,
    ),
    data_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="data",
        help="Data to patch (YAML/JSON)",
        autocompletion=auto_complete_paths,
    ),
    json: bool = typer.Option(False, "--json", help="JSON output"),
    raw: bool = typer.Option(False, "--raw", help="Raw result output"),
    only_result: bool = typer.Option(
        False, "--print-result-only", help="Only print the result"
    ),
) -> None:
    from nettowel import jsonpatch

    try:
        patch_data = read_yaml(patch_file_name)
        data_input = read_yaml(data_file_name)

        new_data = jsonpatch.apply(patch=patch_data, data=data_input)

        if json or raw:
            print_json(data=new_data)
        else:
            panels: List[Panel] = []
            if not only_result:
                panels.append(
                    Panel(
                        JSON.from_data(patch_data),
                        title="[yellow]Patch",
                        border_style="blue",
                    )
                )
                panels.append(
                    Panel(
                        JSON.from_data(data_input),
                        title="[yellow]Input Data",
                        border_style="blue",
                    )
                )
            panels.append(
                Panel(
                    JSON.from_data(data=new_data),
                    title="[yellow]Patched Data with JSON Patch",
                    border_style="blue",
                )
            )
            print(Columns(panels, equal=True))
        raise typer.Exit(0)
    except NettowelInputError as exc:
        typer.echo("Input is not valide", err=True)
        typer.echo(str(exc), err=True)
        raise typer.Exit(3)


if __name__ == "__main__":
    app()
