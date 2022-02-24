from re import L, template
import sys
import typer
from typing import Any, Dict, List
from rich import print_json, print

from rich.panel import Panel
from rich.columns import Columns
from rich.console import Group
from rich.syntax import Syntax
from rich.tree import Tree
from rich.scope import render_scope
from rich.json import JSON


from nettowel.yaml import load as yaml_load
from nettowel.cli._common import get_members, cleanup_dict
from nettowel.jinja import render_template, validate_template, get_variables

app = typer.Typer(help="Templating (Jinja2) functions")


def _variable_tree(data: Dict[str, Any]) -> Tree:
    root = Tree(":books: Variables", style="blue", guide_style="blue")

    types = {
        "boolean": ":keycap_10: boolean",
        "null": ":no_entry: null",
        "number": ":input_numbers: number",
        "string": ":newspaper: string",
        "error": "[red]Type unknown[/]",
    }

    def add(tree: Tree, data: Dict[str, Any], required: bool = True) -> Tree:
        property_type = data.get("type")
        name = data.get("title")
        text = (
            f"[blue]{name} [i](required)[/]"
            if required
            else f"[green]{name} [i](optional)[/]"
        )
        if property_type in ["string", "boolean", "number", "null"]:
            tree.add(Group(text, f'[yellow]{types[data.get("type", "error")]}[/]'))

        if "anyOf" in data:
            any_of = Tree("anyOf", style="yellow", guide_style="yellow")
            [
                any_of.add(types[x.get("type", "error")])
                for x in data.get("anyOf", dict())
            ]
            tree.add(Group(text, any_of))

        if property_type == "array":
            items = data.get("items", dict())
            if items.get("type") == "object":
                color = "blue" if required else "green"
                tree.add(
                    Group(
                        text,
                        add(
                            Tree(
                                ":open_book: object", style="yellow", guide_style=color
                            ),
                            items,
                        ),
                    )
                )
            else:
                any_of_array = items.get("anyOf")
                array = Tree("array (anyOf)", style="yellow", guide_style="yellow")
                [array.add(types[x.get("type", "error")]) for x in any_of_array]
                tree.add(Group(text, array))

        if property_type == "object":
            for property, value in data.get("properties", dict()).items():
                add(tree, value, property in data.get("required", list()))

        return tree

    for property, value in data.get("properties", dict()).items():
        add(root, value, property in data.get("required", list()))
    return root


@app.command()
def render(
    ctx: typer.Context,
    template_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="TEMPLATE",
    ),
    data_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="DATA",
    ),
    trim_blocks: bool = typer.Option(False, "--trim-blocks"),
    lstrip_blocks: bool = typer.Option(False, "--lstrip-blocks"),
    keep_trailing_newline: bool = typer.Option(False, "--keep-trailing-newline"),
    json: bool = typer.Option(False, "--json", help="JSON output"),
    raw: bool = typer.Option(False, "--raw", help="Raw output"),
    only_result: bool = typer.Option(False, "--print-result-only", help="Raw output"),
    floating_panels: bool = typer.Option(
        False,
        "--floating-panels",
        help="Adjust the width of the panel to fit the content",
    ),
) -> None:
    try:
        if template_file_name == "-":
            template_text = sys.stdin.read()
        else:
            with open(template_file_name) as template_file:  # type: ignore
                template_text = template_file.read()
        if data_file_name == "-":
            input_data = yaml_load(sys.stdin)
        else:
            with open(data_file_name) as data_file:  # type: ignore
                input_data = yaml_load(data_file)

        result = render_template(
            template=template_text,
            data=input_data,
            trim_blocks=trim_blocks,
            lstrip_blocks=lstrip_blocks,
            keep_trailing_newline=keep_trailing_newline,
        )

        if json:
            return_data = {
                "result": result,
                "template": template_text,
                "input_data": input_data,
            }
            if only_result:
                print_json(data={"result": result})
            else:
                print_json(data=return_data)
        elif raw:
            print(result)
        else:
            if floating_panels:
                code_width = (
                    max(
                        [len(x) for x in template_text.split("\n")]
                        + [len(x) for x in result.split("\n")]
                    )
                    + 6
                )
            else:
                code_width = None
            panels: List[Panel] = []
            if not only_result:
                data_output = JSON.from_data(input_data)
                template_output = Syntax(
                    template_text,
                    "jinja",
                    line_numbers=True,
                    indent_guides=True,
                    code_width=code_width,
                )
                panels.append(
                    Panel(
                        template_output, title="[yellow]Template", border_style="blue"
                    )
                )
                panels.append(
                    Panel(data_output, title="[yellow]Data", border_style="blue")
                )
            panels.append(
                Panel(
                    Syntax(
                        result,
                        "yaml",
                        line_numbers=True,
                        indent_guides=True,
                        code_width=code_width,
                    ),
                    border_style="blue",
                    title="[yellow]Result",
                )
            )
            if not only_result and floating_panels:
                height = (
                    max(
                        [
                            len(result.split("\n")),
                            len(data_output.text.plain.split("\n")),
                            len(template_text.split("\n")),
                        ]
                    )
                    + 2
                )
                for p in panels:
                    p.height = height
            print(Columns(panels, equal=True))
        typer.Exit(0)

    except ValueError as exc:
        typer.echo(exc, err=True)
        typer.Exit(1)


@app.command()
def validate(
    ctx: typer.Context,
    template_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="TEMPLATE",
    ),
    json: bool = typer.Option(default=False, help="json output"),
) -> None:
    try:
        if template_file_name == "-":
            template_text = sys.stdin.read()
        else:
            with open(template_file_name) as template_file:  # type: ignore
                template_text = template_file.read()
        result, data = validate_template(template_text)
        if json:
            data["valid"] = result
            print_json(data=data)
        else:
            if result:
                print(
                    Panel(
                        "Template is valid :white_heavy_check_mark:",
                        border_style="green",
                        expand=False,
                    )
                )
            else:
                pannel_group = Group(
                    Panel(
                        "Template is [red bold]not[/] valide :hankey:",
                        border_style="red",
                    ),
                    f'The validation resulted in the error "{data["message"]}" in the line number {data["lineno"]}.',
                    f'The error is probably in the following line or before or after it.\n\n{data["line"]}\n',
                    render_scope(data, title=str(data["message"])),
                )
                print(
                    Panel(pannel_group, border_style="red", title="ERROR", expand=False)
                )
        if not result:
            typer.Exit(1)
        typer.Exit(0)

    except ValueError:
        typer.echo("Error", err=True)
        typer.Exit(1)


@app.command()
def variables(
    ctx: typer.Context,
    template_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="TEMPLATE",
    ),
    json: bool = typer.Option(default=False, help="json output"),
) -> None:

    try:
        if template_file_name == "-":
            template_text = sys.stdin.read()
        else:
            with open(template_file_name) as template_file:  # type: ignore
                template_text = template_file.read()
        result = get_variables(template_text)
        if json:
            data = {"result": result}
            print_json(data=data)
        else:
            print(_variable_tree(result))
    except Exception:
        raise


if __name__ == "__main__":
    app()
