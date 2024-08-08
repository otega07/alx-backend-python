#!/usr/bin/env python3
"""Type-annotated function to_kv that takes
a string k and an int OR float v as
arguments and returns a tuple.
The first element of the tuple is the string k.
The second element is the square of the
int OR float v and should be annotated
as a float."""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Return a tuple with the string k and
    the square of the int OR float v."""
    return (k, v * v)
