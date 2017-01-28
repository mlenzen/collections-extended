README
######

.. image:: https://travis-ci.org/mlenzen/collections-extended.svg?branch=master
	:target: https://travis-ci.org/mlenzen/collections-extended
	:alt: Build Status


.. image:: https://coveralls.io/repos/mlenzen/collections-extended/badge.svg?branch=master
	:target: https://coveralls.io/r/mlenzen/collections-extended?branch=master
	:alt: Coverage

Documentation: http://collections-extended.lenzm.net/

GitHub: https://github.com/mlenzen/collections-extended

PyPI: https://pypi.python.org/pypi/collections-extended

Overview
========

``collections_extended`` is a Python module providing
a ``bag`` class, AKA **multiset**,
a ``setlist`` class, which is a **unique list** or **ordered set**,
a ``bijection`` class and ``RangeMap`` which is a mapping from ranges to values.
There are also frozen (hashable) varieties of bags and setlists.

Tested against Python 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, PyPy & PyPy3.

Python 3.1 and 3.2 are unsupported by coverage so they are not included in
Travis CI.

Getting Started
===============

.. code-block:: python

	>>> from collections_extended import bag, setlist, bijection, RangeMap
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

Installation
============

``pip install collections-extended``

Usage
=====
	``from collections_extended import bag, frozenbag, setlist, frozensetlist, bijection``

Classes
=======
There are six new classes provided:

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

:Author: Michael Lenzen
:Copyright: 2017 Michael Lenzen
:License: Apache License, Version 2.0
:Project Homepage: https://github.com/mlenzen/collections-extended
