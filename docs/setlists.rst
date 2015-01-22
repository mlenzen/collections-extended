setlist
=======

A ``setlist`` is an ordered, indexed collection with unique elements.  The class
implements Sequence and Set and should be able to be used as a drop in
replacement for a set or list of you want to add the add an additional
constraint of ordering or uniqueness.  It it more than just an ordered Set
in that the elements are accessible by index (ie. not just a linked set).

However, ``setlist``'s are not comparable like sets or lists. Equality
testing still works, but ``setlist(('a', 'c')) < setlist(('a', 'b'))`` does not
because we'd have to choose to compare by order or by set comparison.

Differences from list
---------------------

* Inclusion testing is O(1)
* Adding an element that is already present does nothing

Differences from set
--------------------

* Elements are ordered and accessible by index
* Adding an element is O(n) as opposed to O(1)

New Methods
-----------
Aside from the methods expected from Sequence and Set, this provides:
- ``setlist.shuffle(random=None)``
  Because random.shuffle(setlist) doesn't work, this is provided to do the same.

Quirks
------
* Swapping elements, eg. `sl[0], sl[1] = sl[1], sl[0]`, doesn't work because
  it is implemented by first inserting one element then the other. But since
  the first element it tries to insert is still in the setlist, nothing happens.
  This causes random.shuffle not to work on a setlist.

