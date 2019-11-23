"""setup.py for collections_extended."""
from os.path import dirname, join
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
	"""TestCommand to run py.test."""

	def finalize_options(self):
		"""Finalize option before test is run."""
		TestCommand.finalize_options(self)
		self.test_args = ['tests']
		self.test_suite = True

	def run_tests(self):
		"""Run tests."""
		import pytest
		errcode = pytest.main(self.test_args)
		sys.exit(errcode)


def long_description():
	"""Read long description from README."""
	path = join(dirname(__file__), 'README.rst')
	with open(path, 'rt') as inf:
		return inf.read()


setup(
	name='collections-extended',
	packages=['collections_extended'],
	version='1.0.2',
	description=(
		'Extra Python Collections - bags (multisets) and setlists (ordered'
		' sets)'
		),
	author='Michael Lenzen',
	author_email='m.lenzen@gmail.com',
	license='Apache License, Version 2.0',
	url='http://collections-extended.lenzm.net/',
	keywords=[
		'collections',
		'bag',
		'multiset',
		'setlist',
		'ordered set',
		'unique list',
		],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: Implementation :: PyPy',
		'Topic :: Software Development',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		],
	long_description=long_description(),
	long_description_content_type='text/x-rst',
	install_requires=['setuptools'],
	tests_require=['pytest'],
	package_data={'': ['README.rst', 'LICENSE', 'CONTRIBUTING.rst']},
	cmdclass={'test': PyTest},
	)
