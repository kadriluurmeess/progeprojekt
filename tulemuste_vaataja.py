"""
tulemuste_vaataja.py - Mängutulemuste analüsaator

See programm loeb mängutulemused.json faili ja kuvab statistikat:
- Üldine areng aja jooksul
- Tulemus tasemete kaupa
- Parimad ja nõrgemad tulemused

Autorid: Kadri Luurmees, Oskar Martsoo
Faili kodeering: UTF-8
Viimane muutmine: 2025-12-15
"""

import json
import os
from datetime import datetime
from collections import defaultdict


def lae_tulemused():
    """
    Lae mängutulemused JSON-failist.
    
    Returns:
        list: Tulemuste list või tühi list kui faili pole.
    """
    failinimi = "mängutulemused.json"
    
    if not os.path.exists(failinimi):
        print(f"❌ Ei leidnud faili: {failinimi}")
        print("   Mängi mõni mäng enne tulemuste vaatamist!")
        return []
    
    try:
        with open(failinimi, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("❌ Viga faili lugemisel - fail võib olla vigane.")
        return []


def kuva_üldstatistika(tulemused):
    """Kuva üldine statistika kõigi mängude kohta."""
    if not tulemused:
        print("\n📊 Tulemused puuduvad.")
        return
    
    print("\n" + "=" * 60)
    print("📊 ÜLDSTATISTIKA")
    print("=" * 60)
    
    kokku_mänge = len(tulemused)
    kokku_punktid = sum(t.get('punktid', 0) for t in tulemused)
    kokku_max = sum(t.get('max_punktid', 0) for t in tulemused)
    keskmine = (kokku_punktid / kokku_max * 100) if kokku_max > 0 else 0
    
    print(f"\n🎮 Mänge kokku: {kokku_mänge}")
    print(f"⭐ Punkte kogutud: {kokku_punktid} / {kokku_max}")
    print(f"📈 Keskmine tulemus: {keskmine:.1f}%")
    
    # Leia parim tulemus
    if tulemused:
        parim = max(tulemused, key=lambda x: x.get('protsent', 0))
        print(f"🏆 Parim tulemus: {parim['protsent']}% (Tase {parim['tase']}, {parim['kuupäev']})")


def kuva_tasemete_statistika(tulemused):
    """Kuva statistika tasemete kaupa."""
    if not tulemused:
        return
    
    print("\n" + "=" * 60)
    print("📊 STATISTIKA TASEMETE KAUPA")
    print("=" * 60)
    
    # Grupeeri tasemete kaupa
    tasemed = defaultdict(list)
    for t in tulemused:
        tasemed[t.get('tase', 0)].append(t)
    
    for tase in sorted(tasemed.keys()):
        tulemus_list = tasemed[tase]
        mänge = len(tulemus_list)
        keskmine = sum(t.get('protsent', 0) for t in tulemus_list) / mänge if mänge > 0 else 0
        parim = max(t.get('protsent', 0) for t in tulemus_list) if tulemus_list else 0
        
        print(f"\n📌 TASE {tase}:")
        print(f"   Mänge: {mänge}")
        print(f"   Keskmine: {keskmine:.1f}%")
        print(f"   Parim: {parim:.1f}%")


def kuva_areng(tulemused, limit=10):
    """Kuva viimased tulemused kronoloogilises järjekorras."""
    if not tulemused:
        return
    
    print("\n" + "=" * 60)
    print(f"📈 VIIMASED {min(limit, len(tulemused))} TULEMUST")
    print("=" * 60)
    
    # Võta viimased tulemused
    viimased = tulemused[-limit:] if len(tulemused) > limit else tulemused
    
    print(f"\n{'Kuupäev':<20} {'Tase':<8} {'Tulemus':<15} {'%':<8}")
    print("-" * 60)
    
    for t in viimased:
        kuupaev = t.get('kuupäev', 'N/A')
        tase = t.get('tase', '?')
        punktid = t.get('punktid', 0)
        max_punktid = t.get('max_punktid', 0)
        protsent = t.get('protsent', 0)
        
        print(f"{kuupäev:<20} {tase:<8} {punktid}/{max_punktid:<12} {protsent:.1f}%")


def kuva_edusammud(tulemused):
    """Analüüsi ja kuva edusamme."""
    if len(tulemused) < 2:
        print("\n⚠️  Liiga vähe tulemusi edusammude analüüsimiseks (vaja vähemalt 2).")
        return
    
    print("\n" + "=" * 60)
    print("🎯 EDUSAMMUD")
    print("=" * 60)
    
    # Võrdle esimest ja viimast tulemust
    esimene = tulemused[0]
    viimane = tulemused[-1]
    
    esimene_protsent = esimene.get('protsent', 0)
    viimane_protsent = viimane.get('protsent', 0)
    
    muutus = viimane_protsent - esimene_protsent
    
    print(f"\n📅 Esimene mäng: {esimene['kuupäev']} - {esimene_protsent:.1f}%")
    print(f"📅 Viimane mäng: {viimane['kuupäev']} - {viimane_protsent:.1f}%")
    
    if muutus > 0:
        print(f"\n🚀 Paranemine: +{muutus:.1f}% punkti! Tubli!")
    elif muutus < 0:
        print(f"\n📉 Langus: {muutus:.1f}% punkti. Ära anna alla!")
    else:
        print(f"\n➡️  Stabiilne: {viimane_protsent:.1f}%")
    
    # Leia kui palju on 100% tulemusi
    täielikud = sum(1 for t in tulemused if t.get('protsent', 0) == 100)
    print(f"\n✨ Täielikke sooritusi (100%): {täielikud} / {len(tulemused)}")


def peamenüü():
    """Põhiprogramm."""
    print("\n" + "=" * 60)
    print("🎮 HISPAANIA ÕPPEMÄNGU TULEMUSTE VAATAJA")
    print("=" * 60)
    
    tulemused = lae_tulemused()
    
    if not tulemused:
        print("\n❌ Tulemused puuduvad. Mängi esmalt mõni mäng!")
        return
    
    while True:
        print("\n" + "-" * 60)
        print("MENÜÜ:")
        print("  1 - Üldstatistika")
        print("  2 - Statistika tasemete kaupa")
        print("  3 - Viimased tulemused")
        print("  4 - Edusammud")
        print("  5 - Kõik statistikad korraga")
        print("  0 - Välju")
        print("-" * 60)
        
        valik = input("\nSinu valik: ").strip()
        
        if valik == "1":
            kuva_üldstatistika(tulemused)
        elif valik == "2":
            kuva_tasemete_statistika(tulemused)
        elif valik == "3":
            kuva_areng(tulemused, limit=15)
        elif valik == "4":
            kuva_edusammud(tulemused)
        elif valik == "5":
            kuva_üldstatistika(tulemused)
            kuva_tasemete_statistika(tulemused)
            kuva_areng(tulemused, limit=10)
            kuva_edusammud(tulemused)
        elif valik == "0":
            print("\n👋 Nägemist!")
            break
        else:
            print("\n❌ Vale valik. Proovi uuesti.")


if __name__ == "__main__":
    peamenüü()
