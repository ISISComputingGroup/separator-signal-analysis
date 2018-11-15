.PHONY: clean data  requirements test

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install the requirements
requirements: test_environment
	python -m pip install -U pip setuptools wheel
	python -m pip install -r requirements.txt

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	
## Clean raw data sets
data: requirements
	python src\make_dataset.py
	
## Run all tests
test:
	python -m unittest discover -s src/tests -p "test_*.py"
