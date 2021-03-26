VENV = .venv

.PHONY: default
default: clean deps tests

.PHONY: deps
deps: $(VENV) requirements.txt
	pip install -r requirements.txt

$(VENV):
	python -m venv $@
	$@/bin/pip install --upgrade pip wheel setuptools

.PHONY: tests
tests: clean
	py.test

.PHONY: testall
testall: clean
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

.PHONY: deep-clean
deep-clean: clean
	rm --recursive --force $(VENV)
	rm --recursive --force .eggs
	rm --recursive --force .pytest_cache
	rm --recursive --force .tox

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
