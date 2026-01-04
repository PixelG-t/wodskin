# download the whole file and run this and it will work 
# main.py - WOD Skin Maker Entry Point



import tkinter as tk
from app import WODSkinMaker

if __name__ == "__main__":
    root = tk.Tk()
    app = WODSkinMaker(root)
    root.mainloop()
