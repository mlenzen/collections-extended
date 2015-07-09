range_map
=========
A RangeMap maps ranges to values. Keys must be hashable and comparable to all
other keys (but not necessarily the same type).

Examples
--------

.. code:: python

	>>> from collections_extended import RangeMap
	>>> us_presidents = RangeMap()
	>>> us_presidents[date(1993, 1, 20):date(2001, 1, 20)] = 'Bill Clinton'
	>>> us_presidents[date(2001, 1, 20):date(2009, 1, 20)] = 'George W. Bush'
	>>> us_presidents[date(2009, 1, 20):] = 'Barack Obama'
	>>> us_presidents[date(1995, 5, 10)]
	'Bill Clinton'
	>>> us_presidents[date(2001, 1, 20)]
	'George W. Bush'
	>>> us_presidents[date(2021, 3, 1)]
	'Barack Obama'
	>>> us_presidents[date(2017, 1, 20):] = 'Someone New'
	>>> us_presidents[date(2021, 3, 1)]
	'Someone New'

Creating RangeMaps
------------------
RangeMaps can be passed a mapping upon creation. Each key, value pair is
interpreted as the start of a range and the mapped value. The end of the range
is the next largest key in the mapping.

RangeMaps can also be created from ``RangeMap.from_iterable(iterable)`` where
the iterable's elements are tuples (start, stop, value). A start or stop key
of None denotes an open range, ie. a start key of None is analgous to -infinity
if the keys are all numbers.

Python 2 vs 3
-------------
Slice notation is not implented for get, set and delete in python 2 and raises
a SyntaxError when used. This is because Python 2 assumes slices are integers
and replaces open slices with 0 and maxint. Instead use ``RangeMap.set``

Implementation
--------------
RangeMaps are backed by lists of the keys, so it's only fast to add/remove to
the end of the list.
