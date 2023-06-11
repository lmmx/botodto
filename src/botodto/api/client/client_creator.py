from __future__ import annotations

from ...aws.service_models import ServiceModels
from .service_name_mapping import MappedServiceName

__all__ = ["Client"]


class Client:
    service_name: MappedServiceName

    def __init__(self, boto3_name: str):
        self.service_name = MappedServiceName(boto3_name)

    @property
    def namespace(self) -> ServiceModels:
        return ServiceModels(self.service_name)
