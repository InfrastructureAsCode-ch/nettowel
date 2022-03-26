import typer
from typing import Any, Dict, Optional, List
from dotenv import load_dotenv, find_dotenv

from nettowel.cli.logging import configure_logger, log

VERBOSE_LEVEL = -1
DOTENV_LOADED = False


def _load_dotenv(dotenv: str) -> None:
    global DOTENV_LOADED
    if dotenv:
        log.debug("Loading dotenv file %s", dotenv)
        load_dotenv(dotenv)
    else:
        if DOTENV_LOADED:
            log.debug("Default dotenv file already loaded")
            return
        log.debug("Search in increasingly higher folders for dotenv file from cwd")
        dotenv_file = find_dotenv(usecwd=True)
        if dotenv_file:
            log.debug("Loading dotenv file %s", dotenv_file)
            load_dotenv(dotenv_file)
    DOTENV_LOADED = True


def _config_logging(verbose: int) -> None:
    global VERBOSE_LEVEL
    if VERBOSE_LEVEL == -1:
        VERBOSE_LEVEL = verbose
    elif verbose == 0:
        return
    else:
        VERBOSE_LEVEL += verbose
    level = 10 * (5 - max(0, min(VERBOSE_LEVEL, 4)))
    configure_logger(level=level)
    log.debug("Set logging level to %d", level)


def callback(
    dotenv: typer.FileText = typer.Option(
        None,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help=".env configuration file. If no file is specified, an attempt is made to search the .env file from cwd.",
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Set de logging level. Default level is 'CRITICAL'",
    ),
) -> None:
    _config_logging(verbose)
    _load_dotenv(str(dotenv) if dotenv else "")


def get_typer_app(help: str) -> typer.Typer:
    return typer.Typer(help=help, callback=callback)


def get_members(obj: object, members: Optional[List[str]] = None) -> Dict[str, Any]:
    if members is None:
        members = [member for member in dir(obj) if not member.startswith("_")]
    return {x: getattr(obj, x) for x in members}


def cleanup_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if not callable(v)}
