import pytest
from typer.testing import CliRunner
from nettowel.cli.yaml import app

pytestmark = pytest.mark.yaml
runner = CliRunner(mix_stderr=False)


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "load" in result.stdout
    assert "dump" in result.stdout


def test_load_json1() -> None:
    result = runner.invoke(app, ["load", "tests/yaml/json1.json"])
    assert result.exit_code == 0
    assert '"id": "G4hjVuvdSnWD03cug8sdOA",' in result.stdout
    assert '"categories": [],' in result.stdout


def test_load_json1_raw() -> None:
    result = runner.invoke(app, ["load", "tests/yaml/json1.json", "--raw"])
    assert result.exit_code == 0
    assert '"id": "G4hjVuvdSnWD03cug8sdOA",' in result.stdout
    assert '"categories": [],' in result.stdout
    assert "─ Data ─" not in result.stdout


def test_load_yaml1() -> None:
    result = runner.invoke(app, ["load", "tests/yaml/yaml1.yaml"])
    assert result.exit_code == 0
    assert '"name": "Urs",' in result.stdout
    assert '"pickups_lines": [' in result.stdout


def test_load_yaml1_raw() -> None:
    result = runner.invoke(app, ["load", "tests/yaml/yaml1.yaml", "--raw"])
    assert result.exit_code == 0
    assert '"name": "Urs",' in result.stdout
    assert '"pickups_lines": [' in result.stdout
    assert "─ Data ─" not in result.stdout


def test_dump_json1() -> None:
    result = runner.invoke(app, ["dump", "tests/yaml/json1.json"])
    assert result.exit_code == 0
    assert "id: G4hjVuvdSnWD03cug8sdOA" in result.stdout
    assert "categories: []" in result.stdout


def test_dump_json1_raw() -> None:
    result = runner.invoke(app, ["dump", "tests/yaml/json1.json", "--raw"])
    assert result.exit_code == 0
    assert "id: G4hjVuvdSnWD03cug8sdOA" in result.stdout
    assert "categories: []" in result.stdout
    assert "─ YAML ─" not in result.stdout
