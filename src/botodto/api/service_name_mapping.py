from __future__ import annotations

from typing import NoReturn

from ..aws.map_source import boto3_to_js_v2, v2_to_v3

__all__ = ["MappedServiceName"]


class MappedServiceName:
    boto3: str
    js_v2: str
    js_v3: str
    _supported_services: list[str] = ["stepfunctions"]

    def __init__(self, boto3_name: str) -> None:
        self.boto3 = boto3_name
        self.js_v2 = self.identify_v2()
        self.js_v3 = self.identify_v3()

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return (
            f"{cls}(boto3={self.boto3!r}, js_v2={self.js_v2!r}, js_v3={self.js_v3!r})"
        )

    def identify_v2(self) -> str:
        js_v2 = boto3_to_js_v2.get(self.boto3)
        if js_v2 is None:
            self.invalidate("How boto3 service names map to JS SDK v2 not established")
        return js_v2

    def identify_v3(self) -> str:
        js_v3 = v2_to_v3.get(self.js_v2)
        if js_v3 is None:
            self.invalidate("JS SDK v2 service name failed to map to a v3 service name")
        return js_v3

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
