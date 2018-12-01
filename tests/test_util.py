import pickle

from collections_extended._util import Sentinel, NOT_SET


class TestSentinel:

	def test_equal(self):
		assert Sentinel('abc') == Sentinel('abc')

	def test_not_equal(self):
		assert not NOT_SET == None

	def test_is(self):
		assert Sentinel('a') is Sentinel('a')

	def test_str(self):
		assert str(Sentinel('abc')) == '<abc>'

	def test_repr(self):
		# assert repr(Sentinel('abc')) == "Sentinel('abc')"
		assert str(Sentinel('abc')) == '<abc>'

	def test_pickle(self):
		pickled = pickle.dumps(NOT_SET, protocol=2)
		unpickled = pickle.loads(pickled)
		assert unpickled == NOT_SET
		assert unpickled is NOT_SET
