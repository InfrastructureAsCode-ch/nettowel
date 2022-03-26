class NettowelException(Exception):
    ...


class NettowelDependencyMissing(NettowelException):
    def __init__(
        self,
        package: str,
        extra_group: str,
        msg_format: str = "{package} is not installed. Install it with pip: pip install nettowel[{group}]",
    ) -> None:
        self.package = package
        self.extra_group = extra_group
        self.msg = msg_format.format(package=package, group=extra_group)
        super().__init__(self.msg)


class NettowelSyntaxError(NettowelException):
    ...


class NettowelTimeoutError(NettowelException):
    ...
