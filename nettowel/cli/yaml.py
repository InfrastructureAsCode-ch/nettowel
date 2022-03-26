import typer
from rich import inspect as rich_inspect
from rich import print_json

from nettowel.cli._common import get_members, cleanup_dict, get_typer_app


app = get_typer_app(help="Templating (Jinja2) functions")


@app.command()
def load(
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


@app.command()
def dump(
    ctx: typer.Context,
    demo: str,
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        demo_obj = {"a": 1}
        data = get_members(demo_obj)
        if json:
            print_json(data=cleanup_dict(data))
        else:
            rich_inspect(demo_obj)
        typer.Exit(0)

    except ValueError as exc:
        typer.echo(exc)
        typer.Exit(1)


if __name__ == "__main__":
    app()
