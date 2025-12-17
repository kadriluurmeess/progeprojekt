# Importimised:

import tkinter as tk
from tkinter import messagebox, ttk
import random
import os
import re
import unicodedata
import difflib
from datetime import datetime
try:
    from sõnastik import SÕNASTIK
except Exception:
    SÕNASTIK = None
try:
    from mängutulemused import add_result, get_results
except Exception:
    add_result = None
    get_results = None


# GUI klass:

class SõnaMängGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hispaania keele õppemäng")
        self.root.geometry("600x700")
        
        # GUI klassi isendimuutujad:
        self.tase = 1
        self.sõnastik = {}
        self.õppimise_sõnad = []
        self.testi_sõnad = []
        self.praegune_index = 0
        self.skoor = 0
        self.max_punktid = 0
        self.olek = "menu"
        self.session_start = None
        self.valed_sõnad = []  
        
        # Andmete laadimine:
        self.lae_sõnastik()
        
        # UI loomine:
        self.loo_ui()
        
    def lae_sõnastik(self):
        """Sõnastiku laadimine moodulist"""
        if SÕNASTIK is None:
            messagebox.showerror("Viga", "sõnastik.SÕNASTIK ei ole saadaval!")
            self.sõnastik = {}
        else:
            self.sõnastik = SÕNASTIK
            
    def loo_ui(self):
        """UI loomine"""
        # Päis
        self.paiseframe = tk.Frame(self.root, bg="#2563eb", height=60)
        self.paiseframe.pack(fill="x")
        self.paiseframe.pack_propagate(False)
        
        tk.Label(self.paiseframe, text="Hispaania keele õppemäng", 
                font=("Arial", 18, "bold"), bg="#2563eb", fg="white").pack(pady=15)
        
        # Põhisisu kast
        self.sisu_frame = tk.Frame(self.root, bg="white")
        self.sisu_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.näita_menüüd()
        
    def puhasta_sisu(self):
        """Puhastab sisu"""
        for widget in self.sisu_frame.winfo_children():
            widget.destroy()
            
    def näita_menüüd(self):
        """Näitab peamenüüd"""
        self.puhasta_sisu()
        self.olek = "menu"
        
        tk.Label(self.sisu_frame, text="Tere tulemast!", 
                font=("Arial", 24, "bold"), bg="white").pack(pady=10)
        
        tk.Label(self.sisu_frame, text="Õpi hispaania keelt tasemete kaupa", 
                font=("Arial", 12), bg="white", fg="gray").pack(pady=3)
        
        # Taseme valiku nupud
        tk.Label(self.sisu_frame, text="Tasemed:", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
        
        nupud_tasemed = tk.Frame(self.sisu_frame, bg="white")
        nupud_tasemed.pack(pady=5)
        
        # Saadaolevad tasemed
        saadaolevad_tasemed = sorted([int(k) for k in self.sõnastik.keys() if k.isdigit()])
        for tase_nr in saadaolevad_tasemed:
            btn_text = str(tase_nr)
            btn_color = "#10b981" if tase_nr == self.tase else "#94a3b8"
            tk.Button(nupud_tasemed, text=btn_text, font=("Arial", 12, "bold"),
                     bg=btn_color, fg="white", width=4, height=1,
                     command=lambda t=tase_nr: self.vaheta_tase(t)).pack(side="left", padx=5)
        
        # Nuppude kast
        nupud_frame = tk.Frame(self.sisu_frame, bg="white")
        nupud_frame.pack(pady=20)
        
        # "Alusta" nupp
        tk.Button(nupud_frame, text="Alusta õppimist", 
                 font=("Arial", 14), bg="#10b981", fg="white",
                 command=self.alusta_õppimist, width=20, height=2).pack(pady=5)
        
        # Statistika nupp
        tk.Button(nupud_frame, text="Statistika", 
                 font=("Arial", 12), bg="#2563eb", fg="white",
                 command=self.näita_statistikat, width=20, height=1).pack(pady=5)
    
    def vaheta_tase(self, uus_tase):
        """Vahetab taseme ja värskendab menüüd"""
        self.tase = uus_tase
        self.näita_menüüd()
    
    def alusta_õppimist(self):
        """Õppima hakkamine"""
        taseme_andmed = self.sõnastik.get(str(self.tase), {})
        
        if not taseme_andmed:
            messagebox.showinfo("Info", f"Tase {self.tase} puudub!")
            return
        self.session_start = datetime.now()
        self.valed_sõnad = []  # Uuesti valesti vastatud sõnad
            
        # Kogu kõik sõnad sellelt tasemelt
        self.õppimise_sõnad = []
        for kategooria, sõnade_list in taseme_andmed.items():
            for sõna_obj in sõnade_list:
                sõna_obj['_kategooria'] = kategooria
                self.õppimise_sõnad.append(sõna_obj)
                
        self.praegune_index = 0
        self.olek = "õppimise"
        self.näita_õppimise_kaarti()
        
    def näita_õppimise_kaarti(self):
        """Näita õppimise kaarti (sõna ja tõlge)"""
        self.puhasta_sisu()
        
        if self.praegune_index >= len(self.õppimise_sõnad):
            # Õppimine läbi, mine testima
            self.alusta_testi()
            return
            
        sõna = self.õppimise_sõnad[self.praegune_index]
        
        tk.Label(self.sisu_frame, text=f"ÕPPIMINE - Tase {self.tase}", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
                
        tk.Label(self.sisu_frame, text=f"Sõna {self.praegune_index + 1} / {len(self.õppimise_sõnad)}", 
                font=("Arial", 10), bg="white", fg="gray").pack()
                
        # Kategooria
        tk.Label(self.sisu_frame, text=f" {sõna.get('_kategooria', '').upper()}", 
                font=("Arial", 11), bg="white", fg="#8b5cf6").pack(pady=10)
        
        # Hispaania sõna
        tk.Label(self.sisu_frame, text=sõna.get('sõna', ''), 
                font=("Arial", 28, "bold"), bg="white", fg="#2563eb").pack(pady=20)
                
        # Eestikeelne tõlge
        tk.Label(self.sisu_frame, text="→", font=("Arial", 18), bg="white").pack()
        tk.Label(self.sisu_frame, text=sõna.get('tõlge', ''), 
                font=("Arial", 24, "bold"), bg="white", fg="#10b981").pack(pady=20)
        
        # Nupud
        nupu_frame = tk.Frame(self.sisu_frame, bg="white")
        nupu_frame.pack(pady=30)
        
        if self.praegune_index > 0:
            tk.Button(nupu_frame, text="← Eelmine", command=self.eelmine_õppimise_sõna,
                     font=("Arial", 11)).grid(row=0, column=0, padx=10)
        
        järgmise_tekst = "Järgmine →" if self.praegune_index < len(self.õppimise_sõnad) - 1 else "Alusta testi"
        tk.Button(nupu_frame, text=järgmise_tekst, command=self.järgmine_õppimise_sõna,
                 font=("Arial", 11), bg="#10b981", fg="white").grid(row=0, column=1, padx=10)
                 
    def eelmine_õppimise_sõna(self):
        """Mine eelmise sõna juurde."""
        if self.praegune_index > 0:
            self.praegune_index -= 1
            self.näita_õppimise_kaarti()
            
    def järgmine_õppimise_sõna(self):
        """Mine järgmise sõna juurde."""
        self.praegune_index += 1
        self.näita_õppimise_kaarti()
        
    def alusta_testi(self):
        """Alusta testimist"""
        self.olek = "test"
        self.testi_sõnad = self.õppimise_sõnad.copy()
        random.shuffle(self.testi_sõnad)
        self.praegune_index = 0
        self.skoor = 0
        self.max_punktid = len(self.testi_sõnad)
        self.valed_sõnad = []  # Taasta valesti vastatud sõnad
        self.näita_testi_küsimust()
        
    def näita_testi_küsimust(self):
        """Näita küsimust"""
        self.puhasta_sisu()
        
        if self.praegune_index >= len(self.testi_sõnad):
            # Test läbi
            self.näita_tulemust()
            return
            
        sõna = self.testi_sõnad[self.praegune_index]
        
        tk.Label(self.sisu_frame, text=f"TEST - Tase {self.tase}", 
                font=("Arial", 14, "bold"), bg="white", fg="#2563eb").pack(pady=10)
                
        tk.Label(self.sisu_frame, text=f"Küsimus {self.praegune_index + 1} / {len(self.testi_sõnad)}", 
                font=("Arial", 10), bg="white", fg="gray").pack()
                
        tk.Label(self.sisu_frame, text=f"Punktid: {self.skoor} / {self.max_punktid}", 
                font=("Arial", 12, "bold"), bg="white", fg="#10b981").pack(pady=10)
        
        # Küsimus
        tk.Label(self.sisu_frame, text=sõna.get('sõna', ''), 
                font=("Arial", 26, "bold"), bg="white", fg="#2563eb").pack(pady=30)
                
        tk.Label(self.sisu_frame, text="Mis on selle sõna tõlge eesti keeles?", 
                font=("Arial", 11), bg="white", fg="gray").pack()
        
        # Sisestusväli
        self.vastuse_entry = tk.Entry(self.sisu_frame, font=("Arial", 16), width=25)
        self.vastuse_entry.pack(pady=20)
        self.vastuse_entry.focus()
        self.vastuse_entry.bind('<Return>', lambda e: self.kontrolli_vastust())
        
        # "Kontrolli" nupp
        tk.Button(self.sisu_frame, text="Kontrolli", command=self.kontrolli_vastust,
                 font=("Arial", 12), bg="#10b981", fg="white", width=15).pack(pady=10)
                 
        # Tagasiside silt
        self.tagasiside_silt = tk.Label(self.sisu_frame, text="", 
                                       font=("Arial", 12, "bold"), bg="white")
        self.tagasiside_silt.pack(pady=10)
        
    def normalize(self, s: str) -> str:
        """Normaliseerib teksti vastuste võrdlemiseks: madaldab tähed, eemaldab täpitähed, eemaldab kirjavahemärgid."""
        if not isinstance(s, str):
            return ""
        s = s.lower().strip()
        s = unicodedata.normalize('NFKD', s)
        s = ''.join(ch for ch in s if not unicodedata.combining(ch))
        s = re.sub(r"[^\w\s]", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def is_correct(self, user: str, expected: str, synonyms: list = None) -> bool:
        """Kontrollib, kas kasutaja vastus on õige. Lubab täpset vastet, sünonüüme, väikseid trükivigu ja sõnade kattuvust."""
        if synonyms is None:
            synonyms = []
        user_n = self.normalize(user)
        if not user_n:
            return False

        candidates = [self.normalize(expected)] + [self.normalize(x) for x in synonyms]

        # Täpne vaste
        if user_n in candidates:
            return True

        # Ligikaudne vaste (trükivead)
        match = difflib.get_close_matches(user_n, candidates, n=1, cutoff=0.78)
        if match:
            return True

        # Osaliselt õige
        exp_tokens = set(self.normalize(expected).split())
        user_tokens = set(user_n.split())
        if exp_tokens and (len(exp_tokens & user_tokens) / max(1, len(exp_tokens)) >= 0.6):
            return True

        return False
    
    def kontrolli_vastust(self):
        """Kasutaja vastuse kontrollimine"""
        if self.praegune_index >= len(self.testi_sõnad):
            return
            
        sõna = self.testi_sõnad[self.praegune_index]
        kasutaja_vastus = self.vastuse_entry.get().strip()
        õige_vastus = sõna.get('tõlge', '')
        synonyms = sõna.get('synonyms', [])
        
        # Võrdlemine
        if self.is_correct(kasutaja_vastus, õige_vastus, synonyms):
            self.skoor += 1
            self.tagasiside_silt.config(text="✓ Õige!", fg="#10b981")
        else:
            self.tagasiside_silt.config(text=f"✗ Vale! Õige: {õige_vastus}", fg="#ef4444")
            # Jälgi valesti vastatud sõnu
            if sõna not in self.valed_sõnad:
                self.valed_sõnad.append(sõna)
            
        self.praegune_index += 1
        self.root.after(1500, self.näita_testi_küsimust)
        
    def näita_tulemust(self):
        """Näita testi tulemus"""
        self.puhasta_sisu()
        
        protsent = (self.skoor / self.max_punktid * 100) if self.max_punktid > 0 else 0
        
        # Kontrolli, kas on vaja valesti vastatud sõnu uuesti õppida
        if self.valed_sõnad and protsent < 100:
            # Näita tulemus, paku võimalust uuesti õppida
            tk.Label(self.sisu_frame, text="📚", font=("Arial", 48), bg="white").pack(pady=20)
            
            tk.Label(self.sisu_frame, text="Test läbitud!", 
                    font=("Arial", 24, "bold"), bg="white").pack(pady=10)
                    
            tk.Label(self.sisu_frame, text=f"Tulemus: {self.skoor} / {self.max_punktid}", 
                    font=("Arial", 18), bg="white").pack(pady=10)
                    
            tk.Label(self.sisu_frame, text=f"{protsent:.1f}%", 
                    font=("Arial", 20, "bold"), bg="white", 
                    fg="#10b981" if protsent >= 80 else "#f59e0b").pack(pady=10)
            
            # Valesti vastatud sõnad
            tk.Label(self.sisu_frame, text=f"Valesti vastatud: {len(self.valed_sõnad)} sõna", 
                    font=("Arial", 14), bg="white", fg="#ef4444").pack(pady=10)
            
            tk.Label(self.sisu_frame, text="Õpime neid sõnu veel kord!", 
                    font=("Arial", 12), bg="white").pack(pady=5)
            
            # Nupp valesti vastatud sõnade uuesti õppimiseks
            tk.Button(self.sisu_frame, text="Õpi valesti vastatud sõnu", 
                     command=self.alusta_valed_õppimist,
                     font=("Arial", 14), bg="#f59e0b", fg="white", width=25, height=2).pack(pady=20)
            
            tk.Button(self.sisu_frame, text="Tagasi menüüsse", command=self.näita_menüüd,
                     font=("Arial", 12)).pack(pady=5)
            
        else:
            # Pole valesti vastatud sõnu
            tk.Label(self.sisu_frame, text="🎉", font=("Arial", 48), bg="white").pack(pady=20)
            
            tk.Label(self.sisu_frame, text="Test läbitud!", 
                    font=("Arial", 24, "bold"), bg="white").pack(pady=10)
                    
            tk.Label(self.sisu_frame, text=f"Tulemus: {self.skoor} / {self.max_punktid}", 
                    font=("Arial", 18), bg="white").pack(pady=10)
                    
            tk.Label(self.sisu_frame, text=f"{protsent:.1f}%", 
                    font=("Arial", 20, "bold"), bg="white", fg="#10b981").pack(pady=10)
            
            # Salvesta tulemus
            self.salvesta_tulemus()
            
            # Kui kõik õiged
            if protsent == 100:
                tk.Label(self.sisu_frame, text="Suurepärane! Kõik vastused õiged!", 
                        font=("Arial", 14, "bold"), bg="white", fg="#10b981").pack(pady=10)
            
            # Nupud
            nupu_frame = tk.Frame(self.sisu_frame, bg="white")
            nupu_frame.pack(pady=30)
            
            if protsent == 100 and str(self.tase + 1) in self.sõnastik:
                tk.Button(nupu_frame, text="Järgmine tase", command=self.järgmine_tase,
                         font=("Arial", 12), bg="#2563eb", fg="white").pack(pady=5)
            
            tk.Button(nupu_frame, text="Korda taset", command=self.alusta_õppimist,
                     font=("Arial", 12)).pack(pady=5)
                     
            tk.Button(nupu_frame, text="Tagasi menüüsse", command=self.näita_menüüd,
                     font=("Arial", 12)).pack(pady=5)
                 
    def alusta_valed_õppimist(self):
        """ Õpi uuesti valesti vastatud sõnu """
        if not self.valed_sõnad:
            messagebox.showinfo("Info", "Pole valesti vastatud sõnu!")
            return
        
        # Valesti vastatud sõnade õppimine
        self.õppimise_sõnad = self.valed_sõnad.copy()
        self.valed_sõnad = [] 
        self.praegune_index = 0
        self.olek = "õppimise"
        self.näita_õppimise_kaarti()
    
    def järgmine_tase(self):
        """Liigu järgmisele tasemele"""
        self.tase += 1
        self.valed_sõnad = [] 
        self.näita_menüüd()
        
    def salvesta_tulemus(self):
        """Salvesta tulemus moodulisse 'mägutulemused'"""
        if add_result is None:
            messagebox.showerror("Viga", "Tulemuste salvestus pole saadaval")
            return
        kestus = None
        if self.session_start:
            kestus = (datetime.now() - self.session_start).total_seconds()
        add_result(self.tase, self.skoor, self.max_punktid, kestus)

    def näita_statistikat(self):
        """Kuva lihtne statistika: keskmine kestus ja protsent."""
        self.puhasta_sisu()
        tk.Label(self.sisu_frame, text="Statistika", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
        if get_results is None:
            tk.Label(self.sisu_frame, text="Tulemused pole saadaval", bg="white").pack(pady=10)
            tk.Button(self.sisu_frame, text="Tagasi", command=self.näita_menüüd).pack(pady=10)
            return
        tulemused = get_results()
        if not tulemused:
            tk.Label(self.sisu_frame, text="Pole ühtegi tulemust veel.", bg="white").pack(pady=10)
            tk.Button(self.sisu_frame, text="Tagasi", command=self.näita_menüüd).pack(pady=10)
            return

        protsendid = [r.get("protsent") for r in tulemused if isinstance(r.get("protsent"), (int, float))]
        kestused = [r.get("kestus_sek") for r in tulemused if isinstance(r.get("kestus_sek"), (int, float))]
        avg_protsent = sum(protsendid) / len(protsendid) if protsendid else 0.0
        avg_kestus = sum(kestused) / len(kestused) if kestused else 0.0

        def fmt_secs(sek):
            mins = int(sek // 60)
            secs = sek - mins * 60
            return f"{mins}m {secs:.1f}s" if sek else "-"

        tk.Label(self.sisu_frame, text=f"Mänge kokku: {len(tulemused)}", font=("Arial", 12), bg="white").pack(pady=5)
        tk.Label(self.sisu_frame, text=f"Keskmine protsent: {avg_protsent:.1f}%", font=("Arial", 12), bg="white").pack(pady=5)
        tk.Label(self.sisu_frame, text=f"Keskmine kestus: {fmt_secs(avg_kestus)}", font=("Arial", 12), bg="white").pack(pady=5)

        tk.Button(self.sisu_frame, text="Tagasi menüüsse", command=self.näita_menüüd,
                 font=("Arial", 12)).pack(pady=15)

#  Programmi käivitamine GUI kaudu
if __name__ == "__main__":
    root = tk.Tk()
    app = SõnaMängGUI(root)
    root.mainloop()