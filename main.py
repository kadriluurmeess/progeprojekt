"""
Progeprojekt - Hispaania keele õppemäng algajatele
Autorid: Kadri Luurmees, Oskar Martsoo
Allikad: 
Kirjeldus: Lihtne sõnavara õppimise mäng.
"""

import tkinter as tk
from gui import SõnaMängGUI

def main():
    """Käivita GUI"""
    root = tk.Tk()
    app = SõnaMängGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()