import tkinter as tk
from tkinter import ttk, messagebox
import random, unicodedata, re

# Reuse saver and loader from your logic module
from mänguloogika import lae_sõnad, salvesta_tulemus


def normalize(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.lower().strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def is_correct(user: str, expected: str, synonyms=None) -> bool:
    if synonyms is None:
        synonyms = []
    user_n = normalize(user)
    if not user_n:
        return False
    candidates = [normalize(expected)] + [normalize(x) for x in synonyms]
    if user_n in candidates:
        return True
    # simple fuzzy fallback: check partial token overlap
    exp_tokens = set(normalize(expected).split())
    user_tokens = set(user_n.split())
    if exp_tokens and (len(exp_tokens & user_tokens) / max(1, len(exp_tokens)) >= 0.6):
        return True
    return False


class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Hispaania õpimäng (GUI)')
        self.sõnastik = {}
        try:
            self.sõnastik = lae_sõnad()
        except Exception as e:
            messagebox.showerror('Viga', f'Ei saa laadida sõnastikku: {e}')
            root.destroy()
            return

        self.levels = sorted([k for k in self.sõnastik.keys()], key=lambda x: int(x))

        top = ttk.Frame(root, padding=12)
        top.grid(sticky='nsew')

        ttk.Label(top, text='Vali tase:').grid(row=0, column=0, sticky='w')
        self.level_var = tk.StringVar(value=self.levels[0] if self.levels else '1')
        self.level_cb = ttk.Combobox(top, values=self.levels, textvariable=self.level_var, state='readonly')
        self.level_cb.grid(row=0, column=1, sticky='w')

        self.learn_btn = ttk.Button(top, text='Õppimine (Learn)', command=self.start_learning)
        self.learn_btn.grid(row=0, column=2, padx=6)

        self.test_btn = ttk.Button(top, text='Test', command=self.start_test)
        self.test_btn.grid(row=0, column=3, padx=6)

        ttk.Separator(top, orient='horizontal').grid(row=1, column=0, columnspan=4, sticky='ew', pady=8)

        # Main card area
        self.card = ttk.Frame(root, padding=12)
        self.card.grid(sticky='nsew')

        self.title_lbl = ttk.Label(self.card, text='', font=('Helvetica', 16, 'bold'))
        self.title_lbl.grid(row=0, column=0, columnspan=3)

        self.word_lbl = ttk.Label(self.card, text='', font=('Helvetica', 24))
        self.word_lbl.grid(row=1, column=0, columnspan=3, pady=(8,2))

        self.pron_lbl = ttk.Label(self.card, text='', font=('Helvetica', 12, 'italic'))
        self.pron_lbl.grid(row=2, column=0, columnspan=3)

        self.trans_lbl = ttk.Label(self.card, text='', font=('Helvetica', 12))
        self.trans_lbl.grid(row=3, column=0, columnspan=3, pady=(6,6))

        # For test mode
        ttk.Label(self.card, text='Sinu vastus:').grid(row=4, column=0, sticky='w')
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(self.card, textvariable=self.answer_var, width=40)
        self.answer_entry.grid(row=4, column=1, sticky='w')
        self.submit_btn = ttk.Button(self.card, text='Esita', command=self.submit_answer)
        self.submit_btn.grid(row=4, column=2, padx=6)

        self.feedback_lbl = ttk.Label(self.card, text='', font=('Helvetica', 11))
        self.feedback_lbl.grid(row=5, column=0, columnspan=3, pady=(6,0))

        nav = ttk.Frame(self.card)
        nav.grid(row=6, column=0, columnspan=3, pady=(10,0))
        self.prev_btn = ttk.Button(nav, text='Eelmine', command=self.prev_word)
        self.prev_btn.grid(row=0, column=0, padx=6)
        self.next_btn = ttk.Button(nav, text='Järgmine', command=self.next_word)
        self.next_btn.grid(row=0, column=1, padx=6)

        # State
        self.mode = None  # 'learn' or 'test'
        self.words = []
        self.index = 0
        self.test_order = []
        self.test_score = 0
        self.test_total = 0

        # initial empty
        self.show_empty()

    def flatten_level(self, level_str):
        level = self.sõnastik.get(level_str, {})
        out = []
        for kateg, nimekiri in level.items():
            for elem in nimekiri:
                e = dict(elem)  # copy
                e['_kateg'] = kateg
                out.append(e)
        return out

    def show_empty(self):
        self.title_lbl.config(text='Vali tase ja režiim')
        self.word_lbl.config(text='')
        self.pron_lbl.config(text='')
        self.trans_lbl.config(text='')
        self.answer_var.set('')
        self.feedback_lbl.config(text='')

    # Learning mode
    def start_learning(self):
        self.mode = 'learn'
        level = self.level_var.get()
        self.words = self.flatten_level(level)
        self.index = 0
        if not self.words:
            messagebox.showinfo('Tühi tase', 'Valitud tasemel ei ole sõnu.')
            return
        self.title_lbl.config(text=f'Õppimine – tase {level}')
        self.show_current()

    def show_current(self):
        if not self.words:
            self.show_empty(); return
        elem = self.words[self.index]
        sõna = elem.get('sõna', '')
        tõlge = elem.get('tõlge', '')
        hääldus = elem.get('hääldus', '')
        kateg = elem.get('_kateg', '')
        self.word_lbl.config(text=sõna)
        self.pron_lbl.config(text=f'[{hääldus}]' if hääldus else '')
        self.trans_lbl.config(text=f'{tõlge}  ({kateg})')
        self.feedback_lbl.config(text=f'{self.index+1}/{len(self.words)}')
        self.answer_var.set('')

    def prev_word(self):
        if not self.words: return
        self.index = max(0, self.index-1)
        self.show_current()

    def next_word(self):
        if not self.words: return
        self.index = min(len(self.words)-1, self.index+1)
        self.show_current()

    # Test mode
    def start_test(self):
        self.mode = 'test'
        level = self.level_var.get()
        self.words = self.flatten_level(level)
        if not self.words:
            messagebox.showinfo('Tühi tase', 'Valitud tasemel ei ole sõnu.')
            return
        self.test_order = list(range(len(self.words)))
        random.shuffle(self.test_order)
        self.test_total = len(self.test_order)
        self.test_score = 0
        self.index = 0
        self.title_lbl.config(text=f'Test – tase {level} ({self.test_score}/{self.test_total})')
        self.show_test_item()

    def show_test_item(self):
        if self.index >= self.test_total:
            self.finish_test()
            return
        elem = self.words[self.test_order[self.index]]
        self.current_elem = elem
        self.word_lbl.config(text=elem.get('sõna', ''))
        h = elem.get('hääldus', '')
        self.pron_lbl.config(text=f'[{h}]' if h else '')
        self.trans_lbl.config(text='')
        self.answer_var.set('')
        self.feedback_lbl.config(text=f'{self.index+1}/{self.test_total} — punktid: {self.test_score}')
        self.answer_entry.focus()

    def submit_answer(self):
        if self.mode != 'test' or not hasattr(self, 'current_elem'):
            return
        user = self.answer_var.get()
        expected = self.current_elem.get('tõlge', '')
        synonyms = self.current_elem.get('synonyms', [])
        if is_correct(user, expected, synonyms):
            self.test_score += 1
            self.feedback_lbl.config(text='✅ Õige!')
        else:
            self.feedback_lbl.config(text=f'❌ Vale. Õige: {expected}')
        self.index += 1
        # small delay then show next
        self.root.after(700, self.show_test_item)

    def finish_test(self):
        level_str = self.level_var.get()
        try:
            tase_int = int(level_str)
        except Exception:
            tase_int = 0
        message = f'Skoor: {self.test_score}/{self.test_total}'
        self.title_lbl.config(text=f'Test lõpetatud – {message}')
        salvesta_tulemus(tase_int, self.test_score, self.test_total)
        if self.test_score == self.test_total:
            messagebox.showinfo('Tase läbitud', 'Tubli! Sa sooritasid taseme 100% — liigud järgmisele tasemele.')
            # try to advance combobox selection if possible
            try:
                idx = self.levels.index(level_str)
                if idx+1 < len(self.levels):
                    self.level_var.set(self.levels[idx+1])
            except Exception:
                pass
        else:
            messagebox.showinfo('Test lõpetatud', f'{message}\nÕpid nüüd uuesti valesid sõnu (prototüüp).')
            # Optionally, filter words to only wrong ones — left as enhancement


if __name__ == '__main__':
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
