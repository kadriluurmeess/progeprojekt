"""
Progeprojekt - Hispaania keele õppemäng algajatele
Autorid: Kadri Luurmees, Oskar Martsoo
Allikad: 
Kirjeldus: Lihtne sõnavara õppimise mäng.
"""

import tkinter as tk
from gui import SonaMangGUI

def main():
    """Käivita graafiline kasutajaliides."""
    root = tk.Tk()
    app = SonaMangGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()