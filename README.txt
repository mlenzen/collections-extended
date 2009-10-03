:Author: Michael Lenzen
:Copyright: 2009 Michael Lenzen

Overview
========

A few collections/data structures that I think should be part of python. Python3 that is, I don't plan on supporting old versions. Maybe 2.7, I'm not sure what the deal with that is.

For now, this package includes one module - `collections_extended`.  This module
extends the built-in collections module to include a `bag` class, AKA multiset, and
a `setlist` class, which is a list of unique elements or an ordered set depending on
how you look at it.  There are also frozen (hashable) varieties of each included.
Finally, all collections are abstracted into one Collection abstract base class and
a Collection factory is provided where you can create a Collection by specifying
the properties unique, ordered and mutable.

Project Homepage:
http://code.google.com/p/python-data-structures/

Documentation:
http://code.google.com/p/python-data-structures/wiki/DocCollectionsExtended

Usage
=====

``import collections_extended as collections``

or

``from collections_extended import *``
