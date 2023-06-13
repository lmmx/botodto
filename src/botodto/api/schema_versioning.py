from enum import Enum

__all__ = ["SchemaVersion"]


class SchemaVersion(Enum):
    BOTO3 = "py"
    JS_V2 = "v2"
    JS_V3 = "v3"
