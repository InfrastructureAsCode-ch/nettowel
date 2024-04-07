from nettowel import __version__


def test_version() -> None:
    assert __version__ == "0.6.1"  # From Makefile
