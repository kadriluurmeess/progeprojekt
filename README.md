# Hispaania Keele Õppemäng

**Autorid:** Kadri Luurmees, Oskar Martsoo  
**Kursus:** Programmeerimine (Tartu Ülikool)  
**Aasta:** 2025

## 📝 Projekti kirjeldus

Interaktiivne konsoolimäng hispaania keele sõnavara õppimiseks ja harjutamiseks. Programm pakub erinevaid raskusastmeid ja kahepoolset tõlkimist (ESP↔EST).

## ✨ Funktsioonid

### Põhifunktsioonid
- ✅ **Tasemepõhine õppimine** - sõnavara on jagatud kategooriatesse ja tasemetesse
- ✅ **Kahepoolne tõlkimine** - mäng testib nii ESP→EST kui EST→ESP suunas
- ✅ **Sünonüümide tugi** - aktsepteerib erinevaid õigeid vastuseid
- ✅ **Vastuste normaliseerimine** - lubab väikeseid trükivigu ja erineval kirjutamist
- ✅ **Tulemuste salvestamine** - kõik tulemused salvestatakse JSON-faili
- ✅ **Tulemuste analüsaator** - eraldi programm statistika ja arengu vaatamiseks
- ✅ **Vale-vastuste kordamine** - valesti läinud sõnad korratakse läbi

## 🚀 Kasutamine

### Põhimängu käivitamine
```powershell
python main.py
```

### Tulemuste vaatamine
```powershell
python tulemuste_vaataja.py
```


## 📁 Projektstruktuur

```
progeprojekt/
├── main.py                  # Põhiprogramm (käivituspunkt)
├── mänguloogika.py          # Mängumootorloogika
├── tulemuste_vaataja.py     # Tulemuste analüsaator
├── sõnastik.json            # Sõnavara andmebaas
├── mängutulemused.json      # Salvestatud tulemused
└── README.md                # See fail
```

## 🎮 Kuidas mängida

1. **Õppimisfaas**: programm näitab sulle sõnu ja tõlkeid

2. **Test 1 (ESP→EST)**: tõlgi hispaania keelsed sõnad eesti keelde

3. **Test 2 (EST→ESP)**: tõlgi eesti keelsed sõnad hispaania keelde

4. **Kordamine**: kui said valesid vastuseid, korratakse ainult neid sõnu

5. **Järgmine tase**: 100% tulemusel liigud automaatselt järgmisele tasemele

## 📊 Tulemuste vaataja

Tulemuste analüsaatori funktsioonid:
- Üldstatistika (kokku mänge, punkte, keskmine)
- Statistika tasemete kaupa
- Viimaste tulemuste ajalugu
- Edusammude analüüs (võrdleb esimest ja viimast)

## 🛠️ Tehnilised detailid

### Kasutatud teegid
- `json` - andmete salvestamine ja laadimine
- `random` - sõnade segamine testides
- `unicodedata` ja `re` - tekstinormaliseerimine
- `difflib` - hägusa vastusevastavuse kontroll
- `datetime` - tulemuste ajatemplid

### Andmestruktuur (sõnastik.json)
```json
{
  "1": {
    "kategooria": [
      {
        "sõna": "hola",
        "tõlge": "tere",
        "synonyms": ["hei", "tere!"]
      }
    ]
  }
}
```

## 📈 Edasiarendus (plaanis)

- [ ] Kontekstipõhised küsimused (lünktekstid valikvariantidega)
- [ ] Graafiline kasutajaliides (tkinter)
- [ ] Rohkem tasemeid ja sõnu
- [ ] Graafikud ja visuaalsed statistikad

## 🤝 Koostöö ja rollid

Koostöö on sujunud, kuid rolle oleks paremini saanud jagada. Siiani me ei andnud otseselt kindlaid ülesandeid üksteisele või ei jaganud ajaliselt ära kui palju mõlemad teevad. Kokkuvõttes saime ühele lainele ja tegelesime mõlemad programmiga umbes 8-9 tundi.