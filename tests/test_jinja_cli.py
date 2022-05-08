import pytest
from typer.testing import CliRunner
from nettowel.cli.jinja import app

pytestmark = pytest.mark.jinja
runner = CliRunner(mix_stderr=False)


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "render" in result.stdout
    assert "validate" in result.stdout
    assert "variables" in result.stdout


def test_render_hi() -> None:
    result = runner.invoke(
        app, ["render", "tests/jinja/template1.j2", "tests/jinja/data1.yaml"]
    )
    assert result.exit_code == 0
    assert "Hi Joe" in result.stdout
    assert "How are you doing?" in result.stdout


def test_render_template_notfound() -> None:
    result = runner.invoke(app, ["render", "notfound", "tests/jinja/data1.yaml"])
    assert result.exit_code == 2
    assert (
        "Invalid value for 'TEMPLATE': File 'notfound' does not exist" in result.stderr
    )


def test_render_data_notfound() -> None:
    result = runner.invoke(app, ["render", "tests/jinja/template1.j2", "notfound"])
    assert result.exit_code == 2
    assert "Invalid value for 'DATA': File 'notfound' does not exist" in result.stderr


def test_render_macdonald_trim_blocks() -> None:
    result = runner.invoke(
        app,
        [
            "render",
            "tests/jinja/template2.j2",
            "tests/jinja/data2.yaml",
            "--trim-blocks",
        ],
    )
    assert result.exit_code == 0
    assert "9 Here a oink, there a oink, everywhere a oink oink." in result.stdout
    assert "15 Old MacDonald had a farm, E I E I O." in result.stdout


def test_render_interface_result_only() -> None:
    result = runner.invoke(
        app,
        [
            "render",
            "tests/jinja/template3.j2",
            "tests/jinja/data3.yaml",
            "--print-result-only",
        ],
    )
    assert result.exit_code == 0
    assert "{% for interface in interfaces %}" not in result.stdout
    assert "ip address 192.168.1.1 255.255.255.0" in result.stdout


def test_render_hi_raw() -> None:
    result = runner.invoke(
        app, ["render", "tests/jinja/template1.j2", "tests/jinja/data1.yaml", "--raw"]
    )
    assert result.exit_code == 0
    assert "Hi Joe\nHow are you doing?\n" == result.stdout


def test_render_error() -> None:
    result = runner.invoke(
        app, ["render", "tests/jinja/templateFail.j2", "tests/jinja/data1.yaml"]
    )
    assert result.exit_code == 2
    assert "expected token ':', got '}'" in result.stderr


def test_validate_hi() -> None:
    result = runner.invoke(app, ["validate", "tests/jinja/data1.yaml"])
    assert result.exit_code == 0
    assert "Template is valid" in result.stdout


def test_validate_fail() -> None:
    result = runner.invoke(app, ["validate", "tests/jinja/templateFail.j2"])
    assert result.exit_code == 1
    assert "Template is not valide" in result.stdout
    assert "{% if {{ test }} %}" in result.stdout
    assert "lineno = 4" in result.stdout


def test_variables_template4() -> None:
    result = runner.invoke(app, ["variables", "tests/jinja/template4.j2"])
    assert result.exit_code == 0
    assert "📚 Variables" in result.stdout
    assert "interfaces (required)" in result.stdout
    assert "── mylist (required)" in result.stdout


def test_variables_error() -> None:
    result = runner.invoke(app, ["variables", "tests/jinja/templateFail.j2"])
    assert result.exit_code == 2
    assert "expected token ':', got '}'" in result.stderr
