def keskmised(jarjend):
    uusjarjend=[]
    for i in range(0,len(jarjend)-1):
        keskmine=(jarjend[i]+jarjend[i+1])/2
        if keskmine%1==0:
            keskmine=int(keskmine)
        uusjarjend.append(keskmine)

    return uusjarjend

print(keskmised([1,2,3,4]))
