bags
----

Bags have constant time inclusion testing but can only contain hashable
elements. See http://en.wikipedia.org/wiki/Multiset

There are two classes provided:

bag
  This is a bag AKA multiset.
frozenbag
  This is a frozen (hashable) version of a bag.

Both classes implement Sized, Iterable and Container while frozenbag also
implement Hashable.

Compared to list
~~~~~~~~~~~~~~~~

* Inclusion testing is O(1)
* Adding and removing elements is O(1)
* Cannot add Mutable elements
* Elements aren't ordered

Compared to set
~~~~~~~~~~~~~~~

* Can add multiple instances of equal elements

New Methods
~~~~~~~~~~~

- ``num_unique_elements()``
    Returns the number of unique elements in the bag. O(1)
- ``unique_elements()``
    Returns a set of all the unique elements in the bag. O(1)
- ``nlargest(n=None)``
    Returns the n most common elements and their counts from most common to
    least.  If n is None then all elements are returned. O(n log n)
- ``copy()``
    Returns a shallow copy of self.  O(self.num_unique_elements())
- ``isdisjoint(other: Iterable)``
    Tests if self is disjoint with any other Iterable.  O(len(other))

The following are only for mutable bags (not frozenbags).

- ``pop()``
- ``add(elem)``
- ``discard(elem)``
- ``remove(elem)``
- ``clear()``
