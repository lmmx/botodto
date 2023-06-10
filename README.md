# botodto

Pydantic model codegen from AWS OpenAPI schemas generated from the AWS JS/TS SDK (v3)

```py
from botodto.aws.models.v2_norm import build_model as build_v2
from botodto.aws.models.v3 import build_model as build_v3

v2 = build_v2()
v3 = build_v3()
```
