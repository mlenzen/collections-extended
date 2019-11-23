Sentinel
========

This is a small class that improves upon using a plain object
as a sentinel for function arguments when None is a valid
parameter and can't be used as the default. The improvements
vs. a plain object are:

* Better ``__str__`` and ``__repr__`` for better messages in
logs and stacktraces. Instead of something like
``'<object object at 0x7ffb4d50e830>'`` you get ``'<not_set>'``
* Sentinels are picklable

See: https://www.wikiwand.com/en/Sentinel_value
Inspired by: https://pypi.org/project/sentinels/

.. autoclass:: collections_extended.sentinel
