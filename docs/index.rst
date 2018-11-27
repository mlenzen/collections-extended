collections_extended's documentation
====================================

``collections_extended`` is a Python module providing
 - a ``bag`` class, AKA **multiset**,
 - a ``setlist`` class, which is a **unique list** or **ordered set**,
 - a ``bijection`` class,
 - a ``RangeMap`` which is a mapping from ranges to values, and
 - a ``IndexedDict`` class.

There are also frozen (hashable) varieties of bags and setlists.

The ABC :class:`collections.abc.Collection` is backported to Python versions < 3.6

It is `tested against`_ Python 2.7, 3.3, 3.4, 3.5, 3.6, 3.7, PyPy & PyPy3.

Contents:

.. toctree::
	:maxdepth: 3

	getting_started
	setlists
	bags
	range_map
	bijection
	indexed_dict
	api
	contributing

Other Packages of Interest
==========================

- http://stutzbachenterprises.com/blist/ - b+ trees,
- https://bitbucket.org/mozman/bintrees - Binary search trees
- https://bidict.readthedocs.org/en/master/ - bijections

:Author: Michael Lenzen
:Copyright: 2018 Michael Lenzen
:License: Apache License, Version 2.0

.. _`tested against`: https://travis-ci.org/mlenzen/collections-extended
