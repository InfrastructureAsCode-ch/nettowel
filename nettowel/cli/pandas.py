import io
import typer
from rich import print_json, print
from rich.panel import Panel
from nettowel.cli._common import get_typer_app, auto_complete_paths, read_yaml

import pandas as pd


app = get_typer_app(help="[EXPERIMENTAL] Pandas tools")


@app.command()
def flatten(
    ctx: typer.Context,
    data: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        help="JSON/YAML file to flatten.",
        autocompletion=auto_complete_paths,
    ),
    sep: str = typer.Option(default=".", help="separator"),
    json: bool = typer.Option(default=False, help="json output"),
    raw: bool = typer.Option(default=False, help="raw output"),
) -> None:
    input_data = read_yaml(data)
    normalized = pd.json_normalize(input_data, sep=sep)
    with io.StringIO() as f:
        normalized.to_csv(f)
        result = f.getvalue()
    if json:
        print_json(data={"result": result})
    elif raw:
        print(result)
    else:
        print(Panel(result, title=f"[yellow]flatten", border_style="blue"))


if __name__ == "__main__":
    app()
