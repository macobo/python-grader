# binary search
top = 10000
bottom = 1

while True:
    mid = (top + bottom) // 2
    print(mid)
    
    answer = input() # ask the user for feedback
    if answer == "too large":
        top = mid - 1
    elif answer == "too small":
        bottom = mid + 1
    elif answer == "correct":
        break