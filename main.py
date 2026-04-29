import tkinter as tk
from src.interface import JogoInterface
from src.controller import JogoController

def main():
    root = tk.Tk()
    root.title("Fighting Fantasy")
    root.geometry("950x750")
    
    # O controlador assume o comando a partir daqui
    app = JogoController(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()