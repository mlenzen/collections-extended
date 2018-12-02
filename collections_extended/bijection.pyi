# Stubs for collections_extended.bijection (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from collections import MutableMapping
from typing import Any, Optional

class bijection(MutableMapping):
    def __init__(self, iterable: Optional[Any] = ..., **kwarg: Any) -> None: ...
    @property
    def inverse(self): ...
    def __len__(self): ...
    def __getitem__(self, key: Any): ...
    def __setitem__(self, key: Any, value: Any) -> None: ...
    def __delitem__(self, key: Any) -> None: ...
    def __iter__(self): ...
    def __contains__(self, key: Any): ...
    def clear(self) -> None: ...
    def copy(self): ...
    def items(self): ...
    def keys(self): ...
    def values(self): ...
    def __eq__(self, other: Any): ...
