# PAIGALDUSJUHEND

## Kiire algus

1. **Kontrolli Python installatsiooni:**
   ```powershell
   python --version
   ```
   Peaks näitama Python 3.8 või uuemat.

2. **Käivita mäng:**
   ```powershell
   python main.py
   ```

3. **Vaata tulemusi:**
   ```powershell
   python tulemuste_vaataja.py
   ```

## Failide ülevaade

| Fail | Kirjeldus | Vajalik |
|------|-----------|---------|
| `main.py` | Põhiprogramm | ✅ Jah |
| `mänguloogika.py` | Mängumootorloogika | ✅ Jah |
| `sõnastik.json` | Sõnavara | ✅ Jah |
| `tulemuste_vaataja.py` | Tulemuste analüsaator | 📊 Soovituslik |
| `mängutulemused.json` | Salvestatud tulemused | 🔄 Automaatne |

## Probleemide lahendamine

### "Ei leidnud faili: sõnastik.json"
**Lahendus:** Veendu, et oled õiges kaustas:
```powershell
cd C:\Users\kadriluurmees\progeprojekt
```

### UTF-8 kodeerimise vead
**Lahendus:** Veendu, et terminalil on UTF-8 tugi:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## Nõuded

- **Python:** 3.8 või uuem
- **Operatsioonisüsteem:** Windows 10/11, Linux, macOS
- **Teegid (kohustuslikud):** json, random, os, re, unicodedata, difflib, datetime (kõik kaasas Pythoniga)
- Programm salvestab tulemused automaatselt
- Sõnastikku saab lihtsalt laiendada (muuda `sõnastik.json`)

---
**Küsimuste korral:** kontrolli README.md või tutvu lähtekoodiga
