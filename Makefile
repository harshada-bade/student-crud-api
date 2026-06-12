.PHONY: install run migrate test

install:
	pip install -r requirements.txt

run:
	python run.py

migrate:
	flask db upgrade

test:
	pytest tests/ -v