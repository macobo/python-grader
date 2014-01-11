"""
Task description (in Estonian):

2. Valimisnimekirjade tipud (10p)
Failis tartu.csv (kodeering UTF-8) on 2013.a. KOV valimiste põhjal Tartu 
linnavolikokku pääsenud inimeste andmed koos saadud häälte arvudega. 
Failis tallinn.csv on samalaadne info Tallinna volikogu kohta. Kirjuta programm,
mis küsib kasutajalt failinime ja väljastab faili sisu põhjal ekraanile kõikide
erinevate valimisnimekirjade nimetused koos vastavas nimekirjas kõige enam hääli
saanud inimese nime ja tema poolt kogutud häälte arvuga. 

Väljundi täpset formaati vaata järgnevast näitest.

Näide: kui kasutaja sisestab tartu.csv, peavad ekraanile ilmuma järgnevad read
(võivad olla teises järjekorras):

    MARGUS TSAHKNA (Erakond Isamaa ja Res Publica Liit) - 3260 häält
    URMAS KRUUSE (Eesti Reformierakond) - 5292 häält
    HELJO PIKHOF (Sotsiaaldemokraatlik Erakond) - 1733 häält
    GEA KANGILASKI (Valimisliit Vabakund) - 670 häält
    TÕNIS LUKAS (Isamaaline Tartu Kodanik - Valimisliit) - 891 häält
    AADU MUST (Eesti Keskerakond) - 1259 häält
"""

from grader import *
from KT2_util import *

def vote_counter(filename):
    with open(filename, encoding="utf-8") as f:
        f.readline()
        votes = {}
        for line in f:
            erakond, haaled, nr, nimi = line.strip().split(",")
            if erakond not in votes or int(haaled) > votes[erakond]["votes"]:
                votes[erakond] = {"votes": int(haaled), "name": nimi}
    return votes

def checker(description, follow_func, filename="_tartu.csv"):
    #if description is None:
    #    description = "Fail {filename}, aasta {year} on üks järgnevatest: {result}"
    expected = vote_counter(filename)

    description = description.format(
        filename = filename)

    contents = open(filename).read()

    @test
    @create_temporary_file('valimised.csv', contents)
    @timeout(3)
    def test_function(m):
        m.stdout.reset()
        m.stdin.write('valimised.csv')
        follow_func(m.stdout.read().split('\n'), expected)

    setDescription(test_function, description)

def find_erakond(line, votes):
    x = [e for e in votes.keys() if e in line]
    if len(x) == 0: return None
    assert len(x) == 1, "Ainult 1 erakond tohib esineda reas. Rida: {}, leitud erakonnad: {}".format(repr(line), x)
    return x[0]

def check_contains_winner(line, votes):
    erakond = find_erakond(line, votes)
    winner = votes[erakond]["name"]
    require_contains(line, winner, "Erakonna {erakond} võitja {what} peaks esinema reas {input}!", erakond=erakond)

def check_contains_votes(line, votes):
    erakond = find_erakond(line, votes)
    vote_count = votes[erakond]["votes"]
    require_contains(line, str(vote_count), "Erakonna {erakond} võitja häälte arv {what} peaks esinema reas {input}!", erakond=erakond)

def check_formatting(line, votes):
    erakond = find_erakond(line, votes)
    winner = votes[erakond]["name"]
    vote_count = votes[erakond]["votes"]
    correct_message = "{winner} ({erakond}) - {vote_count} häält".format(**locals())
    require_contains(line, correct_message, "Rida {input} peaks olema {what}")

def check_all_present(lines, votes):
    result = set()
    not_found = set(votes.keys())
    for line in lines:
        a = find_erakond(line, votes)
        if a is not None: 
            result.add(line)
            not_found.remove(a)
    assert len(not_found) == 0, "Kõikide erakondade tulemused peab väljastama. Ei leitud tulemusi erakondadele: {}".format(not_found)
    return result

def election_checker(*function_list):
    def inner(lines, votes):
        #assert False, lines
        lines = check_all_present(lines, votes)
        for line in lines:
            for fun in function_list:
                fun(line, votes)
    return inner

for filename in ["_tartu.csv", "_tallinn.csv"]:
    checker("Iga erakonna kohta peab olema üks rida - {filename}", 
        election_checker(), filename)
    checker("Iga erakonna võitja peab olema oma erakonna real - {filename}", 
        election_checker(check_contains_winner), filename)
    checker("Iga erakonna võitja häälte arv peab olema erakonna real - {filename}", 
        election_checker(check_contains_votes), filename)
    checker("Ridade vormistamine - {filename}", 
        election_checker(check_formatting), filename)