import typer
from rich import inspect as rich_inspect
from rich import print_json

from nettowel.cli._common import get_typer_app


app = get_typer_app(help="NAPALM functions")


@app.command()
def demo(
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
        raise typer.Exit(0)

    except NotImplementedError as exc:
        typer.echo(exc)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
