import tkinter as tk
from PIL import Image, ImageTk
import os

class GerenciadorCards:
    def __init__(self, container_pai, frame_rodape, limite, finalizar_callback):
        self.pai = container_pai
        self.rodape = frame_rodape
        self.limite = limite
        self.finalizar_callback = finalizar_callback
        
        self.vars = {}
        self.card_widgets = [] 
        # Aumentamos a largura base do card para acomodar imagens maiores
        self.largura_card = 250 
        self.cor_fundo_geral = "#F4ECE1"

    def exibir(self, titulo, dados_cards, subpasta):
        self.frame_main = tk.Frame(self.pai, bg=self.cor_fundo_geral)
        self.frame_main.pack(expand=True, fill="both")

        self.lbl_titulo = tk.Label(
            self.frame_main, text=f"{titulo}\nPontos Disponíveis: {self.limite}",
            font=("Courier New", 18, "bold"), bg=self.cor_fundo_geral, pady=15
        )
        self.lbl_titulo.pack(fill="x")

        self.canvas = tk.Canvas(self.frame_main, bg=self.cor_fundo_geral, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_main, orient="vertical", command=self.canvas.yview)
        
        self.container_cards = tk.Frame(self.canvas, bg=self.cor_fundo_geral)
        self.window_id = self.canvas.create_window((0, 0), window=self.container_cards, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", expand=True, fill="both")
        self.scrollbar.pack(side="right", fill="y")

        self.card_widgets = []
        for item in dados_cards:
            self.criar_card_widget(item, subpasta)

        # Configuração do Botão no Rodapé
        for widget in self.rodape.winfo_children():
            widget.destroy()

        self.btn_confirmar = tk.Button(
            self.rodape, text="[ CONFIRMAR ESCOLHAS ]", 
            command=self.confirmar, font=("Courier New", 12, "bold"),
            bg="#1A1A1A", fg="white", padx=40, pady=12,
            cursor="hand2", relief="flat"
        )
        self.btn_confirmar.pack(expand=True)

        self.pai.update_idletasks()
        self.canvas.bind("<Configure>", self.ao_redimensionar_canvas)
        self.container_cards.bind("<Configure>", self.ajustar_scroll)
        self.reordenar_grid()

    def criar_card_widget(self, item, subpasta):
        # Card "Invisível": bg igual ao fundo, bd=0 e relief flat
        card = tk.Frame(self.container_cards, bg=self.cor_fundo_geral, bd=0, relief="flat", padx=10, pady=10)
        
        # Imagem maior: 160x160
        try:
            caminho = os.path.join(os.path.dirname(__file__), '..', 'assets', subpasta, item['imagem'])
            img = Image.open(caminho).resize((160, 160), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(card, image=foto, bg=self.cor_fundo_geral)
            lbl_img.image = foto
            lbl_img.pack()
        except:
            # Caso a imagem não carregue, um placeholder invisível também
            tk.Label(card, text=f"[{item['nome']}]", bg=self.cor_fundo_geral, font=("Courier New", 10)).pack()

        # Nome da magia
        tk.Label(card, text=item['nome'].upper(), bg=self.cor_fundo_geral, 
                 font=("Courier New", 11, "bold"), fg="#333").pack(pady=(5, 0))

        # Controles (+ / -)
        frame_ctrl = tk.Frame(card, bg=self.cor_fundo_geral)
        frame_ctrl.pack(pady=5)

        var_qtd = tk.IntVar(value=0)
        self.vars[item['id']] = var_qtd

        # Estilização minimalista para os botões de controle
        btn_estilo = {"bg": "#1A1A1A", "fg": "white", "relief": "flat", "width": 2, "cursor": "hand2"}
        
        tk.Button(frame_ctrl, text="-", command=lambda v=var_qtd: self.alterar_qtd(v, -1), **btn_estilo).pack(side="left")
        tk.Label(frame_ctrl, textvariable=var_qtd, width=4, font=("Arial", 14, "bold"), 
                 bg=self.cor_fundo_geral, fg="#1A1A1A").pack(side="left", padx=10)
        tk.Button(frame_ctrl, text="+", command=lambda v=var_qtd: self.alterar_qtd(v, 1), **btn_estilo).pack(side="left")

        self.card_widgets.append(card)

    def ao_redimensionar_canvas(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)
        self.reordenar_grid()

    def ajustar_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def reordenar_grid(self):
        largura_atual = self.canvas.winfo_width()
        if largura_atual <= 1:
            num_colunas = 3
        else:
            num_colunas = max(1, largura_atual // self.largura_card)

        for i, card in enumerate(self.card_widgets):
            linha = i // num_colunas
            coluna = i % num_colunas
            card.grid(row=linha, column=coluna, padx=10, pady=20)

    def alterar_qtd(self, var_alvo, delta):
        total_atual = sum(v.get() for v in self.vars.values())
        if delta > 0 and total_atual < self.limite:
            var_alvo.set(var_alvo.get() + 1)
        elif delta < 0 and var_alvo.get() > 0:
            var_alvo.set(var_alvo.get() - 1)
        
        total = sum(v.get() for v in self.vars.values())
        self.lbl_titulo.config(text=f"ESCOLHA SEUS ENCANTOS\nRestante: {self.limite - total}")

    def confirmar(self):
        escolhas = []
        for id_mag, var in self.vars.items():
            for _ in range(var.get()):
                escolhas.append(id_mag)
        self.finalizar_callback(escolhas)