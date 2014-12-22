from os.path import dirname, join

from setuptools import setup
from setuptools.command.test import test as TestCommand

import collections_extended

class PyTest(TestCommand):
	def finalize_options(self):
		TestCommand.finalize_options(self)
		self.test_args = []
		self.test_suite = True

	def run_tests(self):
		import pytest
		errcode = pytest.main(self.test_args)
		sys.exit(errcode)

setup(
		name='data-structures',
		packages=['collections_extended'],
		version = collections_extended.__version__,
		description = 'Extra Python Data Structures - bags (multisets) and setlists (ordered sets)',
		author = 'Michael Lenzen',
		author_email = 'm.lenzen@gmail.com',
		license='Apache License, Version 2.0',
		url = 'https://github.com/mlenzen/python-data-structures',
		keywords = ['collections', 'bag', 'multiset', 'setlist', 'ordered set', 'unique list'],
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
		tests_require=['pytest'],
		)
