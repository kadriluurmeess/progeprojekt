"""
gui.py - Graafiline kasutajaliides hispaania õppemängule

Sisaldab tasemepõhise õppimise ja testimise:
- Esmalt õppimisrežiim (näitab sõnu)
- Seejärel testimine
- Tasemete süsteem

Autorid: Kadri Luurmees, Oskar Martsoo
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
import os
import re
import unicodedata
import difflib
from datetime import datetime

class SonaMangGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🇪🇸 Hispaania keele õppemäng")
        self.root.geometry("600x500")
        
        # Mängu muutujad
        self.tase = 1
        self.sonastik = {}
        self.oppimise_sonad = []
        self.testi_sonad = []
        self.praegune_index = 0
        self.skoor = 0
        self.max_punktid = 0
        self.olek = "menu"  # menu, oppimise, test
        
        # Laeme andmed
        self.lae_sonastik()
        
        # Loo UI
        self.loo_ui()
        
    def lae_sonastik(self):
        """Lae sõnastik failist."""
        failinimi = "sõnastik.json"
        if os.path.exists(failinimi):
            try:
                with open(failinimi, "r", encoding="utf-8") as f:
                    self.sonastik = json.load(f)
            except Exception as e:
                messagebox.showerror("Viga", f"Viga faili lugemisel: {e}")
        else:
            messagebox.showerror("Viga", "sõnastik.json ei leitud!")
            
    def loo_ui(self):
        """Loo põhiline kasutajaliides."""
        # Päis
        self.paiseframe = tk.Frame(self.root, bg="#2563eb", height=60)
        self.paiseframe.pack(fill="x")
        self.paiseframe.pack_propagate(False)
        
        tk.Label(self.paiseframe, text="🇪🇸 Hispaania keele õppemäng", 
                font=("Arial", 18, "bold"), bg="#2563eb", fg="white").pack(pady=15)
        
        # Põhisisu konteiner
        self.sisu_frame = tk.Frame(self.root, bg="white")
        self.sisu_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.naita_menu()
        
    def puhasta_sisu(self):
        """Eemalda kõik vidinad sisu_frame'ist."""
        for widget in self.sisu_frame.winfo_children():
            widget.destroy()
            
    def naita_menu(self):
        """Näita peamenüüd."""
        self.puhasta_sisu()
        self.olek = "menu"
        
        tk.Label(self.sisu_frame, text="Tere tulemast!", 
                font=("Arial", 24, "bold"), bg="white").pack(pady=30)
        
        tk.Label(self.sisu_frame, text="Õpi hispaania keelt tasemete kaupa", 
                font=("Arial", 12), bg="white", fg="gray").pack(pady=10)
        
        # Taseme valik
        tk.Label(self.sisu_frame, text=f"Praegune tase: {self.tase}", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=20)
        
        # Alusta nupp
        tk.Button(self.sisu_frame, text="📚 Alusta õppimist", 
                 font=("Arial", 14), bg="#10b981", fg="white",
                 command=self.alusta_oppimist, width=20, height=2).pack(pady=10)
                 
    def alusta_oppimist(self):
        """Alusta õppimisrežiimi praegusel tasemel."""
        taseme_andmed = self.sonastik.get(str(self.tase), {})
        
        if not taseme_andmed:
            messagebox.showinfo("Info", f"Tase {self.tase} puudub!")
            return
            
        # Kogu kõik sõnad sellelt tasemelt
        self.oppimise_sonad = []
        for kategooria, sonade_list in taseme_andmed.items():
            for sona_obj in sonade_list:
                sona_obj['_kategooria'] = kategooria
                self.oppimise_sonad.append(sona_obj)
                
        self.praegune_index = 0
        self.olek = "oppimise"
        self.naita_oppimise_kaart()
        
    def naita_oppimise_kaart(self):
        """Näita õppimise kaarti (sõna ja tõlge)."""
        self.puhasta_sisu()
        
        if self.praegune_index >= len(self.oppimise_sonad):
            # Õppimine läbi, mine testimisse
            self.alusta_testi()
            return
            
        sona = self.oppimise_sonad[self.praegune_index]
        
        tk.Label(self.sisu_frame, text=f"📚 ÕPPIMINE - Tase {self.tase}", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
                
        tk.Label(self.sisu_frame, text=f"Sõna {self.praegune_index + 1} / {len(self.oppimise_sonad)}", 
                font=("Arial", 10), bg="white", fg="gray").pack()
                
        # Kategooria
        tk.Label(self.sisu_frame, text=f"📂 {sona.get('_kategooria', '').upper()}", 
                font=("Arial", 11), bg="white", fg="#8b5cf6").pack(pady=10)
        
        # Hispaania sõna
        tk.Label(self.sisu_frame, text=sona.get('sõna', ''), 
                font=("Arial", 28, "bold"), bg="white", fg="#2563eb").pack(pady=20)
                
        # Tõlge
        tk.Label(self.sisu_frame, text="→", font=("Arial", 18), bg="white").pack()
        tk.Label(self.sisu_frame, text=sona.get('tõlge', ''), 
                font=("Arial", 24, "bold"), bg="white", fg="#10b981").pack(pady=20)
        
        # Nupud
        nupu_frame = tk.Frame(self.sisu_frame, bg="white")
        nupu_frame.pack(pady=30)
        
        if self.praegune_index > 0:
            tk.Button(nupu_frame, text="← Eelmine", command=self.eelmine_oppimise_sona,
                     font=("Arial", 11)).grid(row=0, column=0, padx=10)
        
        jargmise_tekst = "Järgmine →" if self.praegune_index < len(self.oppimise_sonad) - 1 else "Alusta testi ✓"
        tk.Button(nupu_frame, text=jargmise_tekst, command=self.jargmine_oppimise_sona,
                 font=("Arial", 11), bg="#10b981", fg="white").grid(row=0, column=1, padx=10)
                 
    def eelmine_oppimise_sona(self):
        """Mine eelmise sõna juurde."""
        if self.praegune_index > 0:
            self.praegune_index -= 1
            self.naita_oppimise_kaart()
            
    def jargmine_oppimise_sona(self):
        """Mine järgmise sõna juurde."""
        self.praegune_index += 1
        self.naita_oppimise_kaart()
        
    def alusta_testi(self):
        """Alusta testimist."""
        self.olek = "test"
        self.testi_sonad = self.oppimise_sonad.copy()
        random.shuffle(self.testi_sonad)
        self.praegune_index = 0
        self.skoor = 0
        self.max_punktid = len(self.testi_sonad)
        self.naita_testi_kusimus()
        
    def naita_testi_kusimus(self):
        """Näita testi küsimust."""
        self.puhasta_sisu()
        
        if self.praegune_index >= len(self.testi_sonad):
            # Test läbi
            self.naita_tulemust()
            return
            
        sona = self.testi_sonad[self.praegune_index]
        
        tk.Label(self.sisu_frame, text=f"📝 TEST - Tase {self.tase}", 
                font=("Arial", 14, "bold"), bg="white", fg="#2563eb").pack(pady=10)
                
        tk.Label(self.sisu_frame, text=f"Küsimus {self.praegune_index + 1} / {len(self.testi_sonad)}", 
                font=("Arial", 10), bg="white", fg="gray").pack()
                
        tk.Label(self.sisu_frame, text=f"Punktid: {self.skoor} / {self.max_punktid}", 
                font=("Arial", 12, "bold"), bg="white", fg="#10b981").pack(pady=10)
        
        # Küsimus
        tk.Label(self.sisu_frame, text=sona.get('sõna', ''), 
                font=("Arial", 26, "bold"), bg="white", fg="#2563eb").pack(pady=30)
                
        tk.Label(self.sisu_frame, text="Mis on selle sõna tõlge eesti keeles?", 
                font=("Arial", 11), bg="white", fg="gray").pack()
        
        # Sisestusväli
        self.vastuse_entry = tk.Entry(self.sisu_frame, font=("Arial", 16), width=25)
        self.vastuse_entry.pack(pady=20)
        self.vastuse_entry.focus()
        self.vastuse_entry.bind('<Return>', lambda e: self.kontrolli_vastust())
        
        # Kontrolli nupp
        tk.Button(self.sisu_frame, text="✓ Kontrolli", command=self.kontrolli_vastust,
                 font=("Arial", 12), bg="#10b981", fg="white", width=15).pack(pady=10)
                 
        # Tagasiside silt
        self.tagasiside_silt = tk.Label(self.sisu_frame, text="", 
                                       font=("Arial", 12, "bold"), bg="white")
        self.tagasiside_silt.pack(pady=10)
        
    def kontrolli_vastust(self):
        """Kontrolli kasutaja vastust."""
        if self.praegune_index >= len(self.testi_sonad):
            return
            
        sona = self.testi_sonad[self.praegune_index]
        kasutaja_vastus = self.vastuse_entry.get().strip()
        oige_vastus = sona.get('tõlge', '')
        
        # Lihtne võrdlus (võib laiendada normalize funktsiooniga)
        if kasutaja_vastus.lower() == oige_vastus.lower():
            self.skoor += 1
            self.tagasiside_silt.config(text="✓ Õige!", fg="#10b981")
        else:
            self.tagasiside_silt.config(text=f"✗ Vale! Õige: {oige_vastus}", fg="#ef4444")
            
        self.praegune_index += 1
        self.root.after(1500, self.naita_testi_kusimus)
        
    def naita_tulemust(self):
        """Näita testi tulemust."""
        self.puhasta_sisu()
        
        protsent = (self.skoor / self.max_punktid * 100) if self.max_punktid > 0 else 0
        
        tk.Label(self.sisu_frame, text="🎉", font=("Arial", 48), bg="white").pack(pady=20)
        
        tk.Label(self.sisu_frame, text="Test läbitud!", 
                font=("Arial", 24, "bold"), bg="white").pack(pady=10)
                
        tk.Label(self.sisu_frame, text=f"Tulemus: {self.skoor} / {self.max_punktid}", 
                font=("Arial", 18), bg="white").pack(pady=10)
                
        tk.Label(self.sisu_frame, text=f"{protsent:.1f}%", 
                font=("Arial", 20, "bold"), bg="white", 
                fg="#10b981" if protsent >= 80 else "#f59e0b").pack(pady=10)
        
        # Salvesta tulemus
        self.salvesta_tulemus()
        
        # Nupud
        nupu_frame = tk.Frame(self.sisu_frame, bg="white")
        nupu_frame.pack(pady=30)
        
        if protsent == 100 and str(self.tase + 1) in self.sonastik:
            tk.Button(nupu_frame, text="➡️ Järgmine tase", command=self.jargmine_tase,
                     font=("Arial", 12), bg="#2563eb", fg="white").pack(pady=5)
        
        tk.Button(nupu_frame, text="🔄 Korda taset", command=self.alusta_oppimist,
                 font=("Arial", 12)).pack(pady=5)
                 
        tk.Button(nupu_frame, text="🏠 Tagasi menüüsse", command=self.naita_menu,
                 font=("Arial", 12)).pack(pady=5)
                 
    def jargmine_tase(self):
        """Liigu järgmisele tasemele."""
        self.tase += 1
        self.naita_menu()
        
    def salvesta_tulemus(self):
        """Salvesta tulemus JSON-faili."""
        tulemus = {
            "kuupäev": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tase": self.tase,
            "punktid": self.skoor,
            "max_punktid": self.max_punktid,
            "protsent": round((self.skoor / self.max_punktid * 100) if self.max_punktid > 0 else 0, 1)
        }
        
        failinimi = "mängutulemused.json"
        tulemused = []
        
        if os.path.exists(failinimi):
            try:
                with open(failinimi, "r", encoding="utf-8") as f:
                    tulemused = json.load(f)
            except:
                pass
                
        tulemused.append(tulemus)
        
        with open(failinimi, "w", encoding="utf-8") as f:
            json.dump(tulemused, f, indent=4, ensure_ascii=False)

# --- Programmi käivitamine ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SonaMangGUI(root)
    root.mainloop()