README
######

.. image:: https://coveralls.io/repos/github/mlenzen/collections-extended/badge.svg?branch=master
	:target: https://coveralls.io/github/mlenzen/collections-extended?branch=master
	:alt: Coverage


.. image:: https://pepy.tech/badge/collections-extended/week
	:target: https://pepy.tech/project/collections-extended/
	:alt: Downloads


Documentation:
	https://collections-extended.lenzm.net/
GitHub:
	https://github.com/mlenzen/collections-extended
PyPI:
	https://pypi.python.org/pypi/collections-extended

Overview
========

``collections_extended`` is a pure Python module with no dependencies providing
extra collections. The new collections include
bags AKA **multisets**,
setlists AKA **unique lists** or **ordered sets**,
a ``bijection``,
a ``RangeMap`` which is a mapping from ranges to values, and
an ``IndexedDict`` class.
There are also frozen (hashable) varieties of bags and setlists.

Compatible with and tested against CPython 3.7, 3.8, 3.9, 3.10, 3.11, PyPy3.6, PyPy3.7 & PyPy3.8.

Getting Started
===============

.. code-block:: python

	>>> from collections_extended import bag, setlist, bijection, RangeMap, IndexedDict
	>>> from datetime import date
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
	>>> sl.insert(1, 'd')  # inserting an element already in raises a ValueError
	Traceback (most recent call last):
	...
		raise ValueError
	ValueError
	>>> sl.index('d')
	4

	>>> bij = bijection({'a': 1, 'b': 2, 'c': 3})
	>>> bij.inverse[2]
	'b'
	>>> bij['a'] = 2
	>>> bij == bijection({'a': 2, 'c': 3})
	True
	>>> bij.inverse[1] = 'a'
	>>> bij == bijection({'a': 1, 'c': 3})
	True

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

	>>> idict = IndexedDict()
	>>> idict['a'] = "A"
	>>> idict['b'] = "B"
	>>> idict['c'] = "C"
	>>> idict.get(key='a')
	'A'
	>>> idict.get(index=2)
	'C'
	>>> idict.index('b')
	1

Installation
============

``pip install collections-extended``

Usage
=====
	``from collections_extended import bag, frozenbag, setlist, frozensetlist, bijection``

New Collections
===============

There are seven new collections provided:

Bags
----
bag
	This is a bag AKA multiset.
frozenbag
	This is a frozen (hashable) version of a bag.

Setlists
--------
setlist
	An ordered set or a list of unique elements depending on how you look at it.
frozensetlist
	This is a frozen (hashable) version of a setlist.

Mappings
--------
bijection
	A one-to-one mapping.
RangeMap
	A mapping from ranges (of numbers/dates/etc)
IndexedDict
	A mapping that keeps insertion order and allows access by index.

Python 2
--------

The package no longer supports Python 2. The last version to support
Python 2.7, 3.4 & 3.5 was 1.0. No new feature releases will be done for 1.x but
any significant bugs that come up may be fixed.

:Author: Michael Lenzen
:Copyright: 2022 Michael Lenzen
:License: Apache License, Version 2.0
:Project Homepage: https://github.com/mlenzen/collections-extended
