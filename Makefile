.PHONY: install test lint run cpu

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

run:
	uvicorn api.main:app --reload

cpu:
	python simulator/cpu/stress.py --duration 5 --workers 1
