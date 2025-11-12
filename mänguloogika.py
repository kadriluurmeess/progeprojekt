"""
Sisaldab mängu põhiloogikat: sõnade laadimist, õppimise ja testimise
vooge, vastuste normaliseerimist ja tulemuste salvestamist JSON-faili (veel ei tööta).
"""

import json, random, os, re, unicodedata, difflib
from datetime import datetime

def salvesta_tulemus(tase: int, punktid: int, max_punktid: int):
    """
    Salvesta mängu tulemus JSON-faili.

    Args:
        tase (int): Käesolev tase, mille skoor salvestatakse.
        punktid (int): Mängija saavutatud punktid.
        max_punktid (int): Taseme maksimaalsed punktid.

    """
    failinimi = "mängutulemused.json"
    
    # Loe olemasolevad tulemused või loo tühi list
    if os.path.exists(failinimi):
        try:
            with open(failinimi, "r", encoding="utf-8") as f:
                tulemused = json.load(f)
        except json.JSONDecodeError:
            tulemused = []
    else:
        tulemused = []
    
    # Lisa uus tulemus
    uus_tulemus = {
        "kuupäev": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tase": tase,
        "punktid": punktid,
        "max_punktid": max_punktid,
        "protsent": round((punktid / max_punktid * 100) if max_punktid > 0 else 0, 1)
    }
    
    tulemused.append(uus_tulemus)
    
    # Salvesta tulemused faili
    with open(failinimi, "w", encoding="utf-8") as f:
        json.dump(tulemused, f, indent=4, ensure_ascii=False)

def lae_sõnad():
    """
    Lae sõnastikuandmed `sõnastik.json` failist.

    Returns:
        dict: Kaardistus tasemetest ja kategooriatest (str -> dict).

    Raises:
        FileNotFoundError: Kui faili ei leita.
        json.JSONDecodeError: Kui faili sisu ei ole korrektne JSON.
    """
    failinimi = "sõnastik.json"
    if not os.path.exists(failinimi):
        raise FileNotFoundError(f"Ei leidnud faili: {failinimi}")

    with open(failinimi, "r", encoding="utf-8") as f:
        return json.load(f)

def õpeta_sõnad(sõnad):
    """
    Õpetusrežiim: kuvab järjest sõnad ja nende tõlked/hääldused.

    Funktsioon tagastab listi õpitud sõnadest, millest hiljem tehakse test.

    Args:
        sõnad (dict): Taseme või kategooria sõnade struktuur.

    Returns:
        list: Sõnade objektide list, mida kasutab testimisfunktsioon.
    """
    print("\n📚 Õpime sõnu!\n")

    õpitud = []

    for kategooria, nimekiri in sõnad.items():
        print(f"\n=== Kategooria: {kategooria.upper()} ===")

        for elem in nimekiri:
            # Kui sõnal on hääldus, näitame seda õppimise ajal
            hääldus = elem.get('hääldus', '')
            if hääldus:
                print(f"\n✨ Uus sõna: {elem['sõna']} [{hääldus}]  →  {elem['tõlge']}")
            else:
                print(f"\n✨ Uus sõna: {elem['sõna']}  →  {elem['tõlge']}")
            õpitud.append(elem)
            # Ootame kasutaja kinnitust järgmise sõnani liikumiseks
            input("👉 Vajuta Enter, et minna järgmise sõna juurde...")

    input("\n🎯 Nüüd testime, mis meelde jäi! Vajuta Enter...\n")
    return õpitud

def testi_teadmisi(õpitud):
    """
    Testi: küsib kasutajalt õpitud sõnade tõlkeid ning hindab vastuseid.

    Args:
        õpitud (list): List sõnadest, mille põhjal test toimub.

    Returns:
        tuple: (punktid, valed), kus `punktid` on õigete vastuste arv ja `valed`
               on list sõnadest, mille vastused olid valed.
    """
    #print("\n🎯 TESTIOSA - proovime, mis meelde jäi!")
    punktid = 0
    valed = []

    def normalize(s: str) -> str:
        """
        Puhasta tekst vastuste võrdlemiseks.

        Eemaldab diakriitilised märgid, madaldab tähed, eemaldab kirjavahemärgid
        ning tühistab mitmikvahed. 
        """
        if not isinstance(s, str):
            return ""
        s = s.lower().strip()
        # Eemalda diakriitikad (näiteks õ, ä, ñ) võrdlust lihtsustamaks
        s = unicodedata.normalize('NFKD', s)
        s = ''.join(ch for ch in s if not unicodedata.combining(ch))
        # Eemalda kirjavahemärgid, jäta ainult tähed, numbrid ja tühikud
        s = re.sub(r"[^\w\s]", "", s)
        # Ühenda järjest tühikud üheks
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def is_correct(user: str, expected: str, synonyms: list[str] | None = None) -> bool:
        """
        Kontrolli, kas kasutaja vastus on õige.

        Esiteks tehakse normaliseeritud täpne võrdlus ootuse või sünonüümidega.
        Kui täpne vaste puudub, lubatakse väikesed trükivead või vormistuslikud erinevused.
        """
        if synonyms is None:
            synonyms = []
        user_n = normalize(user)
        if not user_n:
            return False

        candidates = [normalize(expected)] + [normalize(x) for x in synonyms]
        # exact normalized match
        if user_n in candidates:
            return True

        # fuzzy match using difflib (tolerate small typos)
        match = difflib.get_close_matches(user_n, candidates, n=1, cutoff=0.78)
        if match:
            return True

        # token overlap: if user's answer contains most of expected words
        exp_tokens = set(normalize(expected).split())
        user_tokens = set(user_n.split())
        if exp_tokens and (len(exp_tokens & user_tokens) / max(1, len(exp_tokens)) >= 0.6):
            return True

        return False

    # Testi sõnad suvalises järjekorras
    for elem in random.sample(õpitud, len(õpitud)):
        vastus = input(f"\nMida tähendab '{elem['sõna']}' eesti keeles? ").strip()

        # Sõnastikus võib olla valikuline 'synonyms' väli — kasuta seda, kui olemas
        synonyms = elem.get("synonyms") if isinstance(elem, dict) else None

        if is_correct(vastus, elem.get("tõlge", ""), synonyms):
            print("✅ Õige! Tubli!")
            punktid += 1
        else:
            print(f"❌ Vale. Õige vastus: {elem.get('tõlge', '')}")
            valed.append(elem)

    print(f"\n🏆 Sinu tulemus: {punktid}/{len(õpitud)} punkti.")
    return punktid, valed

def mäng():
    """
    Mängu põhifunktsioon, mis juhib tasemete ja õppimise/testimise tsüklit.

    Loogika:
    - Laeb sõnastiku failist
    - Iga taseme jaoks näitab esmalt õppimisrežiimi (kõik sõnad)
    - Küsib testi; kui punktid on maksimaalsed, liigub järgmisele tasemele
    - Kui on valesid vastuseid, siis jätkatakse ainult valede sõnade õppimisega kuni õnnestumiseni
    """
    sõnastik = lae_sõnad()
    tase = 1

    while True:
        # Kui järgmine tase puudub, oleme lõpetanud
        if str(tase) not in sõnastik:
            print("\n🎉 Palju õnne! Kõik tasemed on läbitud!")
            break

        print(f"\n TASE {tase}")
        taseme_sonad = sõnastik[str(tase)]

        # Esmane õppimine: läbime kõik taseme sõnad
        õpitud = õpeta_sõnad(taseme_sonad)

        while True:
            punktid, valed = testi_teadmisi(õpitud)

            if punktid == len(õpitud):
                # Kui kõik õiged, salvestame tulemuse ja liigutakse edasi
                print(f"\n✅ Tase {tase} sooritatud 100%!" )
                salvesta_tulemus(tase, punktid, len(õpitud))
                tase += 1
                input(f"👉 Vajuta Enter, et liikuda tasemele {tase}...\n")
                break
            else:
                # Õpime uuesti ainult need, mis läksid valesti
                print("\n🔁 Õpime uuesti sõnad, mis läksid valesti.\n")
                salvesta_tulemus(tase, punktid, len(õpitud))
                õpitud = valed  # Jätkame ainult valede sõnadega
            # Õpperežiim uuesti valede sõnadega
            õpitud = õpeta_sõnad({"valesti läksid": valed})
