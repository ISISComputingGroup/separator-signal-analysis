test:
	python -m unittest discover -s tests -p "test_*.py"

.PHONY: data
data:
	python src\make_dataset.py
