from nettowel.exceptions import NettowelDependencyMissing


def test_dependency_error() -> None:
    exc = NettowelDependencyMissing("myPackage", "tests")
    assert (
        "myPackage is not installed. Install it with pip: pip install nettowel[tests]"
        == str(exc)
    )

    exc = NettowelDependencyMissing("myPackage", "tests", "{package}|{group}")
    assert "myPackage|tests" == str(exc)
