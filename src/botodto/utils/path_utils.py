from pathlib import Path

from .. import sdk
from ..data import aws

__all__ = ["data_dir", "aws_oa_dir"]

data_dir = Path(aws.__path__[0])
aws_oa_dir = data_dir / "openapi_directory"

sdk_dir = Path(sdk.__path__[0])
