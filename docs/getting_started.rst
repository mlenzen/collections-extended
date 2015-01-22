Getting Started
===============

Installation
------------

``pip install collections-extended``

Usage
-----
  ``from collections_extended import bag, frozenbag, setlist, frozensetlist``

Examples
--------

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
	>>> from collections_extended import bag
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
