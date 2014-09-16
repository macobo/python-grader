Python Grader [![Build Status](https://travis-ci.org/macobo/python-grader.png?branch=master)](https://travis-ci.org/macobo/python-grader)
=============

---------------
This project was made as a part of Karl-Aksel Puulmann's Bachelor's thesis. The following two links serve as a better introduction to the project than this readme does.

* [Link to poster introducing project](http://macobo.github.io/python-grader/poster.pdf)
* [Link to thesis](http://macobo.github.io/python-grader/thesis.pdf)

-------

This is a module for automatically testing homework solutions that has been used for giving feedback for homeworks and midterms for various first-year programming courses at University of Tartu.

What this project does differently from conventional unit-testing frameworks is allow testing of interactive, input-output based programs as well as more conventional function/class based programs, meanwhile retaining a simple and powerful interface for doing that.

For the student, feedback provided by the module should be helpful for debugging and understanding where they went wrong.

For the teacher, the advantage over using normal unit tests is that it allows to move from purely-manual based input-output testing to a more structured and consistent framework that saves time.


## Example

###Task statement
Write a program which tries to guess an integer that the user picks with as few 
guesses as possible. 

More specifically, each time the program outputs a number, 
the user will answer that the number is either “too large”, “too small” or “correct”. 

###Tester [interactive_search_tester.py](tasks/Examples/interactive_search_tester.py)
```python
from grader import *

# This decorator creates 12 tests, each searching for a different number
@test_cases(
    # list all the different numbers to search for
    [1, 10000, 5000, 3, 9990, 7265, 8724, 2861, 2117, 811, 6538, 4874],
    # The description of the test, shown to the user
    description="Searching for number {0}"
)
def search(m, searched_number):
    # test function - First argument (always given) is a container
    # for the users program and for the stdin/stdout.
    # Second is the searched number (see above).
    found = False
    guesses = []

    while len(guesses) < 14 and not found:
        # Get what the user guessed since last time we asked.
        # This might raise an error if the program didn't only write out a number.
        guess = int(m.stdout.new())
        guesses.append(guess)
        # let the program know if the guess was
        # correct, too large or too small.
        if guess < searched_number:
            m.stdin.put("too small")
        elif guess > searched_number:
            m.stdin.put("too large")
        elif guess == searched_number:
            m.stdin.put("correct")
            found = True

    # If program didn't find the solution fast enough,
    # notify that the program made too many guesses.
    assert found, (
        "Program made too many guesses.\n" +
        "Guesses were: {}".format(guesses))
```

## Setup

**Prerequsite**: Install python3.3 (or python3.4), preferably use a virtualenv.

For full setup guide which involves building python from source and setting up a virtualenv, 
see [INSTALL.md](INSTALL.md)

```bash
# navigate to your projects dir, e.g. ~/projects
git clone https://github.com/macobo/python-grader.git
cd python-grader

python setup.py install
```

To run tests for this module, run `python run_tests.py`.


### Running test on a file
To tester on a solution, run `python -m grader <tester_file> <solution_file>`.

For example, to run the above tester (in the tasks folder) on the sample solution:
```bash
cd tasks/
python -m grader Examples/interactive_search_tester.py Examples/interactive_search_solution.py
```
