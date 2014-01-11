"""
Task description (in Estonian):

3. Read veergudeks (10p)
On antud tekstifail, kus esimesel real on mingi failinimi ja sellele järgneb n
rida ja igas reas on tühikutega eraldatuna m täisarvu. 

Kirjutada programm, mis loob uue faili, kus on samad arvud teises paigutuses –
esialgse faili esimese rea arvud on uue faili esimeses veerus, teise rea arvud
peavad sattuma teise veergu jne, st. uude faili tuleb m rida, igal real n arvu.
Programm peab algse faili nime küsima kasutajalt. 

Uue faili nimeks peab olema esialgse faili esimesel real olev failinimi. 

Näide: kui kasutaja sisestab failinimeks arvutabel.txt ja faili sisu on nagu 
allpool näidatud, siis peab programmi käivitamisel tekkima uus fail nimega
uus_arvutabel.txt, mille sisu on nagu allpool näidatud:

arvutabel.txt:
    uus_arvutabel.txt
    1 2 3 4
    5 6 7 8
    9 10 -11 12

Tekkinud fail uus_arvutabel.txt:
    1 5 9
    2 6 10
    3 7 -11
    4 8 12

Lihtsustus (-2p): Kui sa faili kirjutamist ei oska, siis kuva uus arvutabel
ekraanile.
"""

from grader import *

def invert(matrix):
    if len(matrix) == 0: return []
    result = []
    for col in range(len(matrix[0])):
        result.append([row[col] for row in matrix])
    return result

def description(d):
    def inner(f):
        setDescription(f, d)
        return f
    return inner

def checker(matrix, outfile_name, infile_name, BASE=None):
    contents = outfile_name+"\n"+"\n".join(" ".join(map(str, rida)) for rida in matrix)
    inverted_matrix = invert(matrix)
    N, M = len(matrix), len(matrix[0]) if matrix else 0

    if BASE is None:
        BASE = "Maatriks {matrix}"

    format_args = {
        "matrix": matrix,
        "inverted_matrix": inverted_matrix,
        "outfile": outfile_name,
        "infile": infile_name,
        "M": M,
        "N": N
    }

    @test
    @description((BASE+" - korrektse nimega väljundfail peaks tekkima").format(**format_args))
    @create_temporary_file(infile_name, contents)
    @after_test(delete_file(outfile_name))
    def get_output_file(m):
        from time import sleep
        m.stdin.write(infile_name)
        sleep(0.01)
        import os
        assert os.path.isfile(outfile_name), (
            "Peaks tekkima samasse kausta fail {} aga ei tekkinud."
            .format(outfile_name)
        )
        return open(outfile_name)

    @test
    @description((BASE+" - väljundfailis/väljundis peab olema {M}x{N} maatriks").format(**format_args))
    @create_temporary_file(infile_name, contents)
    @after_test(delete_file(outfile_name))
    def output_matrix(m):
        try:
            handle = get_output_file(m)
        except AssertionError:
            # use stdout if no file
            handle = m.stdout
        user_output = handle.read()
        lines = user_output.strip().split("\n")
        assert len(lines) == M, (
            "Tulemusfailis peaks olema {} rida.\nKasutaja väljund: {}"
            .format(M, repr(user_output)))
        rows = [line.split() for line in lines]
        if len(lines) > 0:
            assert all(len(row) == N for row in rows), (
                "Tulemusfailis peaks olema igal real {} veergu.\nKasutaja väljund: {}"
                .format(N, repr(user_output)))
        return rows, user_output

    @test
    @description((BASE+" - väljundfailis/väljundis korrektne inverteeritud maatriks").format(**format_args))
    @create_temporary_file(infile_name, contents)
    @after_test(delete_file(outfile_name))
    def check_output_matrix(m):
        from pprint import pformat
        no_int_matrix, _ = output_matrix(m)
        int_matrix = [[int(v) for v in row] for row in no_int_matrix]
        assert int_matrix == inverted_matrix, (
            "Tulemuseks saadud maatriks peaks olema algse maatriksi inverteeritud"
            "variant.\nKasutaja väljastatud maatriks:\n{}"
            .format(pformat(int_matrix)))


    @test
    @description((BASE+" - väljundfail/väljundis on rida-realt täpne").format(**format_args))
    @create_temporary_file(infile_name, contents)
    @after_test(delete_file(outfile_name))
    def check_output_accurate(m):
        expected_output = "\n".join(" ".join(map(str, rida)) for rida in inverted_matrix)
        _, user_output = output_matrix(m)
        user_output = user_output.strip()
        assert user_output == expected_output, (
            "\nOodatud väljund:  {}"
            "\nKasutaja väljund: {}"
            .format(repr(expected_output), repr(user_output)))


checker([[1, 2, 3], [5, 6, -7], [10, 11, 12]], "uus_arvutabel.txt", "arvutabel.txt")
checker([[1, 99, -9]], "uus_arvutabel.txt", "arvutabel.txt")
checker([[1, 2], [4, 5], [7, 8]], "mingi_teine_sisendfail.txt", "arvutabel.txt", 
    BASE="Maatriks {matrix}, teine sisendfail")
checker([[1, 99, -9]], "uus_arvutabel.txt", "mingi_teine_valjundfail.txt", 
    BASE="Maatriks {matrix}, teine väljunfail")