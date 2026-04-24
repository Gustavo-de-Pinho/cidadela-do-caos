import tkinter as tk
from src.interface import JogoInterface

def main():
    # Inicializa o motor gráfico (Tkinter)
    root = tk.Tk()
    
    # Cria a nossa interface
    app = JogoInterface(root)
    
    # Mantém a janela aberta
    root.mainloop()

if __name__ == "__main__":
    main()