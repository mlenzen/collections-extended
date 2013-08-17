=============================
python-data-structures README
=============================

:Author: Michael Lenzen
:Copyright: 2013 Michael Lenzen
:Project Homepage: https://github.com/mlenzen/python-data-structures

.. contents::

Overview
========

A few collections/data structures that I think should be part of python. 
Python3 that is, I don't plan on supporting old versions. Maybe 2.7, I'm not
sure what the deal with that is.

For now, this package includes one module - `collections_extended`.  This 
module extends the built-in collections module to include a `bag` class, 
AKA multiset, and a `setlist` class, which is a list of unique elements or 
an ordered set depending on how you look at it.  There are also frozen 
(hashable) varieties of each included.  Finally, all collections are 
abstracted into one Collection abstract base class and a Collection factory
is provided where you can create a Collection by specifying the properties 
unique, ordered and mutable.


Usage
=====
To replace the built in collections module do:
  ``import collections_extended as collections``

To get the basic data structures:
  ``from collections_extended import bag, frozenbag, setlist, frozensetlist``

Or you can simply:
  ``from collections_extended import *``

Classes
=======
There are four new classes provided:

bag
  This is a bag AKA multiset.  See http://en.wikipedia.org/wiki/Multiset
frozenbag
  This is a frozen (hashable) version of a bag.
setlist
  An ordered set or a list of unique elements depending on how you look at it.
frozensetlist
  This is a frozen (hashable) version of a setlist.

bag
---
Bags have constant time inclusion testing.

- ``count(elem)``
    Returns the count of elem in the bag.  O(1)
- ``num_unique_elements()``
    Returns the number of unique elements in the bag. O(1)
- ``unique_elements()``
    Returns a set of all the unique elements in the bag. O(1)
- ``nlargest(n=None)``
    Returns the n most common elements and their counts from most common to least.  If n is None then all elements are returned. O(n log n)
- ``copy()``
    Returns a shallow copy of self.  O(self.num_unique_elements())
- ``cardinality()``
    Returns the cardinality of this bag.  Same as ``len(self)``.  O(1)
- ``underlying_set()``
    Returns the underlying set.  Same as ``self.unique_elements()``.
- ``multiplicity(elem)``
    Same as ``self.count(elem)``
- ``isdisjoint(other: Iterable)``
    Tests if self is disjoint with any other Iterable.  O(len(other))

The following are only for mutable bags (not frozenbags).

- ``pop()``
- ``add(elem)``
- ``discard(elem)``
- ``remove(elem)``
- ``clear()``

setlist
-------


Collection Factory
==================
A Collection factory is provided where you can specify whether you want the Collection returned to be mutable, have unique elements and/or be ordered.  If an Iterable object is passed the Collection will be filled from it, otherwise it will be empty.

``collection(it: Iterable = None, mutable=True, unique=False, ordered=False)``
