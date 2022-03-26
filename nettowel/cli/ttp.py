import sys
import typer
from typing import List
from rich import print_json, print

from rich.json import JSON
from rich.panel import Panel
from rich.columns import Columns
from rich.syntax import Syntax

from nettowel.cli._common import get_typer_app
from nettowel.ttp import render_template


app = get_typer_app(help="TTP templating functions")


@app.command()
def render(
    ctx: typer.Context,
    data_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="DATA",
        help="RAW data like CLI show command outputs or configuration snippets",
    ),
    template_file_name: typer.FileText = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        metavar="TEMPLATE",
        help="TTP template used to get structured data from the raw data",
    ),
    json: bool = typer.Option(default=False, help="json output"),
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
            input_data = sys.stdin.read()
        else:
            with open(data_file_name) as data_file:  # type: ignore
                input_data = data_file.read()

        result = render_template(template=template_text, data=input_data)
        if json:
            print_json(data=result)

        else:
            result_output = JSON.from_data(result)
            if floating_panels:
                code_width = (
                    max(
                        [len(x) for x in template_text.split("\n")]
                        + [len(x) for x in result_output.text.plain.split("\n")]
                    )
                    + 6
                )
            else:
                code_width = None
            panels: List[Panel] = []
            if not only_result:
                data_output = Syntax(
                    input_data,
                    "jinja",
                    line_numbers=True,
                    indent_guides=True,
                    code_width=code_width,
                )
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
                    result_output,
                    border_style="blue",
                    title="[yellow]Result",
                )
            )
            if not only_result and floating_panels:
                height = (
                    max(
                        [
                            len(result_output.text.plain.split("\n")),
                            len(input_data.split("\n")),
                            len(template_text.split("\n")),
                        ]
                    )
                    + 2
                )
                for p in panels:
                    p.height = height
            print(Columns(panels, equal=True))
        typer.Exit(0)

    except NotImplementedError as exc:
        typer.echo(exc)
        typer.Exit(1)


if __name__ == "__main__":
    app()
