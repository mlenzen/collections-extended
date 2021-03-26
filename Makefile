.PHONY: help
help:
	@echo "  clean         remove unwanted files like .pyc's"
	@echo "  lint          check style with flake8"
	@echo "  tests         run tests (using py.test)"
	@echo "  testall       run tests for all Python versions (using tox)"
	@echo "  coverage      run coverage report"
	@echo "  publish       publish to PyPI"
	@echo "  publish-force publish to PyPI ignoring tests and linting"
	@echo "  docs          create HMTL docs (using Sphinx)"

.PHONY: tests
tests:
	py.test

.PHONY: testall
testall:
	tox

.PHONY: clean
clean:
	rm --recursive --force build
	rm --recursive --force dist
	rm --recursive --force *.egg-info
	find . -name *.py[co] -delete
	find . -name *~ -delete
	find . -name __pycache__ -delete
	find . -name *,cover -delete

.PHONY: lint
lint:
	flake8 --statistics --count

.PHONY: coverage
coverage:
	coverage run --source collections_extended --module pytest
	coverage report --show-missing
	coverage html

.PHONY: publish
publish: testall lint coverage publish-force

.PHONY: publish-force
publish-force:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
	git push
	git push --tags

.PHONY: docs
docs:
	rm --force docs/collections_extended.rst
	rm --force docs/modules.rst
	#sphinx-apidoc --output-dir docs/ collections_extended
	make --directory docs clean
	make --directory docs html
	#xdg-open docs/_build/html/index.html
