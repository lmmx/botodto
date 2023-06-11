from __future__ import annotations

import boto3
import botocore

from ...aws.service_models import ServiceModels
from .service_name_mapping import MappedServiceName

__all__ = ["client"]


class client:
    service_name: MappedServiceName
    base_client: botocore.client.BaseClient

    def __init__(self, boto3_name: str):
        self.service_name = MappedServiceName(boto3_name)
        self.base_client = boto3.client(boto3_name)

    @property
    def namespace(self) -> ServiceModels:
        return ServiceModels(self.service_name)
