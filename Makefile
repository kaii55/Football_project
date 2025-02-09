install:
	pip install -r requirements.txt

test:
	pytest tests/

run-notebook:
	jupyter notebook
