from typer.testing import CliRunner
from nettowel.cli.ip import app

runner = CliRunner(mix_stderr=False)


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "ip-info" in result.stdout
    assert "network-info" in result.stdout


def test_ip_info_v4() -> None:
    result = runner.invoke(app, ["ip-info", "127.0.0.1"])
    assert result.exit_code == 0
    assert "is_global = False" in result.stdout
    assert "is_private = True" in result.stdout
    assert "version = 4" in result.stdout
    assert "reverse_pointer = '1.0.0.127.in-addr.arpa'" in result.stdout


def test_ip_info_v6() -> None:
    result = runner.invoke(app, ["ip-info", "::1"])
    assert result.exit_code == 0
    assert "is_global = False" in result.stdout
    assert "is_private = True" in result.stdout
    assert "version = 6" in result.stdout
    assert "0000:0000:0000:0000:0000:0000:0000:0001" in result.stdout


def test_ip_info_error() -> None:
    result = runner.invoke(app, ["ip-info", "0.0.0.0/0"])
    assert result.exit_code == 1
    assert "'0.0.0.0/0' does not appear to be an IPv4 or IPv6 address" in result.stderr


def test_network_info_v4() -> None:
    result = runner.invoke(app, ["network-info", "10.0.0.0/8"])
    assert result.exit_code == 0
    assert "is_global = False" in result.stdout
    assert "is_private = True" in result.stdout
    assert "version = 4" in result.stdout
    assert "prefixlen = 8" in result.stdout
    assert "num_addresses = 16777216" in result.stdout
    assert "with_hostmask = '10.0.0.0/0.255.255.255'" in result.stdout


def test_network_info_v6() -> None:
    result = runner.invoke(app, ["network-info", "2001:db8:c0fe::/64"])
    assert result.exit_code == 0
    assert "is_global = False" in result.stdout
    assert "is_private = True" in result.stdout
    assert "version = 6" in result.stdout
    assert "2001:0db8:c0fe:0000:0000:0000:0000:0000/64" in result.stdout
    assert "num_addresses = 18446744073709551616" in result.stdout


def test_network_info_error() -> None:
    result = runner.invoke(app, ["network-info", "127.0.0.1/33"])
    assert result.exit_code == 1
    assert (
        "'127.0.0.1/33' does not appear to be an IPv4 or IPv6 network" in result.stderr
    )
