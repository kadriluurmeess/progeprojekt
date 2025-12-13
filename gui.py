import tkinter as tk
from tkinter import messagebox
import json
import random
import os
from datetime import datetime

class SonaMangGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sõnaõppe Mäng")
        self.root.geometry("400x350")
        
        # Mängu muutujad
        self.skoor = 0
        self.elud = 3
        self.sonastik = {}
        self.praegune_sona = None
        self.oige_vastus = None
        
        # Laeme andmed
        self.lae_sonastik()
        
        # --- Kujunduse elemendid (Widgets) ---
        
        # Skoori ja elude silt
        self.staatus_silt = tk.Label(root, text=f"Skoor: {self.skoor} | Elud: {self.elud}", font=("Arial", 12))
        self.staatus_silt.pack(pady=10)
        
        # Küsimuse silt
        self.kusimus_silt = tk.Label(root, text="Vajuta 'Alusta', et mängida!", font=("Arial", 16, "bold"))
        self.kusimus_silt.pack(pady=20)
        
        # Sisestusväli
        self.sisestus = tk.Entry(root, font=("Arial", 14))
        self.sisestus.pack(pady=5)
        # Seome Enter klahvi vastuse kontrollimisega
        self.root.bind('<Return>', lambda event: self.kontrolli_vastust())
        
        # Nupud
        self.kontrolli_nupp = tk.Button(root, text="Kontrolli vastust", command=self.kontrolli_vastust, bg="#4CAF50", fg="white")
        self.kontrolli_nupp.pack(pady=5)
        
        self.uus_mangu_nupp = tk.Button(root, text="Alusta / Järgmine sõna", command=self.uus_sona)
        self.uus_mangu_nupp.pack(pady=5)
        
        # Tagasiside silt (Õige/Vale)
        self.tagasiside_silt = tk.Label(root, text="", font=("Arial", 10))
        self.tagasiside_silt.pack(pady=10)

    def lae_sonastik(self):
        """Loeb sõnad keerukama struktuuriga failist sõnastik.json"""
        failinimi = "sõnastik.json"
        self.sonastik = {} # Teeme tühja sõnastiku: {hispaania: eesti}

        if os.path.exists(failinimi):
            try:
                with open(failinimi, "r", encoding="utf-8") as f:
                    andmed = json.load(f)
                    
                    # Käime läbi tasemed (nt "1", "2")
                    for tase, kategooriad in andmed.items():
                        # Käime läbi kategooriad (nt "tervitused", "värvid")
                        for kategooria, sonade_nimekiri in kategooriad.items():
                            # Käime läbi iga sõna nimekirjas
                            for kirje in sonade_nimekiri:
                                hispaania_keeles = kirje["sõna"]
                                eesti_keeles = kirje["tõlge"]
                                # Lisame lihtsustatud sõnastikku
                                self.sonastik[hispaania_keeles] = eesti_keeles
                                
            except Exception as e:
                messagebox.showerror("Viga", f"Viga faili lugemisel: {e}")
                # Tagavara, kui fail on katki
                self.sonastik = {"Hola": "tere", "Adios": "head aega"}
        else:
            messagebox.showwarning("Hoiatus", "Faili sõnastik.json ei leitud!")
            self.sonastik = {"Hola": "tere"}

    def uus_sona(self):
        """Valib suvalise sõna sõnastikust"""
        if self.elud <= 0:
            messagebox.showinfo("Mäng läbi", f"Mäng läbi! Sinu lõplik skoor: {self.skoor}")
            self.salvesta_tulemus()
            self.nulli_mang()
            return

        if not self.sonastik:
            self.kusimus_silt.config(text="Sõnastik on tühi!")
            return

        # Võtame suvalise sõna (võti) ja selle tõlke (väärtus)
        # NB: Sõltub sinu JSONi struktuurist. Siin eeldame: "Eesti": "Inglise"
        self.praegune_sona = random.choice(list(self.sonastik.keys()))
        self.oige_vastus = self.sonastik[self.praegune_sona]
        
        # Uuendame kasutajaliidest
        self.kusimus_silt.config(text=f"Tõlgi sõna: {self.praegune_sona}")
        self.sisestus.delete(0, tk.END) # Tühjendame sisestusvälja
        self.tagasiside_silt.config(text="")
        self.sisestus.focus() # Paneme kursor kasti

    def kontrolli_vastust(self):
        """Kontrollib, kas sisestatud vastus on õige"""
        if not self.praegune_sona:
            return # Mäng pole veel alanud

        kasutaja_vastus = self.sisestus.get().strip()

        # Kontrollime (tõstutundetu)
        if kasutaja_vastus.lower() == self.oige_vastus.lower():
            self.skoor += 1
            self.tagasiside_silt.config(text="Õige! Tubli töö.", fg="green")
            self.root.after(1000, self.uus_sona) # 1 sekundi pärast uus sõna automaatselt
        else:
            self.elud -= 1
            self.tagasiside_silt.config(text=f"Vale! Õige oli: {self.oige_vastus}", fg="red")
            
        self.uuenda_skoori_silti()
        
        if self.elud <= 0:
            self.root.after(1500, lambda: messagebox.showinfo("Mäng läbi", f"Said otsa! Skoor: {self.skoor}"))
            self.root.after(1500, self.salvesta_tulemus)
            self.root.after(1500, self.nulli_mang)

    def uuenda_skoori_silti(self):
        self.staatus_silt.config(text=f"Skoor: {self.skoor} | Elud: {self.elud}")

    def nulli_mang(self):
        self.skoor = 0
        self.elud = 3
        self.uuenda_skoori_silti()
        self.kusimus_silt.config(text="Vajuta 'Alusta', et uuesti proovida")
        self.praegune_sona = None

    def salvesta_tulemus(self):
        """Salvestab tulemuse faili mängutulemused.json"""
        tulemus = {
            "mängija_nimi": "Mängija", # Hiljem võid lisada nime küsimise
            "skoor": self.skoor,
            "voit": False, # Lihtne loogika
            "kuupaev": datetime.now().strftime("%Y-%m-%d"),
            "kell": datetime.now().strftime("%H:%M")
        }
        
        failinimi = "mängutulemused.json"
        olemasolevad_andmed = []
        
        if os.path.exists(failinimi):
            try:
                with open(failinimi, "r", encoding="utf-8") as f:
                    olemasolevad_andmed = json.load(f)
            except:
                pass # Kui fail on katki, alustame tühjalt
        
        olemasolevad_andmed.append(tulemus)
        
        with open(failinimi, "w", encoding="utf-8") as f:
            json.dump(olemasolevad_andmed, f, indent=4)
        print("Tulemus salvestatud!")

# --- Programmi käivitamine ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SonaMangGUI(root)
    root.mainloop()