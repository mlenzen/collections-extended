from distutils.core import setup
from os.path import dirname, join

_version = '0.1.2'

setup(
		name='data-structures',
		version = _version,
		description = 'Python Data Structures - bags/multisets and setlists',
		author = 'Michael Lenzen',
		author_email = 'm.lenzen@gmail.com',
		url = 'https://github.com/mlenzen/python-data-structures',
		py_modules = ['collections_extended'],
		keywords = ['collections', 'bag', 'multiset', 'setlist'],
		classifiers = [
			'Development Status :: 4 - Beta',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: Apache Software License',
			'Operating System :: OS Independent',
			'Programming Language :: Python',
			'Programming Language :: Python :: 3',
			'Topic :: Software Development',
			'Topic :: Software Development :: Libraries',
			'Topic :: Software Development :: Libraries :: Python Modules',
			],
		long_description = open(join(dirname(__file__), 'README.rst')).read(),
		)
