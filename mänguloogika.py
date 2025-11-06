import json, random

def lae_sõnad():
    with open("sõnastik.json", "r", encoding="utf-8") as f:
        return json.load(f)

def vali_küsimus(sõnad):
    kategooria = random.choice(list(sõnad.keys()))
    sõna, tõlge = random.choice(list(sõnad[kategooria].items()))
    return kategooria, sõna, tõlge

def mäng():
    sõnad = lae_sõnad()
    punktid = 0
    for _ in range(5):  # 5 küsimust
        kategooria, sõna, tõlge = vali_küsimus(sõnad)
        print(f"\nKategooria: {kategooria}")
        vastus = input(f"Mida tähendab sõna '{sõna}' eesti keeles? ")
        if vastus.strip().lower() == tõlge:
            print("✅ Õige!")
            punktid += 1
        else:
            print(f"❌ Vale. Õige vastus on '{tõlge}'.")
    print(f"\nSinu tulemus: {punktid}/5 punkti.")
