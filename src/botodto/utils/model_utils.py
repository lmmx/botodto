from __future__ import annotations

__all__ = ["bundle_obj", "listify_obj"]


def bundle_obj(obj: dict, key_alias: str):
    return [{key_alias: key, **values} for key, values in obj.items()]


def listify_obj(values: dict, target_attr: str, key_alias: str):
    values[target_attr] = bundle_obj(
        obj=values.get(target_attr, {}),
        key_alias=key_alias,
    )
    return values
