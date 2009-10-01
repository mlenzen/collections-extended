Python Data Structures
----------------------

Project Homepage:
http://code.google.com/p/python-data-structures/

For now, this package includes one module - `collections_extended`.  This module
extends the built-in collections module to include a `bag` class, AKA multiset, and
a `setlist` class, which is a list of unique elements or an ordered set depending on
how you look at it.  There are also frozen (hashable) varieties of each included.
Finally, all collections are abstracted into one Collection abstract base class and
a Collection factory is provided where you can create a Collection by specifying
the properties unique, ordered and mutable.

See http://code.google.com/p/python-data-structures/wiki/CollectionsExtendedProposal
for more.

