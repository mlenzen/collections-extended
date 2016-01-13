setlist
=======

A ``setlist`` is an ordered, indexed
collection with unique elements.	It it more than just an **ordered Set**
in that the elements are accessible by index (ie. not just a linked set).

However, ``setlist``'s are not comparable like sets or lists. Equality
testing still works, but ``setlist(('a', 'c')) < setlist(('a', 'b'))`` does not
because we'd have to choose to compare by order or by set comparison.

There are two classes provided:

:class:`collections_extended.setlist`
	This is a mutable setlist
:class:`collections_extended.frozensetlist`
	This is a frozen (implements :class:`collections.abc.Hashable`) version of a setlist.

Both classes implement :class:`collections.abc.Sequence`, :class:`collections.abc.Set`

Examples
--------

.. code-block:: python

	>>> from collections_extended import setlist
	>>> import string
	>>> sl = setlist(string.ascii_lowercase)
	>>> sl
	setlist(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'))
	>>> sl[3]
	'd'
	>>> sl[-1]
	'z'
	>>> 'r' in sl	# testing for inclusion is fast
	True
	>>> sl.index('m')	# so is finding the index of an element
	12
	>>> sl.insert(1, 'd')	# inserting an element already in raises a ValueError
	Traceback (most recent call last):
	...
		raise ValueError
	ValueError
	>>> sl.index('d')
	3


Compared to existing similar implementations
--------------------------------------------

Most implementations I've see are ordered sets where items are not accessible
by index.

Compared to Standard Types
--------------------------

setlist vs. list
^^^^^^^^^^^^^^^^

* Inclusion testing is O(1)
* Finding an element is O(1)
* Adding an element that is already present raises a ValueError

setlist vs. set
^^^^^^^^^^^^^^^

* Elements are ordered and accessible by index
* Adding an element is as slow as adding to a list
	* Amortized O(n) for arbitrary insertions
	* O(1) for appending

New Methods
-----------
Aside from the methods expected from Sequence and Set, this provides:
- ``setlist.shuffle(random=None)`` Because random.shuffle(setlist) doesn't work, this is provided to do the same.

ValueErrors
-----------
setlists will raise ``ValueError`` when appending an already present element or
removing a non-existent element. However, the methods inherited from ``Set``
(``add`` and ``discard``) are silent in the same circumstances. This matches the
behavior of ``list`` and ``set``.

The setlist constructor does not raise ``ValueError`` on duplicate values
because I had to choose one or the other and I have code assuming it doesn't.

Quirks
------
* Swapping elements, eg. `sl[0], sl[1] = sl[1], sl[0]`, doesn't work because
	it is implemented by first setting one element then the other. But since
	the first element it tries to set is still in the setlist, nothing happens.
	This causes random.shuffle not to work on a setlist.
