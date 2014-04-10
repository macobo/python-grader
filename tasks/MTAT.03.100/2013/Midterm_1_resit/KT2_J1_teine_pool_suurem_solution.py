def teine_pool_suurem(jarjend):
    teisepoolepikkus=len(jarjend)//2
    esimesepoolepikkus=len(jarjend)-teisepoolepikkus
    return sum(jarjend[esimesepoolepikkus:])>sum(jarjend[:esimesepoolepikkus])
