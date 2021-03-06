from typing import (
	Any,
	Callable,
	Collection,
	Iterable,
	Generic,
	Tuple,
	TypeVar,
)

from .mulset import MulSet, MulSetView

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')


class Pair(Tuple[KeyType, ValType]):

	def __init__(self, key: KeyType, val: ValType):
		self.key = key
		self.val = val


class KeysView(MulSetView):

	def __iter__(self):
		for pair in self.mulset:
			yield pair.key

	def __contains__(self, item):
		for pair in self.mulset:
			if pair.key == item:
				return True
		return False


class ValuesView(MulSetView):

	def __iter__(self):
		for pair in self.mulset:
			yield pair.val

	def __contains__(self, item):
		for pair in self.mulset:
			if pair.val == item:
				return True
		return False


class KeyedMulSet(MulSet[Pair]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.keys = KeysView(self)
		self.values = ValuesView(self)
