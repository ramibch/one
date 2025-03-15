from collections.abc import Iterable
from typing import Any


def get_nested_attr(obj: Any, attr_list: Iterable):
    """
    Get a nested attribute of a object.

    Example (the following statments gives us the same result):

    > final_attr = get_nested_attr(obj, ["foo", "bar"])
    > final_attr = obj.foo.bar

    """
    for attr in attr_list:
        obj = getattr(obj, attr)
    return obj
