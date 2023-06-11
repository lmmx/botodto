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
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}, 'resourceName': {'target': 'com.amazonaws.sfn#Arn'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}, 'resourceName': {'target': 'com.amazonaws.sfn#Arn'}}
{'message': {'target': 'com.amazonaws.sfn#ErrorMessage'}, 'reason': {'target': 'com.amazonaws.sfn#ValidationExceptionReason', 'traits': {}}}
```
