IndexedDicts
============

IndexedDict is an ordered mapping whose elements can be accessed using index,
in addition to key. The interface is mostly a generalization of
:class:`collections.OrderedDict`.

Differences from OrderedDict
----------------------------

Methods ``get``, ``pop`` and ``move_to_end`` have a different signature from
OrderedDict, allowing exactly one of ``index`` or ``key`` argument to be used.
This causes the IndexedDict to not be a drop in replacement to OrderedDict.

New Methods
^^^^^^^^^^^

``fast_pop``
	Remove an item with given key and value from the IndexedDict by first
	swapping the item to the last position and then removing it.
	Returns tuple of ``(popped_value, new_moved_index, moved_key, moved_value)``.
	Time complexity of this operation is O(1).
``index``
	Return index of a record with given key.
``key``
	Return key of a record at given index.

Time Complexity
---------------
IndexedDict generally combines time complexity of dict and list.
Indexed lookups cost list's O(1), keyed lookups cost average case O(1) and worst
case O(n) of dict.
Deleting an element has a time complexity of O(1) if it is the last added one,
or O(n) in general, in addition to the lookup cost.

API
---

.. autoclass:: collections_extended.IndexedDict
