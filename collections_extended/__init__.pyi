from ._compat import Collection as Collection
from ._version import __version__ as __version__
from .bags import CountsView as CountsView, UniqueElementsView as UniqueElementsView, bag as bag, frozenbag as frozenbag
from .bijection import bijection as bijection
from .indexed_dict import IndexedDict as IndexedDict
from .range_map import MappedRange as MappedRange, RangeMap as RangeMap
from .setlists import frozensetlist as frozensetlist, setlist as setlist
from typing import Any, Optional, Iterable

def collection(
		iterable: Optional[Iterable[Any]] = ...,
		mutable: bool = ...,
		ordered: bool = ...,
		unique: bool = ...,
) -> Collection: ...
