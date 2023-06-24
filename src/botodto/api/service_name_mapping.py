from __future__ import annotations

from typing import NoReturn

__all__ = ["MappedServiceName"]


class MappedServiceName:
    boto3: str
    _supported_services: list[str] = ["stepfunctions"]

    def __init__(self, boto3_name: str) -> None:
        self.boto3 = boto3_name

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(boto3={self.boto3!r})"

    def invalidate(self, explanation: str) -> NoReturn:
        raise ValueError(explanation + f": {self!r}")

    @classmethod
    def ensure(cls, service_name: str | MappedServiceName) -> MappedServiceName:
        """
        Helper to 'ensure' a string value is turned into a MappedServiceName.
        """
        if isinstance(service_name, str):
            service_name = MappedServiceName(service_name)
        return service_name
