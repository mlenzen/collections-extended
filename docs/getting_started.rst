Getting Started
===============

Installation
------------

``pip install collections-extended``

Usage
-----
  ``from collections_extended import bag, frozenbag, setlist, frozensetlist, bijection, RangeMap``

Examples
--------

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
