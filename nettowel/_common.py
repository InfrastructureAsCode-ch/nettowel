from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def needs(needs: bool, error_msg: str) -> Callable[[F], F]:
    """
    Decorator to check if the dependencies are installed.
    """

    def decorator_need(func: F) -> F:
        if not needs:
            raise Exception(error_msg)
        return func

    return decorator_need
