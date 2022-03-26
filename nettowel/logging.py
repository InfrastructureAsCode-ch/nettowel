from logging import getLogger

log = getLogger("nettowel")


def configure_logger(level: int) -> None:
    log.setLevel(level=level)
