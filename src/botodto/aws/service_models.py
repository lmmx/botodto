from pydantic import BaseModel

from ..api.client.service_name_mapping import MappedServiceName
from .models import build_v2, build_v3

__all__ = ["ServiceModels"]


class ServiceModels:
    def __init__(self, service_name: MappedServiceName):
        if service_name.boto3 == "stepfunctions":
            self.v2 = build_v2()
            self.v3 = build_v3()
            assert not set(self.v2_names).difference(self.v3_names)
        else:
            raise NotImplementedError("Only AWS Step Functions API implemented so far")

    @staticmethod
    def get_shape_names(model: BaseModel) -> list[str]:
        return [shape.name for shape in model.shapes]

    @property
    def v2_names(self) -> list[str]:
        return self.get_shape_names(model=self.v2)

    @property
    def v3_names(self) -> list[str]:
        return self.get_shape_names(model=self.v3)

    @property
    def v3_bonus_shapes(self) -> list[BaseModel]:  # Not a good annotation
        return [shape for shape in self.v3.shapes if shape.name not in self.v2_names]

    def print_v3_bonus_shape_members(self) -> None:
        for shape in self.v3_bonus_shapes:
            if shape.type == "structure":
                print(
                    f'{shape.name:29}{shape.members.dict(exclude_unset=True)["__root__"]}'
                )
