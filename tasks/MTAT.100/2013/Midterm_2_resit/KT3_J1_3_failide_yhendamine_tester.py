"""
Task description (in Estonian):

3. Failide ühendamine (10p)
Moodle'is olevas failis andmed.zip on hulk tekstifaile (kõik kodeeringus UTF-8),
mis tuleb oma töökausta lahti pakkida. Failis nimekiri.txt on loetelu 
isikukoodidest.
Failides, mille nimi on kujul <isikukood>.txt on vastava inimese andmed, üks
attribuut ühel real (nt. eesnimi: Peeter).

NB! Erinevates failides võivad olla erinevad attribuudid ja erinevas järjekorras
Ülesandeks on kirjutada programm, mis teisendab sedasi esitatud andmehulga
tabeli formaati, kus igale inimesele vastab üks rida ja igale attribuudile üks
veerg, ning salvestab selle uude faili (kodeeringus UTF-8).

Täpsemalt:

Uue faili nimi ja tabelisse kaasatavate attribuutide loetelu tuleb küsida 
kasutajalt. Kasutaja sisestab attribuutide loetelu ühel real, komadega eraldatuna.

Loodava faili esimesel real peavad olema komadega eraldatuna attribuutide nimed.

Järgmistel ridadel peavad olema failis nimekiri.txt viidatud inimeste vastavad
andmed, jällegi komadega eraldatuna.

Veergude järjekord peab vastama kasutaja poolt sisestatud attribuutide loetelule,
ridade järjekord peab vastama failile nimekiri.txt.

Kui mõne inimese kohta mõnda nõutud attribuuti pole, tuleb vastav koht tabelis
jätta tühjaks.

Näide: Failis andmed.zip olevate näiteandmete korral peab sessioon

    Sisesta uue faili nimi: tabel.txt
    Sisesta attribuutide nimed: eesnimi,e-mail,telefon

tekitama faili nimega tabel.txt, mille sisu on

    eesnimi,e-mail,telefon
    Peeter,,55232123
    Siim,siim.sisalik@gmail.com,
    Kadri,kauniskadri@hot.ee,55233245

Soovitus: alusta andmestiku sisselugemisega sõnastike listi:
    [{'eesnimi': 'Peeter', 'perenimi': 'Punnsilm', ...}, 
     {'eesnimi': 'Siim', ...}, ...].
Kui andmete failidest sisselugemine ei õnnestu, siis kirjuta andmestik sõnastike
listina oma koodi käsitsi sisse ja lahenda ülejäänud ülesanne selle põhjal.

Lihtsustus (-5p): programm ignoreerib kasutaja poolt sisestatud attribuutide
loetelu ja teeb tabeli alati attribuutidega eesnimi,perenimi,sünniaasta.Võib
eeldada, et need attribuudid esinevad kõikide inimeste failides, on alati faili
esimesed attribuudid, ning alati samas järjekorras. Selle lihtsustuse korral ei
ole lähe sõnastikku tarvis.

"""

from grader import *
from KT2_util import *

import os
import os.path
import shutil

def description(d):
    def inner(f):
        setDescription(f, d)
        return f
    return inner

def get_solution_content(veerud):
    andmed = []

    nimekiri = open("nimekiri.txt", encoding="UTF-8")
    for rida in nimekiri:
        f = open(rida.strip() + ".txt", encoding="UTF-8")

        kirje = {}
        for attr in f:
            osad = attr.strip().split(": ")
            kirje[osad[0]] = osad[1]
            
        f.close()
        andmed.append(kirje)

    nimekiri.close()

    uue_faili_sisu = ""
    uue_faili_sisu += veerud + "\n"

    for isik in andmed:
        atts = []
        for veerg in veerud.split(","):
            if veerg in isik:
                atts.append(isik[veerg])
            else:
                atts.append("")

        uue_faili_sisu += ",".join(atts) + "\n"

    return uue_faili_sisu

def normalize_content(s):
    return s.lower().strip().replace(";", ",").replace(", ", ",")

def create_needed_files(test_function):
    codes = [
        35806291243,
        50112244534,
        47803035684,
        47810101010,
        37812121212,
        37811111111
    ]
    data = {35806291243: 'eesnimi: Peeter\nperenimi: Punnsilm\nsünniaasta: 1958\nisanimi: Karl\ntelefon: 55232123\n',
            37811111111: 'eesnimi: Martin\nperenimi: Malakas\nsünniaasta: 1978\n',
            47803035684: 'eesnimi: Kadri\nperenimi: Kaunis\nsünniaasta: 1978\nsilmade värv: sinine\ntelefon: 55233245\ne-mail: kauniskadri@hot.ee\n',
            47810101010: 'eesnimi: Tiia\nperenimi: Tiidus\nsünniaasta: 1978\nhobid: kalastamine\ntelefon: 45345345\ne-mail: tiia@piia.ee\n',
            50112244534: 'eesnimi: Siim\nperenimi: Sisalik\nsünniaasta: 2001\ne-mail: siim.sisalik@gmail.com\n',
            37812121212: 'eesnimi: Martin\nperenimi: Malakas\nsünniaasta: 1978\n'}

    create_temporary_file('nimekiri.txt', "\n".join(map(str, codes)))(test_function)
    for code in codes:
        create_temporary_file(str(code)+".txt", data[code])(test_function)


def register_test(data_folder, out_file_name, attributes, desc):
    
    @test
    @after_test(delete_file(out_file_name))
    @description(desc + ". Attribuudid: " + attributes)
    def test_case(m):
        m.stdin.write(out_file_name)
        m.stdin.write(attributes)

        from time import sleep
        sleep(0.01)

        assert os.path.isfile(out_file_name), "Nõutud faili ei tekkinud"
        
        expected_content = get_solution_content(attributes)
        with open(out_file_name, encoding="UTF-8") as f:
            user_content = f.read()

        if user_content != expected_content:
            msg = "Tekitatud fail erineb oodatavast.\n"
            
            if (normalize_content(user_content)
                == normalize_content(expected_content)):
                msg += "* Erinevus on suur/väiketähtedes või tühikutes või eraldajates.\n"

            elif user_content in expected_content and user_content.count("\n") > 2:
                msg += "* Kasutaja tulemus on osa oodatud tulemusest \n"

            elif expected_content in user_content:
                msg += "* Kasutaja tulemus sisaldab oodatud tulemust (ja midagi veel)\n"

            msg += "* Oodatud tulemus oli:\n" + expected_content + "\n"
            msg += "* Kasutaja tulemus oli:\n" + user_content + "\n"

            raise AssertionError(msg)
    
    # creates all the needed files by decorating    
    create_needed_files(test_case)
        

register_test(
    "KT3_J3_algsed_failid", 
    "tabel.txt",
    "eesnimi,perenimi,sünniaasta",
    "Ülesandes välja toodud lihtne juhtum")

register_test(
    "KT3_J3_algsed_failid",
    "tabel.txt",
    "eesnimi,e-mail,telefon",
    "Ülesandes välja toodud esimene näitejuhtum")

register_test(
    "KT3_J3_teine_komplekt", 
    "tabel2.txt",
    "eesnimi,perenimi,sünniaasta",
    "Suurem andmete komplekt, lihtne juhtum")

register_test(
    "KT3_J3_teine_komplekt", 
    "tabel2.txt",
    "eesnimi,e-mail,telefon",
    "Suurem andmete komplekt")

register_test(
    "KT3_J3_teine_komplekt", 
    "tabel2.txt",
    "eesnimi",
    "Suurem andmete komplekt, üks attribuut")

register_test(
    "KT3_J3_teine_komplekt", 
    "tabel2.txt",
    "qwerwer,asdf,qwer,wert",
    "Suurem andmete komplekt, ainult tundmatud attribuudid")