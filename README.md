# Separator Signal Analysis

This repository contains analysis of the voltage and current signal from the 
MUONFE Separator PSU.

## Setup

The commands to setup the environment to repeat the data analysis can be 
found in the make file. To find out what commands are available, run `make` or `make help`.

### Getting started

To set up the repository so you can view the analysis/start a new analysis after 
cloning the git repository:
1. First run `make requirements` in an EPICS terminal to install the extra 
python packages used.
2. Next run `make data` in an EPICS terminal to get the raw data from the 
share. You should treat the raw data as being immutable.
3. Run `make notebooks` in an EPICS terminal to start the Jupyter notebook server. 
It will open a web browser from which to navigate the directory structure 
and view Jupyter notebooks in the `notebooks` folder.

### Commands

#### To get the raw data

Call `make data` in an EPICS terminal.

#### To install the required python packages.

Call `make requirements` in an EPICS terminal.

#### Delete complied python files and extra json files

Call `make clean` in an EPICS terminal.

#### To run the unit tests

Call `make test` in an EPICS terminal.

#### To start the notebook server

Call `make notebook` in an EPICS terminal to start the notebook server. 
`CTRL + C` in the window running the server will stop the server.

#### To get help on what commands you can use

Call `make` or `make help` in an EPICS terminal.


## Data Analysis

### Key Libraries

The main libraries used to perform the data analysis are:

- **Pandas**: Used for importing, cleaning and manipulating data. 
[Docs](http://pandas.pydata.org/pandas-docs/stable/) and a 
[tutorial](http://pandas.pydata.org/pandas-docs/stable/10min.html)).
- **Jupyter**: Used to create interactive notebooks detailing the analysis (https://jupyter.org/). 
These are a combination of markdown and code cells. They should be able to run in order 
from the top to the bottom.
- **Altair**: A declarative charting library which uses the JavaScript library 
`Vega-Lite` to render charts. [Docs](https://altair-viz.github.io/) and 
[examples](https://altair-viz.github.io/gallery/index.html).
 
### Merging notebooks

You may find the nbdime package useful for dealing with merge conflicts with Jupyter 
notebooks ([docs](https://nbdime.readthedocs.io/en/latest/)). This package is installed as 
part of the requirements. To set up git integration run

```bash
python -m nbdime config-git --enable --global
```

To use the web based merge conflict tool, call:

```bash
python -m nbdime mergetool
```
