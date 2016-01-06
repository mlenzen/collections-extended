bags
====

Bags have constant time inclusion testing but can only contain hashable
elements. See http://en.wikipedia.org/wiki/Multiset

There are two classes provided:

:class:`collections_extended.bag`
  This is a mutable bag
:class:`collections_extended.frozenbag`
  This is a frozen (implements :class:`collections.abc.Hashable`) version of a bag.

Both classes implement :class:`collections.abc.Sized`, :class:`collections.abc.Iterable` and :class:`collections.abc.Container`.

Rich Comparison Methods
-----------------------
Bags comparison methods are implemented when other is a Set. If other isn't
a bag, then it's assumed that it is a set that contains at most one of each
element.

.. testsetup::

  >>> from collections_extended import bag

.. code:: python

  >>> bag() == set()
  True
  >>> bag('a') == set('a')
  True
  >>> bag('ab') == set('a')
  False
  >>> bag('a') == set('ab')
  False
  >>> bag('aa') == set('a')
  False
  >>> bag('aa') == set('ab')
  False
  >>> bag('ac') == set('ab')
  False
  >>> bag('ac') <= set('ab')
  False
  >>> bag('ac') >= set('ab')
  False

Compared to existing similar implementations
--------------------------------------------

collections.Counter
^^^^^^^^^^^^^^^^^^^

Counters don't really behave like "collections" (Sized, Iterable, Container)

.. testsetup::

	>>> from collections import Counter
	>>> from collections_extended import bag

Adding and Removing
"""""""""""""""""""

.. code:: python

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

.. code:: python

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

.. code:: python

	>>> for item in Counter('aaa'): print(item)
	a
	>>> for item in bag('aaa'): print(item)
	a
	a
	a

Compared to Standard Types
--------------------------

bag vs. list
^^^^^^^^^^^^

* Inclusion testing is O(1)
* Adding and removing elements is O(1)
* Cannot add mutable elements
* Elements aren't ordered

bag vs. set
^^^^^^^^^^^

* Can add multiple instances of equal elements

New Methods
-----------

``num_unique_elements``
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
``from_mapping(map: Mapping)``
  Classmethod to create a bag from a Mapping that maps elements to counts.

The following are only for mutable bags (not frozenbags).

- ``pop()``
- ``add(elem)``
- ``discard(elem)``
- ``remove(elem)``
- ``clear()``
