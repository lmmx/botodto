# botodto

Pydantic model codegen from AWS OpenAPI schemas generated from the AWS JS/TS SDK (v3)

## Installation

```sh
pip install botodto
```

To develop this library see [DEVELOP.md](https://github.com/lmmx/botodto/tree/master/DEVELOP.md)

## Usage

```py
import botodto

client = botodto.Client("stepfunctions")
client.namespace.print_v3_bonus_shape_members()
```
⇣
```py
ActivityDoesNotExist         {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
ActivityLimitExceeded        {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
ActivityWorkerLimitExceeded  {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
ExecutionAlreadyExists       {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
ExecutionDoesNotExist        {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
ExecutionLimitExceeded       {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
InvalidArn                   {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
InvalidDefinition            {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
InvalidExecutionInput        {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
InvalidLoggingConfiguration  {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
InvalidName                  {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
InvalidOutput                {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
InvalidToken                 {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
InvalidTracingConfiguration  {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
MissingRequiredParameter     {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
ResourceNotFound             {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}, 'resourceName': {'target': 'com.amazonaws.sfn#Arn'}}
StateMachineAlreadyExists    {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
StateMachineDeleting         {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
StateMachineDoesNotExist     {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
StateMachineLimitExceeded    {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
StateMachineTypeNotSupported {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
TaskDoesNotExist             {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
TaskTimedOut                 {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
TooManyTags                  {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}, 'resourceName': {'target': 'com.amazonaws.sfn#Arn'}}
ValidationException          {'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}, 'reason': {'target': 'com.amazonaws.sfn#ValidationExceptionReason', 'traits': {}}}
```

These names are passed in a "Code" key of the JSON response, but are raised to errors as
`botocore.errorfactory` subclasses.

For example, here I ran a request for an invalid ARN:

```py
import boto3
import botocore

client = boto3.client("stepfunctions")

try:
    response = client.describe_state_machine(stateMachineArn="abc")
except botocore.exceptions.ClientError as exc:
    error = exc.response["Error"]
```

The error in this case is:

```py
{'Code': 'InvalidArn',
 'Message': "Invalid Arn: 'Invalid Arn prefix: abc'"}
```

We can use Pydantic data models of the polymorphic value of the 'Code' key here to distinguish
error types for operations whose errors share the same basic format
(`{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}` above).
