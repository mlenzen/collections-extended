bags
====

Bags have constant time inclusion testing but can only contain hashable
elements. See http://en.wikipedia.org/wiki/Multiset

There are two classes provided:

bag :py:class:`collections_extended.bag`
  This is a bag AKA multiset (implements ``Mutable``)
frozenbag :py:class:`collections_extended.frozenbag`
  This is a frozen (implements ``Hashable``) version of a bag.

Both classes implement ``Sized``, ``Iterable`` and ``Container``.

Compared to existing similar implements
---------------------------------------

collections.Counter
^^^^^^^^^^^^^^^^^^^

Counters don't really behave like "collections" (Sized, Iterable, Container)

.. testsetup::

	>>> from collections import Counter
	>>> from collections_extended import bag

Adding and Removing
"""""""""""""""""""

.. doctest::

	>>> c = Counter()
	>>> c['a'] += 1
	>>> c['a'] -= 1
	>>> 'a' in c
	True
	>>> b = bag()
	>>> b.add('a')
	>>> 'a' in b
	True
	>>> b.remove('a')
	>>> 'a' in b
	False

``len``
"""""""

.. doctest::

	>>> c = Counter()
	>>> c['a'] += 1
	>>> len(c)
	1
	>>> c['a'] -= 1
	>>> len(c)
	1
	>>> c['a'] += 2
	>>> len(c)
	1
	>>> len(Counter('aaabbc'))
	3
	>>> b = bag()
	>>> b.add('a')
	>>> len(b)
	1
	>>> b.remove('a')
	>>> len(b)
	0
	>>> len(bag('aaabbc'))
	6

Iterating
"""""""""

.. doctest::

	>>> for item in Counter('aaa'): print(item)
	a
	>>> for item in bag('aaa'): print(item)
	a
	a
	a

Compared to Standard Types
--------------------------

list
^^^^

* Inclusion testing is O(1)
* Adding and removing elements is O(1)
* Cannot add Mutable elements
* Elements aren't ordered

set
^^^

* Can add multiple instances of equal elements

New Methods
-----------

``num_unique_elements()``
	Returns the number of unique elements in the bag. O(1)
``unique_elements()``
	Returns a set of all the unique elements in the bag. O(1)
``nlargest(n=None)``
	Returns the n most common elements and their counts from most common to
	least.  If n is None then all elements are returned. O(n log n)
``copy()``
	Returns a shallow copy of self.  O(self.num_unique_elements())
``isdisjoint(other: Iterable)``
	Tests if self is disjoint with any other Iterable.  O(len(other))

The following are only for mutable bags (not frozenbags).

- ``pop()``
- ``add(elem)``
- ``discard(elem)``
- ``remove(elem)``
- ``clear()``
