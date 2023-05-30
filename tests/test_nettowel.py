from nettowel import __version__


def test_version() -> None:
    assert __version__ == "0.5.1"  # From Makefile
