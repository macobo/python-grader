# järgmisele võimalusele näidetes ei viidata, aga ülesande tekst lubab
def paiguta(n):
    if n == 0:
        return []
    else:
        return [True, paiguta(n-1)]


