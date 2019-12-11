import pytest

from collections_extended.indexed_dict import IndexedDict


def assert_internal_state(self):
    """Asserts that the inner state of the data structure is consistent.
    Returns True, so it can be used in an assert expression itself."""

    assert len(self._dict) == len(self._list)
    for k, (i, v) in self._dict.items():  # noqa
        k2, v2 = self._list[i]
        assert k2 == k
        assert v2 is v


def test_empty_construction():
    d = IndexedDict()
    assert list(d) == []
    assert_internal_state(d)


def test_dict_construction():
    d = IndexedDict({1: 2, 3: 4})
    assert set(d) == {1, 3}  # Not necessarily ordered for python < 3.6
    assert_internal_state(d)


def test_kwargs_construction():
    d = IndexedDict(a=1, b=2, c=3)
    assert set(d) == set("abc")  # Not necessarily ordered for python < 3.6
    assert_internal_state(d)


def test_tuples_construction():
    d = IndexedDict([(1, 2), (3, 4)])
    assert list(d) == [1, 3]  # Must have correct order
    assert_internal_state(d)


def test_clear():
    d = IndexedDict(a=1, b=2, c=3)
    d.clear()
    assert len(d) == 0
    assert list(d) == []
    assert_internal_state(d)


@pytest.fixture()
def d(request):
    ret = IndexedDict([(chr(ord("a") + i), 10 + i) for i in range(5)])
    request.addfinalizer(lambda: assert_internal_state(ret))
    return ret


@pytest.mark.parametrize("indexing", [{"key": "b"}, {"index": 1}, {"index": -4}])
def test_get_key_found(d, indexing):
    assert d.get(**indexing) == 11


@pytest.mark.parametrize("indexing", [{"key": "x"}, {"index": 100}, {"index": -6}])
def test_get_specifying_missing_default(d, indexing):
    assert d.get(default=5, **indexing) == 5


def test_get_deprecated_param(d):
    with pytest.deprecated_call():
        assert d.get('x', d='XXX') == 'XXX'


@pytest.mark.parametrize("indexing", [{"key": "x"}, {"index": 100}, {"index": -6}])
def test_get_missing_default(d, indexing):
    assert d.get(**indexing) is None


def test_get_duplicate_default(d):
    with pytest.raises(ValueError):
        d.get(d=None, default=None)
    with pytest.raises(ValueError):
        d.get(d='XXX', default=None)
    with pytest.raises(ValueError):
        d.get(d=None, default='XXX')
    with pytest.raises(ValueError):
        d.get(d='XXX', default='XXX')


def test_get_both_key_and_index(d):
    with pytest.raises(TypeError):
        d.get(key="a", index=4)


def test_get_no_key_or_index(d):
    with pytest.raises(TypeError):
        d.get()


@pytest.mark.parametrize("indexing", [{"key": "b"}, {"index": 1}, {"index": -4}])
def test_pop_found(d, indexing):
    assert d.pop(**indexing) == 11
    assert list(d) == list("acde")


def test_pop_last(d):
    assert d.pop() == 14
    assert list(d) == list("abcd")


@pytest.mark.parametrize("indexing", [{"key": "x"}, {"index": 100}, {"index": -6}])
def test_pop_missing_default(d, indexing):
    assert d.pop(d="XXX", **indexing) == "XXX"
    assert list(d) == list("abcde")


def test_pop_duplicate_default(d):
    with pytest.raises(ValueError):
        d.pop(d='XXX', default='XXX')


def test_pop_missing_key_no_default(d):
    with pytest.raises(KeyError):
        d.pop("X")
    assert list(d) == list("abcde")


@pytest.mark.parametrize("index", [100, -6])
def test_pop_missing_index_no_default(d, index):
    with pytest.raises(IndexError):
        d.pop(index=index)
    assert list(d) == list("abcde")


def test_deprecated_pop_default(d):
    with pytest.deprecated_call():
        assert d.pop(999, d='XXX') == 'XXX'


def test_pop_empty_default():
    d = IndexedDict()
    assert d.pop(d="XXX") == "XXX"


def test_pop_empty_no_default():
    d = IndexedDict()
    with pytest.raises(IndexError):
        d.pop()


def test_pop_both_key_and_index(d):
    with pytest.raises(TypeError):
        d.pop(key="a", index=4)


@pytest.mark.parametrize("indexing", [{"key": "b"}, {"index": 1}, {"index": -4}])
def test_fast_pop_found(d, indexing):
    assert d.fast_pop(**indexing) == (11, 1, "e", 14)
    assert set(d) == set("acde")


def test_fast_pop_last(d):
    assert d.fast_pop() == (14, 4, "e", 14)
    assert set(d) == set("abcd")


def test_fast_pop_last_key(d):
    assert d.fast_pop("e") == (14, 4, "e", 14)
    assert set(d) == set("abcd")


def test_fast_pop_missing_key(d):
    with pytest.raises(KeyError):
        d.fast_pop("X")
    assert list(d) == list("abcde")


def test_fast_pop_missing_index(d):
    with pytest.raises(IndexError):
        d.fast_pop(index=100)
    assert list(d) == list("abcde")


def test_fast_pop_empty():
    d = IndexedDict()
    with pytest.raises(IndexError):
        d.fast_pop()


def test_fast_pop_both_key_and_index(d):
    with pytest.raises(TypeError):
        d.fast_pop(key="a", index=4)


def test_popitem(d):
    assert d.popitem() == ("e", 14)
    assert list(d) == list("abcd")


def test_popitem_first(d):
    assert d.popitem(last=False) == ("a", 10)
    assert list(d) == list("bcde")


def test_popitem_last(d):
    assert d.popitem(last=True) == ("e", 14)
    assert list(d) == list("abcd")


def test_popitem_index(d):
    assert d.popitem(index=2) == ('c', 12)
    assert list(d) == list('abde')


def test_popitem_key(d):
    assert d.popitem(key='d') == ('d', 13)
    assert list(d) == list('abce')


def test_popitem_multiple_params(d):
    with pytest.raises(ValueError):
        d.popitem(last=True, index=-1)


def test_popitem_empty():
    d = IndexedDict()
    with pytest.raises(KeyError):
        d.popitem()


def test_copy(d):
    l = list(d)
    d2 = d.copy()
    assert_internal_state(d2)

    d.fast_pop("e")
    assert_internal_state(d)
    assert_internal_state(d2)
    assert list(d) != l
    assert list(d2) == l

    d["X"] = "y"
    assert_internal_state(d)
    assert_internal_state(d2)
    assert list(d) != l
    assert list(d2) == l

    d2["Z"] = "w"
    assert_internal_state(d)
    assert_internal_state(d2)


@pytest.mark.parametrize("indexing", [{"key": "b"}, {"index": 1}, {"index": -4}])
def test_move_to_end_key_found(d, indexing):
    d.move_to_end(**indexing)
    assert list(d) == list("acdeb")


def test_move_to_end_noop(d):
    d.move_to_end("e")
    assert list(d) == list("abcde")


@pytest.mark.parametrize("indexing", [{"key": "b"}, {"index": 1}, {"index": -4}])
def test_move_to_begin_key_found(d, indexing):
    d.move_to_end(last=False, **indexing)
    assert list(d) == list("bacde")


def test_move_to_begin_noop(d):
    d.move_to_end("a", last=False)
    assert list(d) == list("abcde")


def test_move_to_end_missing_key(d):
    with pytest.raises(KeyError):
        d.move_to_end(key="X")
    assert list(d) == list("abcde")


@pytest.mark.parametrize("index", [100, -6])
def test_move_to_end_missing_index(d, index):
    with pytest.raises(IndexError):
        d.move_to_end(index=index)
    assert list(d) == list("abcde")


def test_move_to_end_both_key_and_index(d):
    with pytest.raises(TypeError):
        d.move_to_end(key="a", index=4)


def test_move_to_end_no_key_or_index(d):
    with pytest.raises(TypeError):
        d.move_to_end()


def test_index(d):
    assert d.index("c") == 2


def test_index_missing(d):
    with pytest.raises(KeyError):
        d.index("X")


def test_key(d):
    assert d.key(3) == "d"


def test_key_negative(d):
    assert d.key(-2) == "d"


def test_key_missing(d):
    with pytest.raises(IndexError):
        d.key(100)


def test_len(d):
    assert len(d) == 5


def test_getitem(d):
    assert d["a"] == 10
    assert d["c"] == 12


def test_getitem_missing(d):
    with pytest.raises(KeyError):
        d["X"]  # noqa


def test_setitem_overwrite(d):
    d["a"] = 110
    assert list(d) == list("abcde")
    assert d["a"] == 110


def test_setitem_create(d):
    d["x"] = 500
    assert list(d) == list("abcdex")
    assert d["x"] == 500


def test_delitem(d):
    del d["c"]
    assert list(d) == list("abde")


def test_delitem_missing(d):
    with pytest.raises(KeyError):
        del d["x"]


def test_contains(d):
    assert "d" in d
    assert "x" not in d


def test_keys(d):
    assert list(d.keys()) == list("abcde")


def test_values(d):
    assert list(d.values()) == [10, 11, 12, 13, 14]


def test_none_key(d):
    d[None] = None
    assert d[None] is None
    assert list(d) == list("abcde") + [None]


def test_repr():
    d = IndexedDict()
    d[1] = "X"
    d["Y"] = 2
    d[None] = None
    assert repr(d) == "IndexedDict([(1, 'X'), ('Y', 2), (None, None)])"


def test_str():
    d = IndexedDict()
    d[1] = "X"
    d["Y"] = 2
    d[None] = None
    assert str(d) == "IndexedDict({1: 'X', 'Y': 2, None: None})"


def test_items(d):
    assert list(d.items()) == [(chr(ord("a") + i), 10 + i) for i in range(5)]
