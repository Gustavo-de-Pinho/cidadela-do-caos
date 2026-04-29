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
        self.largura_card = 200 # Aumentei um pouco para dar mais respiro

    def exibir(self, titulo, dados_cards, subpasta):
        # 1. Limpeza e Setup Inicial
        self.frame_main = tk.Frame(self.pai, bg="#F4ECE1")
        self.frame_main.pack(expand=True, fill="both")

        self.lbl_titulo = tk.Label(
            self.frame_main, text=f"{titulo}\nPontos Disponíveis: {self.limite}",
            font=("Courier New", 16, "bold"), bg="#F4ECE1", pady=15
        )
        self.lbl_titulo.pack(fill="x")

        # 2. Área de Scroll
        self.canvas = tk.Canvas(self.frame_main, bg="#F4ECE1", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_main, orient="vertical", command=self.canvas.yview)
        
        self.container_cards = tk.Frame(self.canvas, bg="#F4ECE1")
        
        # Este ID é importante para redimensionar o frame interno depois
        self.window_id = self.canvas.create_window((0, 0), window=self.container_cards, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", expand=True, fill="both")
        self.scrollbar.pack(side="right", fill="y")

        # 3. Criar os Widgets dos Cards
        self.card_widgets = [] # Limpa lista anterior
        for item in dados_cards:
            self.criar_card_widget(item, subpasta)

        # 4. Botão de Confirmar no Rodapé
        for widget in self.rodape.winfo_children():
            widget.destroy()

        self.btn_confirmar = tk.Button(
            self.rodape, text="[ CONFIRMAR ESCOLHAS ]", 
            command=self.confirmar, font=("Courier New", 12, "bold"),
            bg="#1A1A1A", fg="white", padx=40, pady=12,
            cursor="hand2", relief="flat"
        )
        self.btn_confirmar.pack(expand=True)

        # 5. LÓGICA DE EXIBIÇÃO CORRIGIDA
        # Força o Tkinter a calcular os tamanhos agora
        self.pai.update_idletasks()
        
        # Monitora redimensionamento da janela
        self.canvas.bind("<Configure>", self.ao_redimensionar_canvas)
        # Monitora tamanho do conteúdo para o scroll
        self.container_cards.bind("<Configure>", self.ajustar_scroll)

        # Chama o grid pela primeira vez manualmente
        self.reordenar_grid()

    def criar_card_widget(self, item, subpasta):
        card = tk.Frame(self.container_cards, bg="white", bd=2, relief="solid", padx=10, pady=10)
        
        try:
            caminho = os.path.join(os.path.dirname(__file__), '..', 'assets', subpasta, item['imagem'])
            img = Image.open(caminho).resize((90, 90), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(card, image=foto, bg="white")
            lbl_img.image = foto
            lbl_img.pack()
        except:
            tk.Label(card, text="[IMG]", bg="white").pack()

        tk.Label(card, text=item['nome'], bg="white", font=("Courier New", 10, "bold")).pack()

        frame_ctrl = tk.Frame(card, bg="white")
        frame_ctrl.pack(pady=5)

        var_qtd = tk.IntVar(value=0)
        self.vars[item['id']] = var_qtd

        tk.Button(frame_ctrl, text="-", width=2, command=lambda v=var_qtd: self.alterar_qtd(v, -1)).pack(side="left")
        tk.Label(frame_ctrl, textvariable=var_qtd, width=3, font=("Arial", 11, "bold"), bg="white").pack(side="left")
        tk.Button(frame_ctrl, text="+", width=2, command=lambda v=var_qtd: self.alterar_qtd(v, 1)).pack(side="left")

        self.card_widgets.append(card)

    def ao_redimensionar_canvas(self, event):
        """Ajusta a largura do frame interno e reposiciona os cards"""
        # Garante que o frame de cards tenha pelo menos a largura do canvas
        self.canvas.itemconfig(self.window_id, width=event.width)
        self.reordenar_grid()

    def ajustar_scroll(self, event):
        """Atualiza a área de rolagem quando cards são adicionados/movidos"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def reordenar_grid(self):
        """Calcula colunas baseado na largura real disponível"""
        largura_atual = self.canvas.winfo_width()
        # Se o Tkinter ainda não calculou (largura=1), usa um padrão de 3 colunas
        if largura_atual <= 1:
            num_colunas = 3
        else:
            num_colunas = max(1, largura_atual // self.largura_card)

        for i, card in enumerate(self.card_widgets):
            linha = i // num_colunas
            coluna = i % num_colunas
            card.grid(row=linha, column=coluna, padx=15, pady=15)

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