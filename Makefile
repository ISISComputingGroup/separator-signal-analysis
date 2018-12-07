.PHONY: clean data requirements test help

MAKEFLAGS += --silent

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install the requirements

requirements:
	python -m pip install -U pip setuptools wheel
	python -m pip install -r requirements.txt

## Delete all compiled Python files
clean: 
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	
## Download raw data sets
data:  
	python src\make_dataset.py
	
## Run all tests
test: requirements
	python -m unittest discover -s src/tests -p "test_*.py"


#################################################################################
#  Help																			#
#################################################################################

.DEFAULT_GOAL := help

help:	
	@echo.
	@echo Commands			Description
	@echo ---------------------------------------------------------------
	@echo clean				Delete all compiled Python files.
	@echo data				Download raw data sets.
	@echo requirements			Install the requirements.
	@echo test				Run all tests.	
	@echo.
	