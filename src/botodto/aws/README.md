# AWS service schema data handling

## Problem statement

1. OpenAPI schemas for AWS services are available from the OpenAPI Directory but are missing exceptions.
   The SDK schemas that it uses come from the JS v2 SDK, which is identical to the botocore SDK
   schemas (except in botocore there are exceptions). We can just swap out the JS SDK source for botocore.

2. Pydantic model code can be generated from OpenAPI schemas using the `datamodel-code-generator` package.

3. The `boto3` library ingests/outputs JSON objects with no awareness of the underlying service schema,
   Pydantic models representing the services' data models eliminate manual handling at API call points,
   give model types semantic interpretation, avoid need for manually writing custom container
   classes for these standard formats, and reduce the code smell of 'primitive obsession' (`dict` overuse).

  - e.g. specific errors, but unclear if possible by this approach

4. The `boto3` library can be wrapped at the client level, and operations mapped to Pydantic models
   so as to parse both calls (inputs) and responses (outputs).

## Solution

- Wrap `boto3` so that the `__getattr__` calls which produce calls to any name in the `_PY_TO_OP` enum of
  API operations is wrapped by the appropriate Pydantic model.

- Produce Pydantic models by `datamodel-code-generator` on the OpenAPI schema derived from the botocore SDK schemas

- Supplement the Pydantic models with exception types.
