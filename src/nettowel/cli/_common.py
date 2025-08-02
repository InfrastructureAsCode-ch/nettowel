import sys
import typer
from typing import Any, Dict, Generator, Optional, List
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from nettowel.yaml import load as yaml_load
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


def auto_complete_paths(incomplete: str) -> Generator[str, None, None]:
    incomplete_path = Path(incomplete)
    if incomplete_path.is_dir():
        glob = incomplete_path.glob("*")
    else:
        glob = incomplete_path.parent.glob(f"{incomplete_path.stem}*")
    for path in glob:
        if path.is_dir():
            yield f"{path}/"
        yield str(path)


def callback(
    dotenv: typer.FileText = typer.Option(
        None,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help=".env configuration file. If no file is specified, an attempt is made to search the .env file from cwd.",
        autocompletion=auto_complete_paths,
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


def read_text(data_file_name: typer.FileText) -> str:
    if data_file_name == "-":
        return sys.stdin.read()
    else:
        with open(data_file_name) as template_file:  # type: ignore
            text: str = template_file.read()
        return text


def read_yaml(data_file_name: typer.FileText) -> Any:
    if data_file_name == "-":
        return yaml_load(sys.stdin)
    else:
        with open(data_file_name) as data_file:  # type: ignore
            return yaml_load(data_file)
