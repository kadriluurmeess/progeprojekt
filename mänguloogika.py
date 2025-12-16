"""
Sisaldab mängu põhiloogikat: sõnade laadimist, õppimise ja testimise
vooge, vastuste normaliseerimist ja tulemuste salvestamist moodulisse.
"""

import random, os, re, unicodedata, difflib
from datetime import datetime
try:
    from sõnastik import SONASTIK
except Exception:
    SONASTIK = None
try:
    from mängutulemused import add_result
except Exception:
    add_result = None

def salvesta_tulemus(tase: int, punktid: int, max_punktid: int):
    """Salvesta mängu tulemus mängutulemused-moodulisse."""
    if add_result is None:
        raise RuntimeError("'mängutulemused.add_result' ei ole saadaval")
    add_result(tase, punktid, max_punktid)

def lae_sõnad():
    """Tagasta sõnastik moodulist `sõnastik.SONASTIK`."""
    if SONASTIK is None:
        raise RuntimeError("'sõnastik.SONASTIK' ei ole saadaval")
    return SONASTIK

def õpeta_sõnad(sõnad):
    """
    Õpetusrežiim: kuvab järjest sõnad ja nende tõlked.

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
            sõna = elem.get('sõna', '')
            tõlge = elem.get('tõlge', '')
            print(f"\n✨ Uus sõna: {sõna}  →  {tõlge}")
            
            õpitud.append(elem)
            
            input("👉 Vajuta Enter, et minna järgmise sõna juurde...")

    input("\n🎯 Nüüd testime, mis meelde jäi! Vajuta Enter...\n")
    return õpitud

def testi_teadmisi(õpitud, suund="esp_est"):
    """
    Testi-edastus: küsib kasutajalt õpitud sõnade tõlkeid ning hindab vastuseid.

    Args:
        õpitud (list): List sõna-objektidest, mille põhjal test toimub.
        suund (str): Tõlke suund - "esp_est" (hispaania→eesti) või "est_esp" (eesti→hispaania).

    Returns:
        tuple: (punktid, valed) kus `punktid` on õigete vastuste arv ja `valed`
               on list sõna-objektidest, mille vastused olid valed.
    """
    #print("\n🎯 TESTIOSA - proovime, mis meelde jäi!")
    punktid = 0
    valed = []
    
    # Näita suunda kasutajale
    if suund == "est_esp":
        print("\n🔄 Tõlgi nüüd EESTI keelest HISPAANIA keelde!\n")

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
        # Vali küsimuse suund
        if suund == "est_esp":
            # Küsi hispaania keelset tõlget eesti sõna kohta
            küsimus = elem.get('tõlge', '')
            õige_vastus = elem.get('sõna', '')
            vastus = input(f"\nKuidas on '{küsimus}' hispaania keeles? ").strip()
            # Hispaania keeles pole sünonüüme, seega None
            synonyms = None
        else:
            # Tavapärane: küsi eesti keelset tõlget hispaania sõna kohta
            küsimus = elem.get('sõna', '')
            õige_vastus = elem.get('tõlge', '')
            vastus = input(f"\nMida tähendab '{küsimus}' eesti keeles? ").strip()
            # Sõnastikus võib olla valikuline 'synonyms' väli
            synonyms = elem.get("synonyms") if isinstance(elem, dict) else None

        if is_correct(vastus, õige_vastus, synonyms):
            print("✅ Õige! Tubli!")
            punktid += 1
        else:
            print(f"❌ Vale. Õige vastus: {õige_vastus}")
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
            # Esimene test: hispaania → eesti
            print("\n📝 TEST 1: Hispaania → Eesti")
            punktid1, valed1 = testi_teadmisi(õpitud, suund="esp_est")
            
            # Teine test: eesti → hispaania
            print("\n📝 TEST 2: Eesti → Hispaania")
            punktid2, valed2 = testi_teadmisi(õpitud, suund="est_esp")
            
            # Kogu punktid ja valed sõnad
            punktid = punktid1 + punktid2
            max_punktid = len(õpitud) * 2  # Kaks testi
            
            # Leia kõik unikaalsed valed sõnad
            valed = []
            valed_ids = set()
            for v in valed1 + valed2:
                v_id = v.get('sõna', '')
                if v_id not in valed_ids:
                    valed_ids.add(v_id)
                    valed.append(v)

            if punktid == max_punktid:
                # Kui kõik õiged mõlemas testis, salvestame tulemuse ja liigume edasi
                print(f"\n✅ Tase {tase} sooritatud 100%!" )
                salvesta_tulemus(tase, punktid, max_punktid)
                tase += 1
                input(f"👉 Vajuta Enter, et liikuda tasemele {tase}...\n")
                break
            else:
                # Õpime uuesti ainult need, mis läksid valesti
                print(f"\n🔁 Õpime uuesti {len(valed)} sõna, mis läksid valesti.\n")
                salvesta_tulemus(tase, punktid, max_punktid)
                õpitud = valed  # Jätkame ainult valede sõnadega
            # Õpperežiim uuesti valede sõnadega
            õpitud = õpeta_sõnad({"valesti läksid": valed})
