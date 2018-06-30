.PHONY: docs tests

help:
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  tests       run tests (using py.test)"
	@echo "  testall     run tests for all Python versions (using tox)"
	@echo "  coverage    run coverage report"
	@echo "  publish     publish to PyPI"
	@echo "  docs        create HMTL docs (using Sphinx)"

tests:
	py.test

testall:
	tox

clean:
	rm -rf build
	rm -rf dist
	rm -rf data_structures.egg-info
	find . -name *.pyc -delete
	find . -name *.pyo -delete
	find . -name *~ -delete
	find . -name __pycache__ -delete
	find . -name *,cover -delete

lint:
	flake8 --statistics --count

coverage:
	coverage run --source collections_extended setup.py pytest
	coverage report -m
	coverage html

publish: testall lint coverage publish-force

publish-force:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
	git push
	git push --tags

docs:
	rm -f docs/collections_extended.rst
	rm -f docs/modules.rst
	#sphinx-apidoc -o docs/ collections_extended
	make -C docs clean
	make -C docs html
	xdg-open docs/_build/html/index.html
