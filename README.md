# botodto

Pydantic model codegen from AWS OpenAPI schemas generated from the AWS SDK (botocore)

## Installation

Requires Python 3.9+

```sh
pip install botodto
```

To develop this library see [DEVELOP.md](https://github.com/lmmx/botodto/tree/master/DEVELOP.md)

## Usage

Swap out `boto3.client` for `botodto.client` and all your responses and errors will be ingested as
Pydantic data models.

```py
import botodto

client = botodto.client("stepfunctions")
```

The names of errors are passed in a "Code" key of the JSON response, but are raised to errors as
`botocore.errorfactory` subclasses.

For example, running a request for an invalid ARN gives an error response with a `Code` value of "InvalidArn":

```py
import botodto

client = botodto.client("stepfunctions")
client.list_executions(stateMachineArn="abc")
```
⇣
```py
InvalidArn(__root__={'Message': "Invalid Arn: 'Invalid ARN prefix: abc'"})
```

The response we get is an object (rather than an error being raised), specifically a Pydantic model
of type `botodto.sdk.stepfunctions.InvalidArn`.

Note that this is still a work in progress: the model currently has an `Any`-typed root, which is
not much use at all! However the normal output responses **do** have proper data models,
and the error types will soon get them too by amending the OpenAPI schemas before running DTO model codegen.
