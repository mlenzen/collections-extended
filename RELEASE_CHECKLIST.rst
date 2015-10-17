Release Checklist
-----------------

#. ``bumpversion ...``

#. Install the package again for local development, but with the new version number: ``python setup.py develop``

#. Run the tests::

	python setup.py test
	tox

#. Build the source distribution: ``python setup.py sdist``

#. Test that the sdist installs::

	mktmpenv
	cd dist
	tar xzvf collections-extended-x.y.z.tar.gz
	cd collections-extended-x.y.z/
	python setup.py install
	<try it out>
	deactivate

#. ``make publish``

#. Test that it pip installs::

	mktmpenv
	pip install collections-extended
	<try it out>
	deactivate

#. Push: ``git push``

#. Push tags: ``git push --tags``

#. Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.

New Python Versions
-------------------

To add support for a new version of python, aside from any new functionality required, add version number to:

#. tox.ini envlist
#. .travis.yml
#. setup.py classifiers
#. README.rst description
