from nettowel.exceptions import NettowelDependencyMissing


def needs(needs: bool, package: str, group: str) -> bool:
    if not needs:
        raise NettowelDependencyMissing(package, group)
    return True
