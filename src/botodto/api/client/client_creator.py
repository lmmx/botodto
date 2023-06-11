from __future__ import annotations

from typing import NoReturn

from ...aws.map_source import v2_to_v3

__all__ = ["Client"]

boto3_to_js_v2 = {"stepfunctions": "states"}


class MappedServiceName:
    boto3: str
    js_v2: str
    js_v3: str

    def __init__(self, boto3_name: str) -> None:
        self.boto3 = boto3_name
        self.js_v2 = self.identify_v2()
        self.js_v3 = self.identify_v3()

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


class Client:
    service_name: MappedServiceName

    def __init__(self, boto3_name: str):
        self.service_name = MappedServiceName(boto3_name)
