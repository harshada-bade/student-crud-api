.PHONY: install run migrate test

install:
	pip install -r requirements.txt

run:
	flask db upgrade && python run.py

test:
	pytest tests/ -v