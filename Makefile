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
	rm -rf build
	rm -rf dist
	rm -rf data_structures.egg-info
	find . -name *.pyc -delete
	find . -name *.pyo -delete
	find . -name *~ -delete
	find . -name __pycache__ -delete
	find . -name *,cover -delete

.PHONY: lint
lint:
	flake8 --statistics --count

.PHONY: mypy
mypy:
	# TODO type check tests
	mypy collections_extended

.PHONY: coverage
coverage:
	coverage run --source collections_extended setup.py test
	coverage report -m
	coverage html

.PHONY: publish
publish: testall mypy lint coverage publish-force

.PHONY: publish-force
publish-force:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
	git push
	git push --tags

.PHONY: docs
docs:
	rm -f docs/collections_extended.rst
	rm -f docs/modules.rst
	#sphinx-apidoc -o docs/ collections_extended
	make -C docs clean
	make -C docs html
	#xdg-open docs/_build/html/index.html
