import tkinter as tk
from PIL import Image, ImageTk
import os

class MenuPrincipal:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks # Funções que o Controller vai nos dar
        
        # Cores (Mantendo o padrão pergaminho que você gostou)
        self.cor_bege_claro = "#F4ECE1"
        self.cor_bege_escuro = "#D2B48C"
        self.cor_preto = "#1A1A1A"
        self.fonte_pixel = ("Courier New", 14, "bold")

        # Container Principal do Menu
        self.frame_menu = tk.Frame(root, bg=self.cor_bege_claro)
        self.frame_menu.pack(expand=True, fill="both")

        # Título / Logo
        self.lbl_titulo = tk.Label(
            self.frame_menu, text="A CIDADELA DO CAOS",
            font=("Courier New", 28, "bold"),
            bg=self.cor_bege_claro, fg=self.cor_preto,
            pady=50
        )
        self.lbl_titulo.pack()

        # Botões do Menu
        self.criar_botao("NOVO JOGO", self.callbacks['novo_jogo'])
        self.criar_botao("CONTINUAR", self.callbacks['continuar'])
        self.criar_botao("TUTORIAL", self.callbacks['tutorial'])
        self.criar_botao("CONFIGURAÇÕES", self.callbacks['config'])

        # Rodapé (Versão/Créditos)
        tk.Label(
            self.frame_menu, text="v1.0 - Baseado na obra de Steve Jackson",
            font=("Courier New", 8), bg=self.cor_bege_claro, fg="#888"
        ).pack(side="bottom", pady=10)

    def criar_botao(self, texto, comando):
        btn = tk.Button(
            self.frame_menu, text=texto, command=comando,
            font=self.fonte_pixel, bg=self.cor_preto, fg="white",
            activebackground=self.cor_bege_escuro,
            width=20, pady=10, relief="flat", cursor="hand2"
        )
        btn.pack(pady=10)

    def destruir(self):
        """Limpa o menu da tela para dar lugar ao jogo"""
        self.frame_menu.destroy()