from os.path import dirname, join
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

	def finalize_options(self):
		TestCommand.finalize_options(self)
		self.test_args = ['tests']
		self.test_suite = True

	def run_tests(self):
		import pytest
		errcode = pytest.main(self.test_args)
		sys.exit(errcode)

setup(
		name='collections-extended',
		packages=['collections_extended'],
		version='0.3.0',
		description=(
			'Extra Python Collections - bags (multisets) and setlists (ordered'
			' sets)'
			),
		author='Michael Lenzen',
		author_email='m.lenzen@gmail.com',
		license='Apache License, Version 2.0',
		url='http://collections-extended.lenzm.net/',
		keywords=['collections', 'bag', 'multiset', 'setlist', 'ordered set', 'unique list'],
		classifiers=[
			'Development Status :: 4 - Beta',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: Apache Software License',
			'Operating System :: OS Independent',
			'Programming Language :: Python',
			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 2.6',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.2',
			'Programming Language :: Python :: 3.3',
			'Programming Language :: Python :: 3.4',
			'Programming Language :: Python :: Implementation :: PyPy',
			'Topic :: Software Development',
			'Topic :: Software Development :: Libraries',
			'Topic :: Software Development :: Libraries :: Python Modules',
			],
		long_description = open(join(dirname(__file__), 'README.rst')).read(),
		install_requires=['setuptools'],
		tests_require=['pytest'],
		package_data={'': ['README.rst', 'LICENSE', 'CONTRIBUTING.rst']},
		cmdclass={'test': PyTest},
		)
