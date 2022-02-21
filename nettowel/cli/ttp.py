import typer
from rich import inspect as rich_inspect
from rich import print_json

from nettowel.cli._common import get_members, cleanup_dict


app = typer.Typer(help="Templating (Jinja2) functions")


@app.command()
def demo(
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
