"""
Task statement
Write a program which tries to guess an integer that the user picks with as few 
guesses as possible. More specifically, each time the program outputs a number, 
the user will answer that the number is either “too large”, “too small” or “correct”. 
"""

from grader import *

# This decorator creates 12 tests, each searching for a different number
@test_with_args(
    # list all the different numbers to search for
    [1, 10000, 5000, 3, 9990, 7265, 8724, 2861, 2117, 811, 6538, 4874],
    # The description of the test, shown to the user
    description="Searching for number {0}"
)
def testi(m, searched_number):
    # test function - First argument (always given) is a container
    # for the users program and for the stdin/stdout.
    # Second is the searched number (see above).
    found = False
    guesses = []

    while len(guesses) < 15 and not found:
        # Get what the user guessed since last time we asked.
        # This might raise an error if the program didn't only write out a number.
        guess = int(m.stdout.new())
        guesses.append(guess)
        # let the program know if the guess was
        # correct, too large or too small.
        if guess < searched_number:
            m.stdin.write("too small")
        elif guess > searched_number:
            m.stdin.write("too large")
        elif guess == searched_number:
            m.stdin.write("correct")
            found = True

    # If program didn't find the solution fast enough,
    # notify that the program made too many guesses.
    assert found, (
        "Program made too many guesses.\n" +
        "Guesses were: {}".format(guesses))
