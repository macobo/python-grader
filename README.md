Python Grader [![Build Status](https://travis-ci.org/macobo/python-grader.png?branch=master)](https://travis-ci.org/macobo/python-grader)
=============

## Goals

Providing a **robust** and **secure** way to automatically grade first-year 
programming courses taught in Python.
Focus is on writing **succinct** tests for grading student solutions and useful feedback for the student. 

## Setup

**Prerequsite**: Install python3.3 (or python3.4), preferably use a virtualenv.

For full setup guide which involves building python from source and setting up a virtualenv, 
see [INSTALL.md](INSTALL.md)

```bash
# navigate to your projects dir, e.g. ~/projects
git clone https://github.com/macobo/python-grader.git
cd python-grader

python3.3 setup.py install
```

To run tests, run `python3.3 run_tests.py`.



## Sample test

###Task:
Write a function named `taisnurkne` that takes three numbers as an agument and returns True or False 
according to whether it's possible to form a right-angled triangle with such side lengths. 
Side lengths are guaranteed to be positive.

###Tester [u6_taisnurkne_tester.py](tasks/MTAT.100/book/u6_taisnurkne_tester.py)
```python
from grader import *

check_function("taisnurkne", [3, 4, 5], True)
check_function("taisnurkne", [1, 1, 1], False)
check_function("taisnurkne", [917.2102192315585, 561.3888059296613, 1075.3752729563455], True)
check_function("taisnurkne", [917.2102192315585, 561.3888059296613, 1075.2752729563455], False)
```

### Running test on a file
To run tests, run `python3.3 -m grader <tester_file> <solution_file>` in the directory they are both contained.

For example, to run the above tester (in the tasks folder) on the sample solution:
```bash
cd tasks/MTAT.100/book
python3.3 -m grader u6_taisnurkne_tester.py u6_taisnurkne_solution.py
```

