import pytest
from typer.testing import CliRunner
from nettowel.cli.ttp import app

pytestmark = pytest.mark.ttp
runner = CliRunner(mix_stderr=False)


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "render" in result.stdout


def test_render_arp() -> None:
    result = runner.invoke(
        app, ["render", "tests/ttp/data1.txt", "tests/ttp/template1.txt"]
    )
    assert result.exit_code == 0
    assert '"protocol": "Internet",' in result.stdout
    assert '"ip": "10.18.8.2",' in result.stdout
    assert '"age": 0,' in result.stdout
    assert '"mac": "52:54:00:fd:7d:ba",' in result.stdout
    assert '"type": "ARPA",' in result.stdout
    assert '"interface": "GigabitEthernet6"' in result.stdout


def test_render_interface() -> None:
    result = runner.invoke(
        app,
        [
            "render",
            "tests/ttp/data2.txt",
            "tests/ttp/template2.txt",
            "--print-result-only",
        ],
    )
    assert result.exit_code == 0
    assert "interface Loopback0" not in result.stdout
    assert '"ip": "192.168.0.113",' in result.stdout
    assert '"vrf": "CPE1",' in result.stdout
    assert '"ip": "2002::fd37",' in result.stdout
    assert '"description": "CPE_Acces_Vlan",' in result.stdout
