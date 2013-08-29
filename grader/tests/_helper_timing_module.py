from time import sleep 

def some_slow_function_that_prints_result(a, b):
    sleep(0.3)
    return "result"

a = input() 
b = input()
print(some_slow_function_that_prints_result(a, b))