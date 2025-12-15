import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import random
from datetime import datetime

# Impordi mänguloogika funktsioonid
from mänguloogika import lae_sõnad, salvesta_tulemus


# Värviskeem
COLORS = {
    'primary': '#2563eb',      # Sinine
    'primary_dark': '#1e40af',
    'secondary': '#10b981',    # Roheline
    'danger': '#ef4444',       # Punane
    'warning': '#f59e0b',      # Oranž
    'bg_main': '#f8fafc',      # Hele hall taust
    'bg_card': '#ffffff',      # Valge kaart
    'text_dark': '#1e293b',    # Tume tekst
    'text_light': '#64748b',   # Hele tekst
    'border': '#e2e8f0',       # Piirjoone värv
    'success': '#22c55e',      # Edu roheline
    'accent': '#8b5cf6',       # Lilla aktsent
}


class ModernButton(tk.Canvas):

    def __init__(self, parent, text, command, bg_color=COLORS['primary'],
                 fg_color='white', width=220, height=60, **kwargs):
        # Lisa rohkem kõrgust ja sisemist serva, et nuppe oleks näha
        padding = 10
        effective_h = height + padding
        super().__init__(parent, width=width, height=effective_h,
                         highlightthickness=0, bg=COLORS['bg_card'], **kwargs)

        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text = text
        self.width = width
        self.height = effective_h
        self.hover = False

        # Loo nupu kujund suurema raadiuse ja sisemise marginaaliga
        margin = 6
        self.rect = self.create_rounded_rect(margin, margin,
                                             width - margin,
                                             effective_h - margin,
                                             radius=14, fill=bg_color, outline='')
        self.text_id = self.create_text(width // 2, effective_h // 2, text=text,
                                        fill=fg_color, font=('Segoe UI', 12, 'bold'))

        # Bind events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Loo ümardatud ristkülik."""
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self, event):
        """Hover efekt."""
        # Kerge heledam toon hoveril
        try:
            self.itemconfig(self.rect, fill=self.bg_color)
        finally:
            self.hover = True
    
    def on_leave(self, event):
        """Taasta tavaline värv."""
        self.itemconfig(self.rect, fill=self.bg_color)
        self.hover = False
    
    def on_click(self, event):
        """Nupu vajutamine."""
        if self.command:
            self.command()


class SpanishLearningGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("🇪🇸 Hispaania keele õppemäng")
        self.root.geometry("960x640")  
        self.root.configure(bg=COLORS['bg_main'])
        
        # Muuda ikoon ja seadistused
        try:
            self.root.iconbitmap('icon.ico')  # Kui on olemas
        except:
            pass
        
        # Lae sõnastik
        try:
            self.sõnastik = lae_sõnad()
            self.levels = sorted([int(k) for k in self.sõnastik.keys()])
        except Exception as e:
            messagebox.showerror("Viga", f"Ei saa laadida sõnastikku:\n{e}")
            self.root.destroy()
            return
        
        # Mänguolek
        self.current_level = 1
        self.current_words = []
        self.current_index = 0
        self.test_mode = None  # 'esp_est' või 'est_esp'
        self.test_score = 0
        self.test_total = 0
        self.test_errors = []
        
        # Loo põhistruktuur
        self.create_header()
        self.create_main_container()
        self.show_home_screen()
    
    def create_header(self):
        """Loo päis."""
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Logo ja pealkiri
        title_font = font.Font(family='Segoe UI', size=24, weight='bold')
        title = tk.Label(header, text="Õpi hispaania keelt!", 
                        font=title_font, bg=COLORS['primary'], fg='white')
        title.pack(side='left', padx=30, pady=20)
        
        # Taseme indikaator
        self.level_label = tk.Label(header, text=f"Tase: {self.current_level}", 
                                    font=('Segoe UI', 14, 'bold'), 
                                    bg=COLORS['primary'], fg='white')
        self.level_label.pack(side='right', padx=20)
    
    def create_main_container(self):
        """Loo põhikonteiner scrollimisega."""
        # Loo scrollimisega konteiner
        canvas = tk.Canvas(self.root, bg=COLORS['bg_main'], highlightthickness=0)
        canvas.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.main_container = tk.Frame(canvas, bg=COLORS['bg_main'])
        canvas_window = canvas.create_window(0, 0, window=self.main_container, anchor='nw')
        
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Uuenda scrollimisala suurus, kui sisu muutub
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
            # Skaaleeri canvas aken kaardi laiusega
            canvas.itemconfig(canvas_window, width=canvas.winfo_width() - 40)
        
        self.main_container.bind('<Configure>', on_frame_configure)
        canvas.bind_all('<MouseWheel>', lambda e: self._on_mousewheel(e, canvas))
    
    def _on_mousewheel(self, event, canvas):
        """Hiire ratta scrollimine."""
        canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
    
    def clear_main_container(self):
        """Puhasta põhikonteiner."""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_home_screen(self):
        """Näita kodulehte."""
        self.clear_main_container()
        
        # alguskiri
        welcome_frame = tk.Frame(self.main_container, bg=COLORS['bg_card'], 
                                relief='flat', bd=0)
        welcome_frame.pack(pady=15, padx=50, fill='x')
        
        welcome_font = font.Font(family='Segoe UI', size=28, weight='bold')
        welcome = tk.Label(welcome_frame, text="Tere tulemast!", 
                          font=welcome_font, bg=COLORS['bg_card'], 
                          fg=COLORS['text_dark'])
        welcome.pack(pady=10)
        
        subtitle = tk.Label(welcome_frame, 
                          text="Õpi hispaania keelt mänguliselt ja tõhusalt",
                          font=('Segoe UI', 14), bg=COLORS['bg_card'], 
                          fg=COLORS['text_light'])
        subtitle.pack(pady=(0, 10))
        
        # Taseme valik
        level_frame = tk.Frame(self.main_container, bg=COLORS['bg_main'])
        level_frame.pack(pady=10)
        
        tk.Label(level_frame, text="Vali tase:", font=('Segoe UI', 14, 'bold'),
                bg=COLORS['bg_main'], fg=COLORS['text_dark']).pack(side='left', padx=10)
        
        self.level_var = tk.StringVar(value=str(self.current_level))
        level_combo = ttk.Combobox(level_frame, textvariable=self.level_var,
                                  values=[str(l) for l in self.levels],
                                  state='readonly', font=('Segoe UI', 12),
                                  width=10)
        level_combo.pack(side='left', padx=10)
        level_combo.bind('<<ComboboxSelected>>', self.on_level_change)
        
        # Nupud (vähendame suurust ja paddingi, et kõik mahuks ekraani)
        button_frame = tk.Frame(self.main_container, bg=COLORS['bg_main'])
        button_frame.pack(pady=10, expand=True)
        
        # Õppimise nupp
        learn_btn = ModernButton(button_frame, "📚 Õppimine", 
                                self.start_learning,
                                bg_color=COLORS['secondary'],
                                width=220, height=50)
        learn_btn.pack(pady=8)
        
        # Testi nupp
        test_btn = ModernButton(button_frame, "📝 Test", 
                               self.start_test,
                               bg_color=COLORS['primary'],
                               width=220, height=50)
        test_btn.pack(pady=8)
        
        # Tulemuste nupp
        results_btn = ModernButton(button_frame, "📊 Tulemused", 
                                  self.show_results,
                                  bg_color=COLORS['accent'],
                                  width=220, height=50)
        results_btn.pack(pady=8)
    
    def on_level_change(self, event=None):
        """Taseme muutmine."""
        try:
            self.current_level = int(self.level_var.get())
            self.level_label.config(text=f"Tase: {self.current_level}")
        except:
            pass
    
    def start_learning(self):
        """Alusta õppimisrežiimi."""
        self.clear_main_container()
        
        # Lae taseme sõnad
        level_data = self.sõnastik.get(str(self.current_level), {})
        self.current_words = []
        
        for category, words in level_data.items():
            for word in words:
                word_copy = word.copy()
                word_copy['_category'] = category
                self.current_words.append(word_copy)
        
        if not self.current_words:
            messagebox.showinfo("Tühi tase", "Sellel tasemel pole sõnu!")
            self.show_home_screen()
            return
        
        self.current_index = 0
        self.show_learning_card()
    
    def show_learning_card(self):
        """Näita õppimiskaarti."""
        self.clear_main_container()
        # Klaviatuuri otseteed: Enter/Right järgmisele, Left eelmisele
        self.root.bind('<Return>', lambda e: self.next_learning_word())
        self.root.bind('<Right>', lambda e: self.next_learning_word())
        self.root.bind('<Left>', lambda e: self.prev_learning_word())
        
        if self.current_index >= len(self.current_words):
            # Õppimine läbi
            self.show_learning_complete()
            return
        
        word = self.current_words[self.current_index]
        
        # Kaart
        card = tk.Frame(self.main_container, bg=COLORS['bg_card'], 
                   relief='solid', bd=1, highlightbackground=COLORS['border'],
                   highlightthickness=1)
        card.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Progressiriba
        progress = (self.current_index + 1) / len(self.current_words) * 100
        progress_frame = tk.Frame(card, bg=COLORS['bg_card'])
        progress_frame.pack(fill='x', padx=20, pady=12)

        tk.Label(progress_frame, 
            text=f"Sõna {self.current_index + 1} / {len(self.current_words)}",
            font=('Segoe UI', 11), bg=COLORS['bg_card'], 
            fg=COLORS['text_light']).pack(anchor='w')

        # Lühike progressiriba, mis skaleerub koos akna laiusega
        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', value=progress)
        progress_bar.pack(fill='x', pady=5)
        
        # Kategooria
        category = word.get('_category', '')
        tk.Label(card, text=f"📂 {category.upper()}", 
            font=('Segoe UI', 12), bg=COLORS['bg_card'],
            fg=COLORS['accent']).pack(pady=(6, 4))
        
        # Hispaania sõna (suur)
        spanish = word.get('sõna', '')
        tk.Label(card, text=spanish, font=('Segoe UI', 32, 'bold'),
            bg=COLORS['bg_card'], fg=COLORS['primary']).pack(pady=14)
        
        # Tõlge
        translation = word.get('tõlge', '')
        tk.Label(card, text="→", font=('Segoe UI', 22),
            bg=COLORS['bg_card'], fg=COLORS['text_light']).pack(pady=6)
        
        tk.Label(card, text=translation, font=('Segoe UI', 26, 'bold'),
            bg=COLORS['bg_card'], fg=COLORS['secondary']).pack(pady=8)
        
        # Navigeerimisnupud (kasutame ttk.Button'e, et need alati selgelt näha oleks)
        nav_frame = tk.Frame(card, bg=COLORS['bg_card'])
        nav_frame.pack(side='bottom', pady=18)

        if self.current_index > 0:
            prev_btn = ttk.Button(nav_frame, text="← Eelmine", command=self.prev_learning_word)
            prev_btn.pack(side='left', padx=10, ipadx=12, ipady=8)

        next_label = "Järgmine →" if self.current_index < len(self.current_words) - 1 else "Lõpeta ✓"
        next_btn = ttk.Button(nav_frame, text=next_label, command=self.next_learning_word)
        next_btn.pack(side='left', padx=10, ipadx=14, ipady=10)

        # Selge vihje klaviatuurile
        nav_hint = tk.Label(card, text="Enter või → järgmisele, ← eelmisele",
                    font=('Segoe UI', 10), bg=COLORS['bg_card'], fg=COLORS['text_light'])
        nav_hint.pack(pady=(6, 0))
        
        # Tagasi nupp (hoia nähtaval väiksemal ekraanil)
        back_btn = ttk.Button(card, text="🏠 Tagasi", command=self.show_home_screen)
        back_btn.pack(pady=(12, 10), ipadx=10, ipady=8)
    
    def prev_learning_word(self):
        """Eelmine sõna."""
        self.current_index = max(0, self.current_index - 1)
        self.show_learning_card()
    
    def next_learning_word(self):
        """Järgmine sõna."""
        self.current_index += 1
        self.show_learning_card()
    
    def show_learning_complete(self):
        """Õppimine lõpetatud."""
        self.clear_main_container()
        
        # Õnnitlemine
        card = tk.Frame(self.main_container, bg=COLORS['bg_card'])
        card.pack(pady=80, padx=100)
        
        tk.Label(card, text="🎉", font=('Segoe UI', 72),
                bg=COLORS['bg_card']).pack(pady=20)
        
        tk.Label(card, text="Õppimine läbitud!", 
                font=('Segoe UI', 28, 'bold'),
                bg=COLORS['bg_card'], fg=COLORS['success']).pack(pady=10)
        
        tk.Label(card, text=f"Õpisid {len(self.current_words)} sõna!",
                font=('Segoe UI', 16), bg=COLORS['bg_card'],
                fg=COLORS['text_light']).pack(pady=10)
        
        # Nupud
        btn_frame = tk.Frame(card, bg=COLORS['bg_card'])
        btn_frame.pack(pady=30)
        
        test_btn = ModernButton(btn_frame, "📝 Alusta testi", 
                       self.start_test,
                       bg_color=COLORS['primary'],
                       width=220, height=60)
        test_btn.pack(pady=10)
        
        home_btn = ModernButton(btn_frame, "🏠 Tagasi", 
                       self.show_home_screen,
                       bg_color=COLORS['text_light'],
                       width=220, height=60)
        home_btn.pack(pady=10)
    
    def start_test(self):
        """Alusta testi."""
        # Lae sõnad
        level_data = self.sõnastik.get(str(self.current_level), {})
        self.current_words = []
        
        for category, words in level_data.items():
            for word in words:
                self.current_words.append(word)
        
        if not self.current_words:
            messagebox.showinfo("Tühi tase", "Sellel tasemel pole sõnu!")
            self.show_home_screen()
            return
        
        # Sega sõnad
        random.shuffle(self.current_words)
        
        # Alusta esimese testiga (ESP→EST)
        self.test_mode = 'esp_est'
        self.current_index = 0
        self.test_score = 0
        self.test_total = len(self.current_words)
        self.test_errors = []
        
        self.show_test_question()
    
    def show_test_question(self):
        """Näita testi küsimust."""
        self.clear_main_container()
        
        # Kontrolli kas test on läbi
        if self.current_index >= len(self.current_words):
            if self.test_mode == 'esp_est':
                # Liigu teise testi juurde
                self.test_mode = 'est_esp'
                self.current_index = 0
                random.shuffle(self.current_words)
                self.show_test_transition()
                return
            else:
                # Mõlemad testid läbi
                self.show_test_results()
                return
        
        word = self.current_words[self.current_index]
        
        # Test kaart
        card = tk.Frame(self.main_container, bg=COLORS['bg_card'])
        card.pack(pady=50, padx=100, fill='both', expand=True)
        
        # Päis
        mode_text = "ESP → EST" if self.test_mode == 'esp_est' else "EST → ESP"
        tk.Label(card, text=f"📝 TEST: {mode_text}", 
                font=('Segoe UI', 16, 'bold'),
                bg=COLORS['bg_card'], fg=COLORS['accent']).pack(pady=20)
        
        # Progress
        progress_text = f"Küsimus {self.current_index + 1} / {self.test_total}"
        tk.Label(card, text=progress_text, font=('Segoe UI', 12),
                bg=COLORS['bg_card'], fg=COLORS['text_light']).pack()
        
        # Skoor
        score_text = f"Punktid: {self.test_score}"
        tk.Label(card, text=score_text, font=('Segoe UI', 14, 'bold'),
                bg=COLORS['bg_card'], fg=COLORS['primary']).pack(pady=10)
        
        # Küsimus
        if self.test_mode == 'esp_est':
            question = word.get('sõna', '')
            prompt = "Mis on selle sõna tõlge eesti keeles?"
        else:
            question = word.get('tõlge', '')
            prompt = "Kuidas on see hispaania keeles?"
        
        tk.Label(card, text=question, font=('Segoe UI', 32, 'bold'),
                bg=COLORS['bg_card'], fg=COLORS['primary']).pack(pady=30)
        
        tk.Label(card, text=prompt, font=('Segoe UI', 12),
                bg=COLORS['bg_card'], fg=COLORS['text_light']).pack()
        
        # Sisestusväli
        self.answer_var = tk.StringVar()
        entry_frame = tk.Frame(card, bg=COLORS['bg_card'])
        entry_frame.pack(pady=20)
        
        entry = tk.Entry(entry_frame, textvariable=self.answer_var,
                        font=('Segoe UI', 16), width=30, 
                        relief='solid', bd=2)
        entry.pack(pady=10)
        entry.focus()
        entry.bind('<Return>', lambda e: self.check_answer())
        
        # Esita nupp
        submit_btn = ModernButton(card, "✓ Kontrolli", self.check_answer,
                                 bg_color=COLORS['secondary'],
                                 width=180, height=50)
        submit_btn.pack(pady=20)
        
        # Tagasiside label (alguses tühi)
        self.feedback_label = tk.Label(card, text="", 
                                      font=('Segoe UI', 14, 'bold'),
                                      bg=COLORS['bg_card'])
        self.feedback_label.pack(pady=10)
    
    def check_answer(self):
        """Kontrolli vastust."""
        user_answer = self.answer_var.get().strip().lower()
        word = self.current_words[self.current_index]
        
        if self.test_mode == 'esp_est':
            correct = word.get('tõlge', '').lower()
            synonyms = [s.lower() for s in word.get('synonyms', [])]
        else:
            correct = word.get('sõna', '').lower()
            synonyms = []
        
        # Kontrolli vastust
        is_correct = user_answer == correct or user_answer in synonyms
        
        if is_correct:
            self.test_score += 1
            self.feedback_label.config(text="✓ Õige!", fg=COLORS['success'])
        else:
            self.test_errors.append(word)
            self.feedback_label.config(text=f"✗ Vale! Õige: {correct if self.test_mode == 'esp_est' else word.get('sõna')}", 
                                      fg=COLORS['danger'])
        
        # Järgmine küsimus pärast viivitust
        self.current_index += 1
        self.root.after(1500, self.show_test_question)
    
    def show_test_transition(self):
        """Näita üleminekut testide vahel."""
        self.clear_main_container()
        
        card = tk.Frame(self.main_container, bg=COLORS['bg_card'])
        card.pack(pady=100, padx=100)
        
        tk.Label(card, text="🔄", font=('Segoe UI', 64),
                bg=COLORS['bg_card']).pack(pady=20)
        
        tk.Label(card, text="Esimene test läbitud!", 
                font=('Segoe UI', 24, 'bold'),
                bg=COLORS['bg_card'], fg=COLORS['primary']).pack(pady=10)
        
        tk.Label(card, text=f"Sinu skoor: {self.test_score} / {self.test_total}",
                font=('Segoe UI', 18), bg=COLORS['bg_card'],
                fg=COLORS['text_dark']).pack(pady=10)
        
        tk.Label(card, text="Nüüd tõlgi eesti keelest hispaania keelde!",
                font=('Segoe UI', 14), bg=COLORS['bg_card'],
                fg=COLORS['text_light']).pack(pady=20)
        
        # Jätka automaatselt
        self.root.after(2500, self.show_test_question)
    
    def show_test_results(self):
        """Näita testi tulemusi."""
        self.clear_main_container()
        
        total_possible = self.test_total * 2  # Kaks testi
        percentage = (self.test_score / total_possible * 100) if total_possible > 0 else 0
        
        # Salvesta tulemus
        salvesta_tulemus(self.current_level, self.test_score, total_possible)
        
        # Tulemuste kaart
        card = tk.Frame(self.main_container, bg=COLORS['bg_card'])
        card.pack(pady=50, padx=100)
        
        # Emotikon tulemuse põhjal
        if percentage >= 90:
            emoji = "🏆"
            msg = "Suurepärane!"
            color = COLORS['success']
        elif percentage >= 70:
            emoji = "🎉"
            msg = "Väga hea!"
            color = COLORS['secondary']
        elif percentage >= 50:
            emoji = "👍"
            msg = "Hea töö!"
            color = COLORS['primary']
        else:
            emoji = "📚"
            msg = "Jätka harjutamist!"
            color = COLORS['warning']
        
        tk.Label(card, text=emoji, font=('Segoe UI', 80),
                bg=COLORS['bg_card']).pack(pady=20)
        
        tk.Label(card, text=msg, font=('Segoe UI', 28, 'bold'),
                bg=COLORS['bg_card'], fg=color).pack(pady=10)
        
        # Skoor
        tk.Label(card, text=f"{self.test_score} / {total_possible}",
                font=('Segoe UI', 36, 'bold'), bg=COLORS['bg_card'],
                fg=COLORS['primary']).pack(pady=20)
        
        tk.Label(card, text=f"{percentage:.1f}%",
                font=('Segoe UI', 24), bg=COLORS['bg_card'],
                fg=COLORS['text_light']).pack()
        
        # Vead
        if self.test_errors:
            tk.Label(card, text=f"Vale vastuseid: {len(self.test_errors)}",
                    font=('Segoe UI', 14), bg=COLORS['bg_card'],
                    fg=COLORS['danger']).pack(pady=10)
        
        # Nupud
        btn_frame = tk.Frame(card, bg=COLORS['bg_card'])
        btn_frame.pack(pady=30)
        
        if percentage == 100:
            tk.Label(card, text="✨ Täiuslik skoor! Liigume järgmisele tasemele!",
                    font=('Segoe UI', 12, 'bold'), bg=COLORS['bg_card'],
                    fg=COLORS['success']).pack(pady=10)
            
            if self.current_level < max(self.levels):
                next_btn = ModernButton(btn_frame, "➡ Järgmine tase", 
                                       self.go_next_level,
                                       bg_color=COLORS['success'],
                                       width=200, height=50)
                next_btn.pack(pady=10)
        
        retry_btn = ModernButton(btn_frame, "🔄 Proovi uuesti", 
                                self.start_test,
                                bg_color=COLORS['primary'],
                                width=200, height=50)
        retry_btn.pack(pady=10)
        
        home_btn = ModernButton(btn_frame, "🏠 Tagasi", 
                               self.show_home_screen,
                               bg_color=COLORS['text_light'],
                               width=200, height=50)
        home_btn.pack(pady=10)
    
    def go_next_level(self):
        """Liigu järgmisele tasemele."""
        if self.current_level < max(self.levels):
            self.current_level += 1
            self.level_var.set(str(self.current_level))
            self.level_label.config(text=f"Tase: {self.current_level}")
        self.show_home_screen()
    
    def show_results(self):
        """Näita tulemuste statistikat."""
        self.clear_main_container()
        
        # Lae tulemused
        try:
            with open('mängutulemused.json', 'r', encoding='utf-8') as f:
                results = json.load(f)
        except:
            results = []
        
        if not results:
            # Tulemused puuduvad
            card = tk.Frame(self.main_container, bg=COLORS['bg_card'])
            card.pack(pady=100, padx=100)
            
            tk.Label(card, text="📊", font=('Segoe UI', 64),
                    bg=COLORS['bg_card']).pack(pady=20)
            
            tk.Label(card, text="Tulemused puuduvad", 
                    font=('Segoe UI', 24, 'bold'),
                    bg=COLORS['bg_card'], fg=COLORS['text_dark']).pack(pady=10)
            
            tk.Label(card, text="Mängi mõni mäng tulemuste nägemiseks!",
                    font=('Segoe UI', 14), bg=COLORS['bg_card'],
                    fg=COLORS['text_light']).pack(pady=20)
            
            back_btn = ModernButton(card, "🏠 Tagasi", self.show_home_screen,
                                   bg_color=COLORS['primary'],
                                   width=180, height=50)
            back_btn.pack(pady=20)
            return
        
        # Tulemuste kaart
        card = tk.Frame(self.main_container, bg=COLORS['bg_card'])
        card.pack(pady=30, padx=50, fill='both', expand=True)
        
        tk.Label(card, text="📊 Sinu Tulemused", 
                font=('Segoe UI', 24, 'bold'),
                bg=COLORS['bg_card'], fg=COLORS['primary']).pack(pady=20)
        
        # Üldstatistika
        total_games = len(results)
        total_score = sum(r.get('punktid', 0) for r in results)
        total_max = sum(r.get('max_punktid', 0) for r in results)
        avg = (total_score / total_max * 100) if total_max > 0 else 0
        
        stats_frame = tk.Frame(card, bg=COLORS['bg_card'])
        stats_frame.pack(pady=20)
        
        # Statistika blokid
        self.create_stat_box(stats_frame, "🎮", "Mänge", str(total_games), 0, 0)
        self.create_stat_box(stats_frame, "⭐", "Punktid", f"{total_score}/{total_max}", 0, 1)
        self.create_stat_box(stats_frame, "📈", "Keskmine", f"{avg:.1f}%", 0, 2)
        
        # Viimased tulemused
        tk.Label(card, text="Viimased mängud:", 
                font=('Segoe UI', 16, 'bold'),
                bg=COLORS['bg_card'], fg=COLORS['text_dark']).pack(pady=(30, 10))
        
        # Tabel
        table_frame = tk.Frame(card, bg=COLORS['bg_card'])
        table_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Päis
        headers = ['Kuupäev', 'Tase', 'Tulemus', '%']
        for i, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=('Segoe UI', 11, 'bold'),
                    bg=COLORS['bg_card'], fg=COLORS['text_dark'],
                    width=15).grid(row=0, column=i, padx=5, pady=5)
        
        # Viimased 10 tulemust
        for i, result in enumerate(results[-10:][::-1]):
            tk.Label(table_frame, text=result.get('kuupäev', '')[:16],
                    font=('Segoe UI', 10), bg=COLORS['bg_card'],
                    fg=COLORS['text_light']).grid(row=i+1, column=0, padx=5, pady=3)
            
            tk.Label(table_frame, text=str(result.get('tase', '')),
                    font=('Segoe UI', 10), bg=COLORS['bg_card'],
                    fg=COLORS['text_light']).grid(row=i+1, column=1, padx=5, pady=3)
            
            score = f"{result.get('punktid', 0)}/{result.get('max_punktid', 0)}"
            tk.Label(table_frame, text=score, font=('Segoe UI', 10),
                    bg=COLORS['bg_card'], fg=COLORS['text_light']).grid(row=i+1, column=2, padx=5, pady=3)
            
            percent = result.get('protsent', 0)
            color = COLORS['success'] if percent >= 80 else COLORS['primary'] if percent >= 60 else COLORS['warning']
            tk.Label(table_frame, text=f"{percent:.1f}%",
                    font=('Segoe UI', 10, 'bold'), bg=COLORS['bg_card'],
                    fg=color).grid(row=i+1, column=3, padx=5, pady=3)
        
        # Tagasi nupp
        back_btn = ModernButton(card, "🏠 Tagasi", self.show_home_screen,
                               bg_color=COLORS['primary'],
                               width=180, height=50)
        back_btn.pack(pady=20)
    
    def create_stat_box(self, parent, icon, label, value, row, col):
        """Loo statistika kast."""
        box = tk.Frame(parent, bg='white', relief='solid', 
                      bd=1, highlightbackground=COLORS['border'],
                      highlightthickness=1, width=150, height=100)
        box.grid(row=row, column=col, padx=15, pady=10)
        box.grid_propagate(False)
        
        tk.Label(box, text=icon, font=('Segoe UI', 32),
                bg='white').pack(pady=(10, 0))
        tk.Label(box, text=value, font=('Segoe UI', 16, 'bold'),
                bg='white', fg=COLORS['primary']).pack()
        tk.Label(box, text=label, font=('Segoe UI', 10),
                bg='white', fg=COLORS['text_light']).pack()


def main():
    """Käivita GUI."""
    root = tk.Tk()
    app = SpanishLearningGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
