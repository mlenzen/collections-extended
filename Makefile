PACKAGE = collections_extended
VENV = $(shell poetry env info --path)

.PHONY: default
default: clean deps tests

.PHONY: deps
deps:
	pip install poetry
	poetry install --remove-untracked

.PHONY: tests
tests:
	poetry run py.test

.PHONY: testall
testall:
	poetry run tox

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
deep-clean: clean clean-docs
	rm --recursive --force $(VENV)
	rm --recursive --force .eggs
	rm --recursive --force .pytest_cache
	rm --recursive --force .tox

# Linting

.PHONY: lint
lint:
	poetry run flake8 --statistics --count
	poetry check

.PHONY: fixme-check
fixme-check:
	! git grep FIXME | grep "^Makefile" --invert-match

.PHONY: coverage
coverage:
	poetry run coverage run --source $(PACKAGE) --module pytest
	poetry run coverage report --show-missing
	poetry run coverage html

# Publishing

.PHONY: publish
publish: fixme-check lint testall publish-force

.PHONY: publish-force
publish-force:
	poetry build
	poetry publish
	git push
	git push --tags

.PHONY: clean-docs
clean-docs:
	rm --force docs/$(PACKAGE).rst
	rm --force docs/modules.rst

.PHONY: docs
docs: clean-docs
	#sphinx-apidoc --output-dir docs/ $(PACKAGE)
	make --directory docs clean
	make --directory docs html
	#xdg-open docs/_build/html/index.html
