import sys

is_py2 = sys.version_info[0] == 2

if is_py2:
	maxint = sys.maxint
	keys_set = lambda d: set(d.keys())
else:
	maxint = sys.maxsize
	keys_set = dict.keys
