from __future__ import annotations

from importlib import import_module
from typing import Callable, TypeVar

import boto3
import botocore
from pydantic import BaseModel

from ...aws.service_models import ServiceModels
from ..service_name_mapping import MappedServiceName

__all__ = ["client"]

T = TypeVar("T", bound=BaseModel)


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

    def _get_model(self, class_name: str) -> T:
        """
        Import the generated SDK module with the client's service name and get the model
        with the given name. The import is cached: after the first call there's no overhead.
        """
        module = import_module(f".sdk.{self._service_name.boto3}", package="botodto")
        return getattr(module, class_name)

    def _wrap_method(self, method):
        def wrapped_method(*args, **kwargs):
            try:
                result = method(*args, **kwargs)
                operation_name = self._base_client._PY_TO_OP_NAME[method]
                model = self._get_model(f"{operation_name}Output")
            except botocore.exceptions.ClientError as exc:
                if self._raise_errors:
                    raise exc
                else:
                    result = exc.response["Error"]
                    operation_name = result.pop("Code")
                    model = self._get_model(operation_name)
            return model.parse_obj(result)

        return wrapped_method

    @property
    def _namespace(self) -> ServiceModels:
        return ServiceModels(self._service_name)
