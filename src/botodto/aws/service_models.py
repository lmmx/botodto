from pydantic import BaseModel

from ..api.service_name_mapping import MappedServiceName
from .models import build_botocore

__all__ = ["ServiceModels"]


class ServiceModels:
    def __init__(self, service_name: MappedServiceName):
        if service_name.boto3 in MappedServiceName._supported_services:
            self.built = build_botocore(service_name=service_name)
        else:
            raise NotImplementedError("Only AWS Step Functions API implemented so far")

    @staticmethod
    def get_shape_names(model: BaseModel) -> list[str]:
        return [shape.name for shape in model.shapes]

    @property
    def botocore_names(self) -> list[str]:
        return self.get_shape_names(model=self.built)

    def print_error_shape_members(self) -> None:
        for shape in self.built.shapes:
            if shape.type == "structure":
                print(
                    f'{shape.name:29}{shape.members.dict(exclude_unset=True)["__root__"]}',
                )
