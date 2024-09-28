SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy barra2_dl tests
	poetry run flake8 .
	if poetry run command -v doc8 > /dev/null 2>&1; then poetry run doc8 -q docs; fi

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check

.PHONY: test
test: lint package unit
