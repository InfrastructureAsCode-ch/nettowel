import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"


def configure_logger(level: int) -> None:
    logging.basicConfig(
        level=level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    log.setLevel(level)


log = logging.getLogger("nettowel")
log.info("Hello, World!")
