import typer
from rich import inspect as rich_inspect
from rich import print_json

from nettowel.cli._common import get_members, cleanup_dict


app = typer.Typer(help="TextFSM template functions")


@app.command()
def render(
    ctx: typer.Context,
    # demo: str,
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        raise NotImplementedError("Not Implemented Yet")
        if json:
            print_json(data=None)
        else:
            rich_inspect(None)
        typer.Exit(0)

    except NotImplementedError as exc:
        typer.echo(exc)
        typer.Exit(1)


if __name__ == "__main__":
    app()
