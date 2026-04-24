import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk # Necessário para as imagens
import os

class JogoInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("A Cidadela do Caos")
        
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
        self.carregar_icones()

        # --- 1. CABEÇALHO (JUSTIFICADO COM O TEXTO) ---
        # Usamos o mesmo padx=40 do frame de texto para alinhar
        self.header = tk.Frame(root, bg=self.cor_bege_escuro, pady=10)
        self.header.pack(side="top", fill="x")

        # Este container interno garante o alinhamento "justificado"
        self.status_container = tk.Frame(self.header, bg=self.cor_bege_escuro)
        self.status_container.pack(fill="x", padx=40) # Alinhado com a janela de texto

        # Configura as 4 colunas para terem o mesmo peso (distribuição igual)
        for i in range(4):
            self.status_container.columnconfigure(i, weight=1)

        self.stats = {}
        self.criar_slot_status("Habilidade", "hab.png", 0)
        self.criar_slot_status("Energia", "ene.png", 1)
        self.criar_slot_status("Sorte", "sor.png", 2)
        self.criar_slot_status("Magia", "mag.png", 3)

        # --- 2. RODAPÉ DE BOTÕES ---
        self.frame_botoes = tk.Frame(root, bg=self.cor_bege_claro, pady=15)
        self.frame_botoes.pack(side="bottom", fill="x")

        self.btn_iniciar = tk.Button(
            self.frame_botoes, text="[ INICIAR AVENTURA ]", 
            command=self.exibir_introducao,
            font=("Courier New", 12, "bold"), 
            bg=self.cor_preto, fg=self.cor_branco,
            padx=25, pady=12, relief="flat", cursor="hand2"
        )
        self.btn_iniciar.pack()

        # --- 3. JANELA DE TEXTO ---
        self.frame_texto = tk.Frame(root, bg=self.cor_bege_escuro, padx=40, pady=10)
        self.frame_texto.pack(side="top", expand=True, fill="both")

        self.texto_principal = scrolledtext.ScrolledText(
            self.frame_texto, wrap=tk.WORD, 
            font=("Courier New", 14, "bold"),
            bg=self.cor_branco, fg=self.cor_preto, 
            padx=30, pady=30, 
            borderwidth=2, relief="solid"
        )
        self.texto_principal.pack(expand=True, fill="both")
        self.texto_principal.configure(state="disabled")

    def carregar_icones(self):
        """Carrega e redimensiona as imagens da pasta assets"""
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
                # Redimensiona para um tamanho que caiba bem (ex: 70x70 pixels)
                img = img.resize((75, 75), Image.Resampling.LANCZOS)
                self.icones[nome] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Erro ao carregar {arq}: {e}")
                # Cria um placeholder caso a imagem não exista
                self.icones[nome] = None

    def criar_slot_status(self, nome, img_nome, coluna):
        var = tk.StringVar(value="0")
        self.stats[nome] = var

        # Frame para cada slot (Habilidade, Energia, etc)
        slot = tk.Frame(self.status_container, bg=self.cor_bege_escuro)
        slot.grid(row=0, column=coluna, sticky="nsew")

        # Label da Imagem com o texto em cima
        # compound="center" coloca o texto no meio da imagem
        lbl_img = tk.Label(
            slot, 
            image=self.icones[nome], 
            textvariable=var,
            font=("Courier New", 22, "bold"),
            fg=self.cor_preto, # Cor do número
            bg=self.cor_bege_escuro,
            compound="center"
        )
        lbl_img.pack()

        # Texto pequeno embaixo para identificar o que é
        tk.Label(
            slot, text=nome.upper(), 
            bg=self.cor_bege_escuro, 
            fg=self.cor_preto, 
            font=("Courier New", 8, "bold")
        ).pack()

    def exibir_texto(self, texto):
        self.texto_principal.configure(state="normal")
        self.texto_principal.delete(1.0, tk.END)
        self.texto_principal.insert(tk.END, texto)
        self.texto_principal.configure(state="disabled")

    def atualizar_stats(self, hab, ene, sor, mag):
        self.stats["Habilidade"].set(str(hab))
        self.stats["Energia"].set(str(ene))
        self.stats["Sorte"].set(str(sor))
        self.stats["Magia"].set(str(mag))

    def exibir_introducao(self):
        self.atualizar_stats(10, 22, 11, 7)
        msg = "A CIDADELA DO CAOS\n\nSua missão começa aqui..."
        self.exibir_texto(msg)