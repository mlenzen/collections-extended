collections_extended README
###########################

.. image:: https://travis-ci.org/mlenzen/python-data-structures.svg?branch=master
  :target: https://travis-ci.org/mlenzen/python-data-structures
  :alt: Build Status

.. contents::

Getting Started
===============

.. code:: python

   >>> from collections_extended import bag, setlist
   >>> b = bag('abracadabra')
   >>> b.count('a')
   5
   >>> b.remove('a')
   >>> b.count('a')
   4
   >>> 'a' in b
   True
   >>> b.count('d')
   1
   >>> b.remove('d')
   >>> b.count('d')
   0
   >>> 'd' in b
   False

   >>> sl = setlist('abracadabra')
   >>> sl
   setlist(('a', 'b', 'r', 'c', 'd'))
   >>> sl[3]
   'c'
   >>> sl[-1]
   'd'
   >>> 'r' in sl  # testing for inclusion is fast
   True
   >>> sl.index('d')  # so is finding the index of an element
   4
   >>> sl.insert('d', 1)  # inserting an element already in the setlist does nothing
   >>> sl.index('d')
   4
 
Installation
============

``pip install data-structures``

Overview
========

This package includes one module - ``collections_extended``.  This 
module extends the built-in collections module to include a ``bag`` class, 
AKA multiset, and a ``setlist`` class, which is a list of unique elements /
ordered set.  There are also frozen (hashable) varieties of each included.


Usage
=====
  ``from collections_extended import bag, frozenbag, setlist, frozensetlist``

Classes
=======
There are four new classes provided:

bag
  This is a bag AKA multiset. 
frozenbag
  This is a frozen (hashable) version of a bag.
setlist
  An ordered set or a list of unique elements depending on how you look at it.
frozensetlist
  This is a frozen (hashable) version of a setlist.

bag
---
Bags have constant time inclusion testing but can only contain hashable elements. See http://en.wikipedia.org/wiki/Multiset

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
A ``setlist`` is an ordered, indexed collection with unique elements.  The class
implements Sequence and Set and should be able to be used as a drop in
replacement for a set or list of you want to add the add an additional
constraint of ordering or uniqueness.  It it more than just an ordered Set
in that the elements are accessible by index (ie. not just a linked set).

However, ``setlist``'s are not comparable like sets or lists. Equality
testing still works, but ``setlist(('a', 'c')) < setlist(('a', 'b'))`` does not
because we'd have to choose to compare by order or by set comparison.

Differences from list
~~~~~~~~~~~~~~~~~~~~~

* Inclusion testing is O(1)
* Adding an element that is already present does nothing

Differences from set
~~~~~~~~~~~~~~~~~~~~

* Elements are ordered and accessible by index
* Adding an element is O(n) as opposed to O(1)


Collection Factory
==================
A Collection factory is provided where you can specify whether you want the
Collection returned to be mutable, have unique elements and/or be ordered.  If
an Iterable object is passed the Collection will be filled from it, otherwise
it will be empty.

``collection(it = None, mutable=True, unique=False, ordered=False)``

:Author: Michael Lenzen
:Copyright: 2014 Michael Lenzen
:License: Apache License, Version 2.0
:Project Homepage: https://github.com/mlenzen/python-data-structures
