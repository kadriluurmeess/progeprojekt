# Importimised

import random, os, re, unicodedata, difflib
from datetime import datetime

# Sõnastiku laadimine
try:
    from sõnastik import SÕNASTIK
except Exception:
    SÕNASTIK = None

# Mängutulemuste salvestamine
try:
    from mängutulemused import add_result
except Exception:
    add_result = None

# Funktsioonid
def salvesta_tulemus(tase: int, punktid: int, max_punktid: int):
    """ Salvestab mängu tulemuse moodulisse 'mängutulemused'. """
    if add_result is None:
        raise RuntimeError("'mängutulemused.add_result' ei ole saadaval")
    add_result(tase, punktid, max_punktid)

def lae_sõnad():
    """ Laeb sõnad moodulist 'sõnastik'. """
    if SÕNASTIK is None:
        raise RuntimeError("'sõnastik.SÕNASTIK' ei ole saadaval")
    return SÕNASTIK

# Õppimisrežiim
def õpeta_sõnad(sõnad):
    """ Õpetusrežiim: kuvab järjest sõnad ja nende tõlked.
    Funktsioon tagastab listi õpitud sõnadest, millest hiljem tehakse test. """
    print("\n Õpime sõnu!\n")
    
    õpitud = []

    for kategooria, nimekiri in sõnad.items():
        print(f"\n=== Kategooria: {kategooria.upper()} ===")

        for elem in nimekiri:
            sõna = elem.get('sõna', '')
            tõlge = elem.get('tõlge', '')
            print(f"\n Uus sõna: {sõna}  →  {tõlge}")
            
            õpitud.append(elem)
            
            input(" Vajuta Enter, et minna järgmise sõna juurde...")

    input("\n Nüüd testime, mis meelde jäi! Vajuta Enter...\n")
    return õpitud

# Testirežiim
def testi_teadmisi(õpitud):
    """ Testib kasutaja teadmisi õpitud sõnade põhjal. """
    #print("\n TESTIOSA - proovime, mis meelde jäi!")
    punktid = 0
    valed = []
    


    def normalize(s: str) -> str:
        """ Normaliseerib teksti vastuste võrdlemiseks: madaldab tähed, eemaldab täpitähed, eemaldab kirjavahemärgid. """
        if not isinstance(s, str):
            return ""
        s = s.lower().strip()
        s = unicodedata.normalize('NFKD', s)
        s = ''.join(ch for ch in s if not unicodedata.combining(ch))
        s = re.sub(r"[^\w\s]", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def is_correct(user: str, expected: str, synonyms: list[str] | None = None) -> bool:
        """ Kontrollib, kas kasutaja vastus on õige. Lubab täpset vastet, sünonüüme, väikseid trükivigu ja sõnade kattuvust. """
        if synonyms is None:
            synonyms = []
        user_n = normalize(user)
        if not user_n:
            return False

        candidates = [normalize(expected)] + [normalize(x) for x in synonyms]

        # Täpne vaste
        if user_n in candidates:
            return True

        # Ligikaudne vaste (trükivead)
        match = difflib.get_close_matches(user_n, candidates, n=1, cutoff=0.78)
        if match:
            return True

        # Osaliselt õige
        exp_tokens = set(normalize(expected).split())
        user_tokens = set(user_n.split())
        if exp_tokens and (len(exp_tokens & user_tokens) / max(1, len(exp_tokens)) >= 0.6):
            return True

        return False

    # Testime sõnu juhuslikus järjekorras
    for elem in random.sample(õpitud, len(õpitud)):
        küsimus = elem.get('sõna', '')
        õige_vastus = elem.get('tõlge', '')
        vastus = input(f"\nMida tähendab '{küsimus}' eesti keeles? ").strip()
        synonyms = elem.get("synonyms") if isinstance(elem, dict) else None

        if is_correct(vastus, õige_vastus, synonyms):
            print(" Õige! Tubli!")
            punktid += 1
        else:
            print(f" Vale. Õige vastus: {õige_vastus}")
            valed.append(elem)

    print(f"\n Sinu tulemus: {punktid}/{len(õpitud)} punkti.")
    return punktid, valed

# Mängu põhiloogika
def mäng():
    """
    Mängu põhifunktsioon.
    Loogika: laeb sõnastiku, läbib tasemed, õpetab sõnad, testib, kordab valesid sõnu; tase läbitud ainult siis kui 100%.
    """
    sõnastik = lae_sõnad()
    tase = 1

    while True:
        if str(tase) not in sõnastik:
            print("\n Palju õnne! Kõik tasemed on läbitud!")
            break

        print(f"\n TASE {tase}")
        taseme_sonad = sõnastik[str(tase)]

        # Õppimine
        õpitud = õpeta_sõnad(taseme_sonad)

        while True:
            punktid1, valed1 = testi_teadmisi(õpitud)

            punktid = punktid1
            max_punktid = len(õpitud)

            # Leia kõik valed sõnad
            valed = []
            valed_ids = set()
            for v in valed1:
                v_id = v.get('sõna', '')
                if v_id not in valed_ids:
                    valed_ids.add(v_id)
                    valed.append(v)

            if punktid == max_punktid:
                print(f"\n Tase {tase} sooritatud 100%!" )
                salvesta_tulemus(tase, punktid, max_punktid)
                tase += 1
                input(f" Vajuta Enter, et liikuda tasemele {tase}...\n")
                break
            else:
                # Õpime uuesti ainult need, mis läksid valesti
                print(f"\n🔁 Õpime uuesti {len(valed)} sõna, mis läksid valesti.\n")
                salvesta_tulemus(tase, punktid, max_punktid)
                õpitud = valed  # Jätkame ainult valede sõnadega
            # Õpperežiim uuesti valede sõnadega
            õpitud = õpeta_sõnad({"valesti läksid": valed})
