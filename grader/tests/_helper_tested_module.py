name = input()
# test builtins
print("Hi,",name, max(5, 6))

def add_one(x):
    print("Got",x)
    return x + 1

def slow_function(a):
    from time import sleep
    sleep(0.2)
    return a

def askInput():
    a = input()
    print(slow_function(a))

def raiseException(msg):
    raise Exception(msg)