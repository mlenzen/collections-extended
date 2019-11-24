============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/mlenzen/collections-extended/issues.

If you are reporting a bug, please include:

* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

This could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts,
articles, and such.

Documentation is built automatically on every push using Read the Docs.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/mlenzen/collections-extended/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Useful Reading
~~~~~~~~~~~~~~

https://docs.python.org/3/reference/datamodel.html#emulating-container-types
https://docs.python.org/3/library/collections.abc.html

Ready to contribute? Here's how to set up `collections-extended` for local development.

#. Fork the `collections-extended` repo on GitHub.
#. Clone your fork locally::

	$ git clone git@github.com:your_name_here/collections-extended.git

#. Make sure you are excluding your editor's files from the repo

	We don't want to use the project's gitignore to exclude every
	editor's files, so set up your global gitignore.
	See: https://help.github.com/articles/ignoring-files/

#. Install your local copy into a virtualenv::

	$ cd collections-extended
	$ python -m venv .venv
	$ . .venv/bin/activate
	$ pip install -r requirements.txt

#. Create a branch for local development::

	$ git checkout -b name-of-your-bugfix-or-feature

#. Make your changes locally.

#. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

	$ flake8
	$ py.test
	$ tox

#. Commit your changes and push your branch to GitHub::

	$ git add .
	$ git commit -m "Your detailed description of your changes."
	$ git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for all supported versions. Check
   https://travis-ci.org/mlenzen/collections-extended/pull_requests
   and make sure that the tests pass for all supported Python versions.
4. Add the feature/bug to the appropriate section in HISTORY.rst
5. Review and update the relevant docs.

Tips
----

To run a subset of tests::

	$ py.test tests/test_example.py
	$ py.test tests/test_example.py::test_func
