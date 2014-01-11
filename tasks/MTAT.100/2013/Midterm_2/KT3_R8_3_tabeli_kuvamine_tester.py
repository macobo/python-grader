"""
Task description (in Estonian):

3. Tabeli kuvamine (12p)
On antud fail tulemused.csv, mille sisu tuleb ekraanile kuvada vormindatud
tabelina. Faili esimesel real on antud veergude nimed ning ülejäänud ridadel
tabeli sisu. 

Veeru nimi (koos tühikutega) on vähemalt sama pikk kui ükskõik mis selle veeru
väärtus (vajadusel on lisatud lõppu tühikuid).

    Nt. kui tulemused.csv sisu on
    Nimi         ,Sünniaasta,Elukoht  ,Punkte
    Karl,1991,Türi,73
    Ants,1978,Tallinn,89
    Juulius,1939,Tartu,90

siis tuleb ekraanile kuvada tabel, kus veeru laius sõltub failis antud veeru
nime pikkusest (arvestades ka tühikuid):
    ---------------------------------------------------
    | Nimi          | Sünniaasta | Elukoht   | Punkte |
    ---------------------------------------------------
    | Karl          | 1991       | Türi      | 73     |
    | Ants          | 1978       | Tallinn   | 89     |
    | Juulius       | 1939       | Tartu     | 90     |
    ---------------------------------------------------


Et programm oleks kasulik, peab lahendus töötama suvalise sellise csv faili
korral (ei tohi eeldada, et failis on 4 veergu).

Vihje1: Programm
    print("tere", end="")
    print("tore")
kuvab ekraanile teretore.

Vihje2: 
    >>> "a" * 7
    'aaaaaaa'

Lihtsustus (-4p): Võib eeldada, et failis on veeru andmed alati sama pikad kui
veeru nimi. Sel juhul tuleks kasutada faili tulemused_lihtsam.csv.

Alternatiivne lihtsustus (-5p): Kõik veerud võib teha laiusega 15 ja võib
eeldada, et ükski infojupp pole pikem kui 13 sümbolit.

Lihtsustus (-3p): Tabeli kuvamisel ei ole vaja eristada veergude nimede rida
ülejäänud ridadest.
"""

from grader import *

def description(d):
    def inner(f):
        setDescription(f, d)
        return f
    return inner

# esiteks, kas kõik vajalikud asjad väljundis
# teiseks, kas vaheread olemas
# kolmandaks, muude ridade peal vaatame kas neid on õige arv, 
#             kas kriipsud neis olemas piisaval arvul, kas igaühe vahel sõna
# neljandaks, kas IO on üksühele sama (miinus lõpust \n jne)

TESTS = [
    ({
        "Nimi         ": ["Karl", "Ants", "Juulius"],
        "Sünniaasta":   ["1991", "1978", "1939"],
        "Elukoht  ":    ["Türi", "Tallinn", "Tartu"],
        "Punkte":       ["73", "89", "90"]
    }, "Näitesisend"),

    ({
        'Sünd         ': ['1962         ', '1983         ', '1991         ', '1970         ', '1967         '], 
        'Perenimi     ': ['Lepik        ', 'Koppel       ', 'Kaasik       ', 'Ilves        ', 'Mihhailov    '], 
        'Eesnimi      ': ['Jekaterina   ', 'Joanna       ', 'Kornelius    ', 'Kärt         ', 'Kai          ']
    }, "Kõik veerud on pikkusega 13"),

    ({
        'Sünd      ':   ['1966', '1983', '1968', '1984', '1973'], 
        'Perenimi   ':  ['Pärn', 'Petrov', 'Kaasik', 'Vasiliev', 'Lepik'], 
        'Eesnimi      ': ['Knud', 'Joosep', 'Kalmar', 'Josias', 'Jekaterina']
    }, "Veerud eri pikkustega"),

    ({
        'Perenimi  ': ['Andreev', 'Pavlov', 'Mägi', 'Semenov', 'Sepp', 'Lepik', 'Saar', 'Pärn', 'Raudsepp', 'Kaasik'], 
        'Eesnimi   ': ['Kornelius', 'Kärt', 'Kornili', 'Kaspar', 'Josias', 'Kate', 'Kalmar', 'Knud', 'Katariina', 'Joosep'], 
        'Sünd      ': ['1962', '1979', '1991', '1978', '1991', '1988', '1962', '1968', '1990', '1974'], 
        'Tulemus   ': ['127915563', '50494497', '155015854', '43712995', '182306115', '159527443', '10578093', '177650890', '90490302', '154466925']
    }, "Pikk tabel, veerud sama pikad")
]

def input_table(testcase):
    join_line = lambda parts: ",".join(map(str, parts))

    headers = sorted(testcase.keys())
    n = len(testcase[headers[0]])

    result = [join_line(headers)]
    for i in range(n):
        result.append(join_line(testcase[h][i] for h in headers))
    return "\n".join(result)

def output_table(file_contents):
    lines = file_contents.split('\n')
    kriips = ""
    pais, lines = lines[0].split(','), lines[1:]
    for veerg in pais:
        kriips += "-" * (len(veerg) + 3)
    kriips += '-'

    output = [kriips]
    output.append("".join("| "+h+" " for h in pais) + "|")
    output.append(kriips)
    for rida in lines:
        veerud = rida.strip().split(',')
        rida = ""
        for i in range(len(veerud)):
            veerg = veerud[i]
            rida += "| " + veerg.ljust(len(pais[i])) + " "
        output.append(rida + "|")
    output.append(kriips)
    return "\n".join(output)

def table_lines(output):
    lines = output.strip().split('\n')
    no_with_dashes = 0
    result = []
    for line in lines:
        if "---" in line:
            no_with_dashes += 1
        else:
            result.append(line)
    return result, no_with_dashes

@test
@create_temporary_file('tulemused.csv', input_table(TESTS[0][0]))
@description("Näitesisend - kasutatakse tulemus.csv faili")
def using_correct_file(m): pass

def checker(testcase, BASE):
    file_contents = input_table(testcase)

    @test
    @create_temporary_file("tulemused.csv", file_contents)
    @create_temporary_file("tulemused_lihtsam.csv", file_contents)
    @description((BASE + " - kõik sisendis olevad andmed peavad kusagil väljundis leiduma"))
    def test_everything_in_input(m):
        output = m.stdout.read()
        not_in_output = set()
        for header, values in testcase.items():
            h = header.strip()
            if h not in output: not_in_output.add(h)
            not_in_output |= {v.strip() for v in values if v.strip() not in output}
        assert len(not_in_output) == 0, (
            "Ei leidnud kasutaja väljundist sõnu {}\n"
            "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
            .format(not_in_output, output, file_contents))

    def get_header_index(output):
        headers = [h.strip() for h in testcase.keys()]
        for i, line in enumerate(output.split('\n')):
            if all(h in line for h in headers):
                return i

        assert False, (
            "Ei leidnud päist\n"
            "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
            .format(output, file_contents))

    @test
    @create_temporary_file("tulemused.csv", file_contents)
    @create_temporary_file("tulemused_lihtsam.csv", file_contents)
    @description((BASE + " - peab olema täpselt 3 rida kriipsudega, üks kohe pärast päist"))
    def test_dashed_lines(m):
        output = m.stdout.read().strip()
        lines = output.split('\n')
        header_index = get_header_index( output)
        assert header_index > 0, (
            "Päis asus esimesel real.\n"
            "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
            .format(output, file_contents))

        assert table_lines(output)[1] == 3, (
            "Täpselt 3 rida kus on ainult kriipsud peab leiduma.\n"
            "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
            .format(output, file_contents))
        
        is_dashed = lambda line: "----" in line
        assert is_dashed(lines[header_index-1]) and is_dashed(lines[header_index+1]), (
            "Päise ümber on joontega ümbritsetud read\n"
            "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
            .format(output, file_contents))

    @test
    @create_temporary_file("tulemused.csv", file_contents)
    @create_temporary_file("tulemused_lihtsam.csv", file_contents)
    @description((BASE + " - püstkriipsud päises enne iga sõna"))
    def test_header_separated(m):
        output = m.stdout.read().strip()
        header_index = get_header_index(output)
        header = output.split('\n')[header_index]
        parts = header.split("|")[1:-1] # skip last borders
        assert len(parts) == len(testcase.items()), (
            "Päises peab olema {} püstkriipsu\n"
            "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
            .format(output, file_contents))

    @test
    @create_temporary_file("tulemused.csv", file_contents)
    @create_temporary_file("tulemused_lihtsam.csv", file_contents)
    @description((BASE + " - püstkriipsud peavad olema kohakuti"))
    def test_borders(m):
        output = m.stdout.read().strip()
        lines = output.split('\n')
        header_index = get_header_index(output)
        dash_indeces = [i for i in range(len(lines[header_index])) if lines[header_index][i] == "|"]
        assert dash_indeces, (
            "Päises peab olema eraldaja, | märk"
            "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
            .format(output, file_contents))
        
        for j in range(header_index+1, len(lines)):
            if "|" not in lines[j]: continue
            indeces = [i for i in range(len(lines[j])) if lines[j][i] == "|"]
            assert indeces == dash_indeces, (
                "Real {} ei asu eraldajad samal kohal mis päises"
                "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
                .format((j, lines[j]), output, file_contents))

    @test
    @create_temporary_file("tulemused.csv", file_contents)
    @create_temporary_file("tulemused_lihtsam.csv", file_contents)
    @description((BASE + " - täpne väljundi kontroll"))
    def test_exact(m):
        output = m.stdout.read().strip()
        expected = output_table(file_contents)
        assert output == expected, (
            "Väljundid polnud täpselt samad.\nOotasime:\n{}\n\n"
            "Kasutaja väljund:\n{}\n\nSisendfail:\n{}"
            .format(expected, output, file_contents))


for testcase, desc in TESTS:
    #print(input_table(testcase))
    checker(testcase, desc)