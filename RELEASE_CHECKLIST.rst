Release Checklist
-----------------

#. Run tests and linter ``make testall`` and ``make lint``

#. ``bumpversion [patch|minor|major]``

#. Install the package again for local development, but with the new version number: ``python setup.py develop``

#. ``make publish``

#. Test that it pip installs::

	mktmpenv
	pip install collections-extended
	<try it out>
	deactivate

#. Check the PyPI listing page to make sure that the README displays properly.
	If not, copy and paste the RestructuredText into http://rst.ninjs.org/ to
	find out what broke the formatting.

New Python Versions
-------------------

To add support for a new version of python, aside from any new functionality
required, add version number to:

#. tox.ini envlist
#. .travis.yml
#. setup.py classifiers
#. README.rst description
#. docs/index.rst list of versions

New Year
--------

When a new year arrives, it needs to be updated in:

* README.rst
* docs/index.rst
* docs/conf.py
