Release Checklist
-----------------

#. ``bumpversion [patch|minor|major]``

#. ``make publish``

#.	Test that it pip installs

	#. Make a test virtual environment
	#. ``pip install collections-extended``
	#. Confirm the new version number was installed
	#. Try it out

#. Check the PyPI listing page to make sure that the README displays properly.

   If not, copy and paste the RestructuredText into http://rst.ninjs.org/ to
   find out what broke the formatting.

New Python Versions
-------------------

To add support for a new version of python, aside from any new functionality
required, add version number to:

#. tox.ini envlist
#. .github/workflows/python-package.yml
#. pyproject.toml classifiers
#. README.rst description
#. docs/index.rst list of versions

New Year
--------

When a new year arrives, it needs to be updated in:

* README.rst
* docs/index.rst
* docs/conf.py
