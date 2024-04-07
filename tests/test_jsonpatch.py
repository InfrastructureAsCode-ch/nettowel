import json
from pathlib import Path

import pytest
from typer.testing import CliRunner
from nettowel.cli.jsonpatch import app

pytestmark = pytest.mark.jsonpatch
runner = CliRunner(mix_stderr=False)


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "apply" in result.stdout
    assert "create" in result.stdout


def test_create() -> None:
    result = runner.invoke(
        app, ["create", "tests/jsonpatch/data1.yaml", "tests/jsonpatch/data2.yaml"]
    )
    assert result.exit_code == 0
    assert "replace" in result.stdout
    assert "/interfaces/1/mask" in result.stdout
    assert "255.255.255.192" in result.stdout


def test_create_raw() -> None:
    result = runner.invoke(
        app,
        ["create", "tests/jsonpatch/data1.yaml", "tests/jsonpatch/data2.yaml", "--raw"],
    )
    assert result.exit_code == 0
    result = json.loads(result.stdout)
    with Path("tests/jsonpatch/data_patch.json").open() as f:
        expected = json.load(f)
    assert result == expected


def test_apply() -> None:
    result = runner.invoke(
        app, ["apply", "tests/jsonpatch/data_patch.json", "tests/jsonpatch/data1.yaml"]
    )
    assert result.exit_code == 0
    assert "255.255.255.192" in result.stdout


def test_apply_raw() -> None:
    result = runner.invoke(
        app,
        [
            "apply",
            "tests/jsonpatch/data_patch.json",
            "tests/jsonpatch/data1.yaml",
            "--raw",
        ],
    )
    assert result.exit_code == 0
    result = json.loads(result.stdout)
    assert isinstance(result, dict)
    assert result["interfaces"][1]["mask"] == "255.255.255.192"
