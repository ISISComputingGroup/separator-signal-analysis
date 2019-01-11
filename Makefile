.PHONY: clean data requirements test help notebooks

MAKEFLAGS += --silent

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install the requirements

requirements:
	python -m pip install -U pip setuptools wheel
	python -m pip install -r requirements.txt

## Delete all compiled Python files and altair json files
clean:
	@echo off
	del /S *.pyc
	del /S *.pyo
	del /S "__pycache__
	del /S *.json
	
## Download raw data sets
data:  
	python src\make_dataset.py
	
## Run all tests
test: requirements
	python -m unittest discover -s src/tests -p "test_*.py"
	

## Starts up notebook server
notebooks: requirements
	python -m notebook

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
	@echo notebooks			Start the Jupyter notebooks server running.	
	@echo.
	
