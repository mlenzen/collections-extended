POETRY = poetry

.PHONY: default
default: clean deps tests

.PHONY: deps
deps:
	poetry install --remove-untracked

.PHONY: tests
tests: clean
	poetry run py.test

.PHONY: testall
testall: clean
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
deep-clean: clean
	rm --recursive --force $(VENV)
	rm --recursive --force .eggs
	rm --recursive --force .pytest_cache
	rm --recursive --force .tox

.PHONY: lint
lint:
	poetry run flake8 --statistics --count
	poetry check

.PHONY: fixme-check
fixme-check:
	! git grep FIXME | grep "^Makefile" --invert-match

.PHONY: coverage
coverage:
	poetry run coverage run --source collections_extended --module pytest
	poetry run coverage report --show-missing
	poetry run coverage html

.PHONY: publish
publish: testall lint coverage publish-force

.PHONY: publish-force
publish-force:
	poetry build
	poetry publish
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
