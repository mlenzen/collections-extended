.. py:currentmodule:: collections_extended

Change Log
==========

2.0.0 - Unreleased
------------------

Breaking Changes
""""""""""""""""

* Drop support for Python 2.7 & 3.4
* When multiplying bags, the cartesian product creates a tuple instead of adding
  the elements.
* bags no longer inherit from Set
  * can no longer compare as equal to Sets
* Rename and expose bag and set base classes
  * `_basebag` -> :class:`Bag`
  * `_basesetlist` -> :class:`SetList`

Added
"""""

* Added :class:`IndexedDict`
* Improve efficiency for large bag operations
* Add :meth:`setlist.swap`
* Add :meth:`bag.count`, :class:`CountsView` & :class:`UniqueElementsView`
* Add :meth:`bag.issubset` and :meth:`issuperset`
* Add support for Python 3.8
* Add :class:`Sentinel`
* Make :class:`MappedRange` a class instead of a namedtuple
* Add change log

Fixed
"""""

Deprecated
""""""""""

Removed
"""""""

1.0.3 - 2019-11-23
------------------

Breaking Changes
""""""""""""""""

* Drop support for Python 2.6 & 3.3

* When multiplying bags, the cartesian product creates a tuple instead of adding
  the elements.
* bags no longer inherit from Set
  * can no longer compare as equal to Sets
* Rename and expose bag and set base classes
  * `_basebag` -> :class:`Bag`
  * `_basesetlist` -> :class:`SetList`

Added
"""""

* Added :class:`IndexedDict`
* Improve efficiency for large bag operations
* Add :meth:`setlist.swap`
* Add :meth:`bag.count`, :class:`CountsView` & :class:`UniqueElementsView`
* Add :meth:`bag.issubset` and :meth:`issuperset`
* Add support for Python 3.8
* Add :class:`Sentinel`
* Make :class:`MappedRange` a class instead of a namedtuple
* Add change log

Fixed
"""""

Deprecated
""""""""""

Removed
"""""""

1.0.2 - 2018-06-30
------------------

1.0.1 - 2018-04-14
------------------

1.0.0 - 2017-10-17
------------------

0.10.1 - 2017-10-20
-------------------

0.10.0 - 2017-10-20
-------------------

0.9.0 - 2017-01-28
------------------

0.8.2 - 2016-10-24
------------------

0.8.1 - 2016-10-24
------------------

0.8.0 - 2016-08-21
------------------

0.7.2 - 2016-08-07
------------------

0.7.1 - 2016-08-07
------------------

0.7.0 - 2016-01-13
------------------

0.6.0 - 2015-10-18
------------------

0.5.2 - 2015-07-09
------------------

0.5.1 - 2015-07-08
------------------

0.5.0 - 2015-07-08
------------------

0.4.0 - 2015-03-29
------------------

0.3.1 - 2015-01-31
------------------

0.3.0 - 2015-01-31
------------------

0.2.0 - 2015-01-20
------------------

Changed name from data-structures to collections-extended

0.1.6 - 2015-01-20
------------------

Deprecated data-structures

0.1.5 - 2015-01-20
------------------

0.1.4 - 2014-05-24
------------------

0.1.3 - 2014-05-24
------------------

0.1.2 - 2009-10-03
------------------

0.1.1 - 2009-10-03
------------------

0.1.0 - 2009-10-01
------------------

Initial release published to PyPi

0.0.0 - 2009-07-14
------------------

Repository created, modules organized in one package.
