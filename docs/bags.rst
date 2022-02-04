.. py:currentmodule:: collections_extended

bags (Multisets)
================

Bags are a multiset_ implementation for Python.
Currently, bags have constant time inclusion testing but can only contain
hashable elements due to the implementation.

.. _multiset: http://en.wikipedia.org/wiki/Multiset

There are three classes provided:

:class:`Bag`
  An abstract base class for bags.
:class:`bag`
  A mutable (unhashable) `Bag`.
:class:`frozenbag`
  An immutable (implements :class:`collections.abc.Hashable`) `Bag`.

The `Bag` base class implements :class:`collections.abc.Sized`,
:class:`collections.abc.Iterable` and :class:`collections.abc.Container`
as well as :class:`collections.abc.Collection` starting in Python
3.6 and the polyfilled :class:`Collection` for Python < 3.6.

Set Operations
--------------
`Bags` use python operators for multiset operations:

* `__add__` (`a + b`): The sum of two multisets
* `__sub__` (`a - b`): The difference between a and b
* `__and__` (`a & b`): The intersection of a and b
* `__or__` (`a | b`): The union of a and b
* `__xor__` (`a ^ b`): The symmetric difference between a and b

:class:`bag` has the equivalent in-place operators defined.

Comparison Methods
------------------
`Bags` are comparable only to other `Bags`.
Ordering comparisons are done setwise.

.. testsetup::

	>>> from collections_extended import bag

.. code-block:: python

	>>> bag('ac') <= bag('ab')
	False
	>>> bag('ac') >= bag('ab')
	False
	>>> bag('a') <= bag('a') < bag('aa')
	True
	>>> bag('aa') <= bag('a')
	False

Compared to existing similar implementations
--------------------------------------------

collections.Counter
^^^^^^^^^^^^^^^^^^^

Counters don't really behave like Collections - Sized, Iterable, Containers

.. testsetup::

	>>> from collections import Counter
	>>> from collections_extended import bag

Adding and Removing
"""""""""""""""""""

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

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

These are `bag` methods that are not implementing an abstract method from a
standard Python ABC.

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
``issubset(other: Iterable)``
	Tests if self is a subset of another Iterable.
``issuperset(other: Iterable)``
	Tests if self is a superset of another Iterable.
``from_mapping(map: Mapping)``
	Classmethod to create a bag from a Mapping that maps elements to counts.

The following are only for mutable bags (not frozenbags).

- ``pop()``
- ``add(elem)``
- ``discard(elem)``
- ``remove(elem)``
- ``clear()``

API
---

Bag
^^^

.. autoclass:: Bag

bag
^^^

.. autoclass:: bag

frozenbag
^^^^^^^^^

.. autoclass:: frozenbag

Views
^^^^^

.. autoclass:: CountsView
   :no-undoc-members:

.. autoclass:: UniqueElementsView
   :no-undoc-members:
