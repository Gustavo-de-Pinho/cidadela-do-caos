import json
import os
import tkinter as tk
from src.menu import MenuPrincipal
from src.interface import JogoInterface
from src.personagem import Personagem
from src.engine import Engine
from src.gerenciador_cards import GerenciadorCards

class JogoController:
    def __init__(self, root):
        self.root = root
        self.personagem = None
        self.biblioteca_historia = self.carregar_json_historia()
        self.exibir_menu_inicial()

    # --- 1. CARREGAMENTO DE DADOS ---
    
    def carregar_json_historia(self):
        """Carrega o arquivo principal de narrativa"""
        caminho = os.path.join(os.path.dirname(__file__), '..', 'data', 'historia.json')
        try:
            if os.path.exists(caminho):
                with open(caminho, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar historia.json: {e}")
        return {}

    def carregar_json_generico(self, nome_arquivo):
        """Lê arquivos da pasta data (itens.json, magias.json, etc)"""
        caminho = os.path.join(os.path.dirname(__file__), '..', 'data', nome_arquivo)
        try:
            if os.path.exists(caminho):
                with open(caminho, 'r', encoding='utf-8') as f:
                    return json.load(f)
            print(f"Aviso: Ficheiro {nome_arquivo} não encontrado em {caminho}")
        except Exception as e:
            print(f"Erro ao ler {nome_arquivo}: {e}")
        return []

    # --- 2. FLUXO DE TELAS (NAVEGAÇÃO) ---

    def exibir_menu_inicial(self):
        """Exibe a tela de abertura do jogo"""
        callbacks = {
            'novo_jogo': self.iniciar_novo_jogo,
            'continuar': lambda: print("Recurso 'Continuar' em desenvolvimento."),
            'tutorial': self.exibir_tutorial,
            'config': self.abrir_configuracoes
        }
        self.tela_atual = MenuPrincipal(self.root, callbacks)

    def iniciar_novo_jogo(self):
        """Prepara o sistema para uma nova jornada"""
        self.tela_atual.destruir()
        self.personagem = Personagem()
        self.ui = JogoInterface(self.root)
        
        # Configura o botão inicial para o sorteio de atributos
        self.ui.btn_iniciar.configure(
            text="[ ROLAR ATRIBUTOS ]", 
            command=self.clicou_rolar_dados,
            state="normal"
        )
        
        self.ui.exibir_texto_maquina(
            "BEM-VINDO, JOVEM MAGO.\n\n"
            "Antes de partirmos para a Cidadela, precisamos definir sua força e sua conexão com o arcano.\n"
            "Clique no botão abaixo para lançar os dados."
        )

    # --- 3. MECÂNICAS DE CRIAÇÃO ---

    def clicou_rolar_dados(self):
        """Inicia animação e bloqueia o botão para evitar erros"""
        self.ui.btn_iniciar.configure(state="disabled")
        self.ui.animar_dado(1500)
        
        # Sorteia valores via Engine
        hab, ene, sor, mag = Engine.calcular_atributos_iniciais()
        
        # Aguarda o fim do GIF para processar os resultados
        self.ui.root.after(1500, lambda: self.finalizar_setup_atributos(hab, ene, sor, mag))

    def finalizar_setup_atributos(self, hab, ene, sor, mag):
        """Aplica os dados ao personagem e habilita a escolha de magias"""
        self.personagem.habilidade = hab
        self.personagem.energia = ene
        self.personagem.sorte = sor
        self.personagem.pontos_magia = mag
        
        # Atualiza o cabeçalho visual
        self.ui.atualizar_stats(hab, ene, sor, mag)
        
        # Muda o comportamento do botão para a fase de Magias
        self.ui.btn_iniciar.configure(
            state="normal", 
            text="[ ESCOLHER ENCANTOS ]", 
            command=self.abrir_selecao_magias
        )

        msg = (
            "DESTINO TRAÇADO!\n\n"
            f"Seus atributos iniciais: \nHabilidade {hab},\n Energia {ene},\n Sorte {sor}.\n"
            f"Você tem direito a {mag} pontos de Magia.\n\n"
            "Abra seu grimório agora para escolher seus feitiços."
        )
        self.ui.exibir_texto_maquina(msg)

    def abrir_selecao_magias(self):
        """Transição para a tela de cards de magia"""
        print("Debug: Abrindo tela de seleção de magias...")
        
        # 1. Troca o "palco" de texto por cards
        palco = self.ui.preparar_palco_para_cards()
        
        # 2. Carrega as magias do JSON
        dados_magias = self.carregar_json_generico('magias.json')
        
        if not dados_magias:
            print("Erro: Não foi possível carregar as magias para exibição.")
            return

        # 3. Inicia o gerenciador de cards no palco central
        self.tela_cards = GerenciadorCards(
            palco, 
            self.personagem.pontos_magia, 
            self.finalizar_escolha_magias
        )
        self.tela_cards.exibir("GRIMÓRIO DE ENCANTOS", dados_magias, "magias")
        
        # 4. Esconde o botão inferior da UI (o GerenciadorCards terá seu próprio botão)
        self.ui.btn_iniciar.pack_forget()

    def finalizar_escolha_magias(self, escolhidas):
        """Salva as magias e inicia a história real"""
        self.personagem.encantos = escolhidas
        self.ui.restaurar_palco_para_texto()
        
        # Re-exibe o botão de baixo caso precise (ou limpa se usar botões do JSON)
        # self.ui.btn_iniciar.pack(side="bottom", pady=15) 
        
        self.carregar_nodo("introducao_1")

    # --- 4. NARRATIVA E JOGO ---

    def carregar_nodo(self, chave):
        """Navega pelos parágrafos do livro-jogo"""
        dados = self.biblioteca_historia.get(chave)
        if dados:
            self.ui.limpar_botoes()
            self.ui.atualizar_ilustracao(dados.get("imagem"))
            self.ui.exibir_texto_maquina(dados["texto"])
            
            for opcao in dados["opcoes"]:
                # Importante: o command usa uma 'default variable' d=... para evitar bugs de loop
                self.ui.criar_botao_escolha(
                    opcao["texto"], 
                    lambda d=opcao["ir_para"]: self.carregar_nodo(d)
                )

    def exibir_tutorial(self):
        print("Tutorial clicado.")

    def abrir_configuracoes(self):
        print("Configurações clicadas.")