# botodto

Pydantic model codegen from AWS OpenAPI schemas generated from the AWS JS/TS SDK (v3)

```py
from botodto.aws.models import build_v2
from botodto.aws.models import build_v3

v2 = build_v2()
v3 = build_v3()

v2_names = [shape.name for shape in v2.shapes]
v3_names = [shape.name for shape in v3.shapes]

assert not set(v2_names).difference(v3_names)

v3_bonus_shapes = [shape for shape in v3.shapes if shape.name not in v2_names]

for shape in v3_bonus_shapes:
    if shape.type == "structure":
        print(shape.members)
```
