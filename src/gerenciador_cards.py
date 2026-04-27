import tkinter as tk
from PIL import Image, ImageTk
import os

class GerenciadorCards:
    def __init__(self, container_pai, limite, finalizar_callback):
        self.pai = container_pai
        self.limite = limite # No caso de magias, será o valor sorteado
        self.finalizar_callback = finalizar_callback
        self.vars = {}
        self.selecionados_count = 0

    def exibir(self, titulo, dados_cards, subpasta):
        self.frame_cards = tk.Frame(self.pai, bg="#F4ECE1")
        self.frame_cards.pack(expand=True, fill="both")

        # Título e Contador de Pontos
        self.lbl_titulo = tk.Label(self.frame_cards, 
                                   text=f"{titulo}\nRestante: {self.limite}", 
                                   font=("Courier New", 16, "bold"), bg="#F4ECE1")
        self.lbl_titulo.pack(pady=10)

        # Grade com Scroll
        canvas = tk.Canvas(self.frame_cards, bg="#F4ECE1", highlightthickness=0)
        scroll_y = tk.Scrollbar(self.frame_cards, orient="vertical", command=canvas.yview)
        self.grade = tk.Frame(canvas, bg="#F4ECE1")

        self.grade.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.grade, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", expand=True, fill="both", padx=20)
        scroll_y.pack(side="right", fill="y")

        for i, item in enumerate(dados_cards):
            self.criar_card(item, i // 3, i % 3, subpasta)

        self.btn_confirmar = tk.Button(self.frame_cards, text="[ CONFIRMAR SELEÇÃO ]", 
                                       command=self.confirmar, font=("Courier New", 12, "bold"),
                                       bg="#1A1A1A", fg="white", padx=20, pady=10)
        self.btn_confirmar.pack(pady=20)

    def criar_card(self, item, lin, col, subpasta):
        card = tk.Frame(self.grade, bg="white", bd=2, relief="solid", padx=5, pady=5)
        card.grid(row=lin, column=col, padx=10, pady=10)

        # Imagem
        try:
            caminho = os.path.join(os.path.dirname(__file__), '..', 'assets', subpasta, item['imagem'])
            img = Image.open(caminho).resize((70, 70), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(img)
            lbl = tk.Label(card, image=foto, bg="white")
            lbl.image = foto
            lbl.pack()
        except:
            tk.Label(card, text="[IMG]", bg="white").pack()

        var = tk.BooleanVar()
        self.vars[item['id']] = var
        
        # Checkbox com lógica de limite
        cb = tk.Checkbutton(card, text=item['nome'], variable=var, bg="white", 
                            font=("Courier New", 9, "bold"),
                            command=self.atualizar_contador)
        cb.pack()

    def atualizar_contador(self):
        escolhidos = sum(1 for v in self.vars.values() if v.get())
        restante = self.limite - escolhidos
        
        if restante < 0:
            # Se estourar o limite, desmarcar o último (opcional) ou apenas avisar
            self.lbl_titulo.config(text=f"LIMITE EXCEDIDO!\nRestante: 0", fg="red")
            self.btn_confirmar.config(state="disabled")
        else:
            self.lbl_titulo.config(text=f"ESCOLHA SEUS ENCANTOS\nRestante: {restante}", fg="black")
            self.btn_confirmar.config(state="normal")

    def confirmar(self):
        selecionados = [id_it for id_it, v in self.vars.items() if v.get()]
        self.finalizar_callback(selecionados)