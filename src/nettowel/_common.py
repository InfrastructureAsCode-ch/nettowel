from nettowel.exceptions import NettowelDependencyMissing
from nettowel.logger import log


def needs(needs: bool, package: str, group: str) -> bool:
    if not needs:
        log.warning(
            "Package %s is not installed. It is part of the nettowel group %s",
            package,
            group,
        )
        raise NettowelDependencyMissing(package, group)
    log.debug("Package %s is installed", package)
    return True
