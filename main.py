"""
Progeprojekt - Hispaania keele õppemäng algajatele
Autorid: Kadri Luurmees, Oskar Martsoo
Allikad: 
Kirjeldus: Lihtne sõnavara õppimise mäng.
"""


from mänguloogika import mäng

def main():
    """
    Kuvab lühikese tervituse ja käivitab `mäng()` funktsiooni mänguloogikast.
    """
    print("🇪🇸 Tere tulemast Hispaania keele õppemängu!")
    print("Tõlgi hispaania keelsed sõnad eesti keelde ja vastupidi.")
    mäng()

if __name__ == "__main__":
    main()