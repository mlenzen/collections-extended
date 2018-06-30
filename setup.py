"""setup.py for collections_extended."""
from os.path import dirname, join

from setuptools import setup


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
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: Implementation :: PyPy',
		'Topic :: Software Development',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		],
	long_description=open(join(dirname(__file__), 'README.rst')).read(),
	install_requires=['setuptools'],
	setup_requires=['pytest-runner'],
	tests_require=['pytest'],
	package_data={'': ['README.rst', 'LICENSE', 'CONTRIBUTING.rst']},
	)
