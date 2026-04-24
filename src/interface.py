import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageSequence
import os

class JogoInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Fighting Fantasy - A Cidadela do Caos [Beta]")

        # --- CONFIGURAÇÃO DE TELA ---
        self.root.geometry("950x750")
        self.root.minsize(850, 650)
        
        # Paleta de Cores
        self.cor_bege_claro = "#F4ECE1"
        self.cor_bege_escuro = "#D2B48C"
        self.cor_branco = "#FFFFFF"
        self.cor_preto = "#1A1A1A"
        
        self.root.configure(bg=self.cor_bege_claro)

        # --- CARREGAMENTO DE ASSETS ---
        self.icones = {}
        self.carregar_icones() # Agora a função está logo ali embaixo!

        # --- 1. CABEÇALHO (JUSTIFICADO) ---
        self.header = tk.Frame(root, bg=self.cor_bege_escuro, pady=10)
        self.header.pack(side="top", fill="x")

        self.status_container = tk.Frame(self.header, bg=self.cor_bege_escuro)
        self.status_container.pack(fill="x", padx=40)

        for i in range(4):
            self.status_container.columnconfigure(i, weight=1)

        self.stats_vars = {}
        self.criar_slot_status("Habilidade", 0)
        self.criar_slot_status("Energia", 1)
        self.criar_slot_status("Sorte", 2)
        self.criar_slot_status("Magia", 3)

        # --- 2. RODAPÉ DE BOTÕES ---
        self.frame_botoes = tk.Frame(root, bg=self.cor_bege_claro, pady=15)
        self.frame_botoes.pack(side="bottom", fill="x")

        self.btn_iniciar = tk.Button(
            self.frame_botoes, text="[ INICIAR AVENTURA ]", 
            font=("Courier New", 12, "bold"), 
            bg=self.cor_preto, fg=self.cor_branco,
            padx=25, pady=12, relief="flat", cursor="hand2"
        )
        self.btn_iniciar.pack()

        # --- 3. JANELA DE TEXTO ---
        self.frame_central = tk.Frame(root, bg=self.cor_bege_escuro, padx=40, pady=10)
        self.frame_central.pack(side="top", expand=True, fill="both")

        self.container_texto = tk.Frame(self.frame_central, bg=self.cor_branco, bd=2, relief="solid")
        self.container_texto.pack(expand=True, fill="both")

        self.texto_principal = scrolledtext.ScrolledText(
            self.container_texto, wrap=tk.WORD, 
            font=("Courier New", 14, "bold"),
            bg=self.cor_branco, fg=self.cor_preto, 
            padx=30, pady=30, borderwidth=0
        )
        self.texto_principal.pack(expand=True, fill="both")
        self.texto_principal.configure(state="disabled")

        # LABEL DO DADO (Invisível até ser animado)
        self.lbl_dado = tk.Label(self.container_texto, bg=self.cor_branco)
        self.lbl_dado.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-30)

    # --- MÉTODOS DE SUPORTE ---

    def carregar_icones(self):
        caminho_assets = os.path.join(os.path.dirname(__file__), '..', 'assets')
        arquivos = {
            "Habilidade": "hab.png",
            "Energia": "ene.png",
            "Sorte": "sor.png",
            "Magia": "mag.png"
        }
        
        for nome, arq in arquivos.items():
            caminho = os.path.join(caminho_assets, arq)
            try:
                img = Image.open(caminho).convert("RGBA")
                img = img.resize((75, 75), Image.Resampling.LANCZOS)
                self.icones[nome] = ImageTk.PhotoImage(img)
            except:
                self.icones[nome] = None

    def criar_slot_status(self, nome, coluna):
        var = tk.StringVar(value="0")
        self.stats_vars[nome] = var

        slot = tk.Frame(self.status_container, bg=self.cor_bege_escuro)
        slot.grid(row=0, column=coluna, sticky="nsew")

        lbl_img = tk.Label(
            slot, image=self.icones.get(nome), textvariable=var,
            font=("Courier New", 22, "bold"), fg=self.cor_preto,
            bg=self.cor_bege_escuro, compound="center"
        )
        lbl_img.pack()

        tk.Label(slot, text=nome.upper(), bg=self.cor_bege_escuro, 
                 fg=self.cor_preto, font=("Courier New", 8, "bold")).pack()

    def animar_dado(self, duracao_ms=1500):
        caminho_gif = os.path.join(os.path.dirname(__file__), '..', 'assets', 'dados.gif')
        if not os.path.exists(caminho_gif):
            print("Aviso: assets/dados.gif não encontrado.")
            return

        try:
            img_gif = Image.open(caminho_gif)
            
            # Redimensionando para 60x60 (um tamanho bom para o canto)
            tamanho_pixel = (60, 60)
            self.frames = []
            
            for frame in ImageSequence.Iterator(img_gif):
                # Importante: converter para RGBA para manter transparência se houver
                frame_redimensionado = frame.copy().convert("RGBA").resize(tamanho_pixel, Image.Resampling.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame_redimensionado))
            
            def atualizar(ind):
                if hasattr(self, 'frames') and self.frames:
                    frame = self.frames[ind]
                    self.lbl_dado.configure(image=frame)
                    # Velocidade da animação (80ms entre frames)
                    self.proximo_frame = self.root.after(80, atualizar, (ind + 1) % len(self.frames))

            atualizar(0)
            # Agenda o sumiço do dado após a duração total
            self.root.after(duracao_ms, self.parar_animacao_dado)
            
        except Exception as e:
            print(f"Erro ao animar dado: {e}")

    def parar_animacao_dado(self):
        if hasattr(self, 'proximo_frame'):
            self.root.after_cancel(self.proximo_frame)
        self.lbl_dado.configure(image="")

    def atualizar_stats(self, hab, ene, sor, mag):
        self.stats_vars["Habilidade"].set(str(hab))
        self.stats_vars["Energia"].set(str(ene))
        self.stats_vars["Sorte"].set(str(sor))
        self.stats_vars["Magia"].set(str(mag))

    def exibir_texto(self, texto):
        self.texto_principal.configure(state="normal")
        self.texto_principal.delete(1.0, tk.END)
        self.texto_principal.insert(tk.END, texto)
        self.texto_principal.configure(state="disabled")