#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from invoke import run, task
from invoke.util import log


@task
def test():
	"""test - run the test runner."""
	run('python setup.py test', pty=True)


@task(name='test-all')
def testall():
	"""test-all - run tests on every Python version with tox."""
	run('tox')


@task
def clean():
	"""clean - remove build artifacts."""
	run('rm -rf build/')
	run('rm -rf dist/')
	run('rm -rf data_structures.egg-info')
	run('find . -name *.pyc -delete')
	run('find . -name *.pyo -delete')
	run('find . -name *~ -delete')
	run('find . -name __pycache__ -delete')

	log.info('cleaned up')


@task
def lint():
	"""lint - check style with flake8."""
	run('flake8 collections_extended tests')


@task
def coverage():
	"""coverage - check code coverage quickly with the default Python."""
	run('coverage run --source collections_extended setup.py test')
	run('coverage report -m')
	run('coverage html')
	run('open htmlcov/index.html')

	log.info('collected test coverage stats')


@task(clean)
def publish():
	"""publish - package and upload a release to the cheeseshop."""
	run('python setup.py sdist upload', pty=True)
	run('python setup.py bdist_wheel upload', pty=True)

	log.info('published new release')


@task
def docs():
	run('rm -f docs/collections_extended.rst')
	run('rm -f docs/modules.rst')
	run('sphinx-apidoc -o docs/ collections_extended')
	run('make -C docs clean')
	run('make -C docs html')
	run('open docs/_build/html/index.html')
