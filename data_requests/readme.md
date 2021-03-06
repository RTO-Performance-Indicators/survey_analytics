# README

This folder contains code that assists with common data requests.

There are two scripts:

* SSS_Query.py
* survey_functions.py

SSS_Query.py contains Megan's version of python code.

survey_functions.py contains Andrew's version of python code.

## Usage

### python

To use the python functions in this module:

1. Make sure you have a copy of this repository on a local drive
2. Import the module by:
    + importing the sys module
    + append the location of the repository
    + specify the script of your choice

For example, to import survey_functions.py and the functions contained in the
script:

```
import sys
sys.path.append('C:\\...\\GitHub\\survey_analytics')
from data_requests import survey_functions
```

### R

To use the R functions in this module:

1. Make sure you have a copy of this repository on a local drive
2. Import the script using the *source* function

For example:

```
source("C:/Users/.../Documents/GitHub/survey_analytics/data_requests/[filename].R")
```