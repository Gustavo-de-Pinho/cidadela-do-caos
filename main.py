import tkinter as tk
from src.interface import JogoInterface
from src.controller import JogoController

def main():
    root = tk.Tk()
    
    # Inicia a Visão (View)
    # Passamos apenas o root; o Controller cuidará do resto
    ui = JogoInterface(root)
    
    # Inicia o Controlador (Controller) e entrega a UI para ele
    app = JogoController(ui)
    
    root.mainloop()

if __name__ == "__main__":
    main()