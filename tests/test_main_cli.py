import pytest
from typer.testing import CliRunner
from nettowel.cli.main import app

runner = CliRunner(mix_stderr=False)


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Awesome collection of network automation functions" in result.stdout
    assert "Failed to import" not in result.stderr
    assert not result.stderr
