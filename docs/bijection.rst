bijection
=========

Bijections are functions that map keys to unique values, ie.
one-to-one, onto functions. See: https://en.wikipedia.org/wiki/Bijection

`bijection` maintains the inverse mapping on `bijection.inverse` which
is itself an instance of `bijection`.

Examples
--------

.. code-block:: python

	>>> from collections_extended import bijection
	>>> bij = bijection({'a': 1, 'b': 2, 'c': 3})
	>>> bij.inverse[2]
	'b'
	>>> bij['a'] = 2
	>>> bij == bijection({'a': 2, 'c': 3})
	True
	>>> bij.inverse[1] = 'a'
	>>> bij == bijection({'a': 1, 'c': 3})
	True
	>>> bij.inverse.inverse is bij
	True

API
---

.. autoclass:: collections_extended.bijection
