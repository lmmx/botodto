from __future__ import annotations

import json

from ..api.schema_versioning import SchemaVersion
from ..api.service_name_mapping import MappedServiceName
from .path_utils import data_dir

__all__ = ["ingest_json", "ingest_json_legacy"]


def ingest_json(service_name: MappedServiceName, version: SchemaVersion) -> dict | list:
    ver = version.value
    if ver == "v2":
        filename = "v2-normal.json"
    elif ver == "v3":
        filename = "v3-smithy.json"
    service_dir = data_dir / service_name.boto3
    path = service_dir / filename
    return json.loads(path.read_text())


def ingest_json_legacy(filename) -> dict | list:
    path = data_dir / "stepfunctions" / filename
    return json.loads(path.read_text())
