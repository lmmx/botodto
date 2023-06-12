from __future__ import annotations

import boto3
import botocore

from ...aws.service_models import ServiceModels
from .service_name_mapping import MappedServiceName

__all__ = ["client"]


class client:
    _service_name: MappedServiceName
    _base_client: botocore.client.BaseClient
    _raise_errors: bool

    def __init__(self, boto3_name: str, raise_errors: bool = False):
        self._service_name = MappedServiceName(boto3_name)
        self._base_client = boto3.client(boto3_name)
        self._raise_errors = raise_errors
        self.__init_api_methods__()

    def __init_api_methods__(self) -> None:
        for method_name in self._base_client._PY_TO_OP_NAME:
            wrapped_method = self._wrap_method(getattr(self._base_client, method_name))
            setattr(self, method_name, wrapped_method)

    def _wrap_method(self, method):
        def wrapped_method(*args, **kwargs):
            try:
                result = method(*args, **kwargs)
            except botocore.exceptions.ClientError as exc:
                if self._raise_errors:
                    raise exc
                else:
                    result = exc.response["Error"]
            return result

        return wrapped_method

    @property
    def _namespace(self) -> ServiceModels:
        return ServiceModels(self._service_name)
