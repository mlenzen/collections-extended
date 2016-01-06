"""Python 2/3 compatibility helpers."""
import sys

is_py2 = sys.version_info[0] == 2

if is_py2:
	keys_set = lambda d: set(d.keys())
else:
	keys_set = dict.keys
