import sys

is_py2 = sys.version_info[0] == 2

if is_py2:
	maxint = sys.maxint
else:
	maxint = sys.maxsize
