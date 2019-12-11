.. currentmodule:: collections_extended

Collection Factory
==================

`collections_extended` also provides a collection factory.
Combining Python's standard collections with bags and setlists
allows you to create a collection with any combination of
ordered, unique and mutable.

=================================================  =======  =======  ======
Collection                                         Mutable  Ordered  Unique
=================================================  =======  =======  ======
:class:`list`                                            ✔        ✔
:class:`tuple`                                                    ✔
:class:`set`                                             ✔                ✔
:class:`frozenset`                                                        ✔
:class:`bag`                                             ✔
:class:`frozen_bag`
:class:`setlist`                                         ✔        ✔       ✔
:class:`frozensetlist`                                            ✔       ✔
=================================================  =======  =======  ======

API
---

.. autofunction:: collections_extended.collection

.. autoclass:: collections_extended.Collection(Sized, Iterable, Container)

    Collection abstract base class from :mod:`collections.abc` for Python >= 3.6
    and backported to < 3.6
