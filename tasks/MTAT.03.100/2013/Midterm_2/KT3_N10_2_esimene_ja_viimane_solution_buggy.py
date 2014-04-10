# siin tekib probleem tühja listiga
def esimene_ja_viimane(lst):
    if not isinstance(lst, list):
        return lst
    return [esimene_ja_viimane(lst[0]), esimene_ja_viimane(lst[-1])]
