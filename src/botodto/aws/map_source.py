"""
We will need a map from boto3 to v2 names.

As an initial proof of concept, both will simply be a dict of 1 known mapping.
"""

__all__ = ["v2_to_v3", "boto3_to_js_v2"]

boto3_to_js_v2 = {"stepfunctions": "states"}

v2_to_v3 = {"states": "sfn"}
