collections_extended's documentation
====================================

``collections_extended`` is a Python module providing
a ``bag`` class, AKA **multiset**,
a ``setlist`` class, which is a **unique list** or **ordered set**,
a ``bijection`` class and ``RangeMap`` which is a mapping from ranges to values.
There are also frozen (hashable) varieties of bags and setlists.

It is `tested against`_ Python 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, PyPy & PyPy3.

Contents:

.. toctree::
	:maxdepth: 3

	getting_started
	setlists
	bags
	range_map
	api
	contributing

Other Packages of Interest
==========================

- http://stutzbachenterprises.com/blist/ - b+ trees,
- https://bitbucket.org/mozman/bintrees - Binary search trees
- https://bidict.readthedocs.org/en/master/ - bijections

:Author: Michael Lenzen
:Copyright: 2016 Michael Lenzen
:License: Apache License, Version 2.0

.. _`tested against`: https://travis-ci.org/mlenzen/collections-extended
