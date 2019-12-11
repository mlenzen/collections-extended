range_map
=========
A RangeMap maps ranges to values. Keys must be hashable and comparable to all
other keys (but not necessarily the same type). Each range `a:b` maps all values
`a <= x < b` so it includes `a` but not `b`.

Examples
--------

.. code-block:: python

    >>> from collections_extended import RangeMap
    >>> from datetime import date
    >>> version = RangeMap()
    >>> version[date(2017, 10, 20): date(2017, 10, 27)] = '0.10.1'
    >>> version[date(2017, 10, 27): date(2018, 2, 14)] = '1.0.0'
    >>> version[date(2018, 2, 14):] = '1.0.1'
    >>> version[date(2017, 10, 24)]
    '0.10.1'
    >>> version[date(2018, 7, 1)]
    '1.0.1'
    >>> version[date(2018, 6, 30):] = '1.0.2'
    >>> version[date(2018, 7, 1)]
    '1.0.2'

Creating RangeMaps
------------------
RangeMaps can be passed a mapping upon creation. Each key, value pair is
interpreted as the start of a range and the mapped value. The end of the range
is the next largest key in the mapping.

RangeMaps can also be created from ``RangeMap.from_iterable(iterable)`` where
the iterable's elements are tuples (start, stop, value). A start or stop key
of None denotes an open range, ie. a start key of None is analgous to -infinity
if the keys are all numbers.

Quirks
------

Python 2 vs 3
~~~~~~~~~~~~~
Slice notation is not implemented for get, set and delete in python 2 and raises
a SyntaxError when used. This is because Python 2 assumes slices are integers
and replaces open slices with 0 and maxint. Instead use ``RangeMap.set``,
``RangeMap.delete`` and ``RangeMap.get_range``.

PyPy
~~~~
pypy (not pypy3) cannot accept non-ints in __getitem__ so RangeMap[1.5:3]
doesn't work.

Implementation
--------------
RangeMaps are backed by lists of the keys, so it's only fast to add/remove the
greatest values in the range (the end of the list).

API
---

.. autoclass:: collections_extended.RangeMap

.. autoclass:: collections_extended.MappedRange
    :no-undoc-members:
