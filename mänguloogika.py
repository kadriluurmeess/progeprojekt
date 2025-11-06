import json, random, time

def lae_sõnad():
    with open("sõnastik.json", "r", encoding="utf-8") as f:
        return json.load(f)

def õpeta_sõnad(sõnad):
    print("\n📚 Õppimisosa - õpime sõnu ükshaaval!")
    print("Vajuta Enter, kui oled valmis järgmise sõna juurde liikuma.\n")

    õpitud = []

    for kategooria, nimekiri in sõnad.items():
        print(f"\n=== Kategooria: {kategooria.upper()} ===")
        for elem in nimekiri:
            print(f"\n✨ Uus sõna: {elem['sõna']}  →  {elem['tõlge']}")
            print(f"Selgitus: {elem['selgitus']}\n")

            print("Näited kasutamiseks:")
            for n in elem["näited"]:
                print(f" • {n}")

            õpitud.append(elem)
            input("\n👉 Vajuta Enter, et minna järgmise sõna juurde...")

    input("\n🎯 Nüüd testime, mis meelde jäi! Vajuta Enter...\n")
    return õpitud

def testi_teadmisi(õpitud):
    print("\n🎯 TESTIOSA - proovime, mis meelde jäi!")
    punktid = 0

    for elem in random.sample(õpitud, len(õpitud)):
        vastus = input(f"\nMida tähendab '{elem['sõna']}' eesti keeles? ").strip().lower()
        if vastus == elem["tõlge"]:
            print("✅ Õige! Tubli!")
            punktid += 1
        else:
            print(f"❌ Vale. Õige vastus: {elem['tõlge']}")
            print("💡 Näide:", random.choice(elem["näited"]))

    print(f"\n🏆 Sinu tulemus: {punktid}/{len(õpitud)} punkti.")

def mäng():
    sõnad = lae_sõnad()
    õpitud_sonad = õpeta_sõnad(sõnad)
    testi_teadmisi(õpitud_sonad)
    print("\nAitäh mängimast! Hasta luego! 👋")
