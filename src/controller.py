import json
import os
from src.menu import MenuPrincipal
from src.interface import JogoInterface
from src.personagem import Personagem
from src.engine import Engine

class JogoController:
    def __init__(self, root):
        self.root = root
        self.personagem = None # Será instanciado no Novo Jogo
        self.biblioteca_historia = self.carregar_json()
        self.exibir_menu_inicial()

    def carregar_json(self):
        """Carrega os parágrafos do livro"""
        caminho = os.path.join(os.path.dirname(__file__), '..', 'data', 'historia.json')
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def exibir_menu_inicial(self):
        """Monta a tela de Menu"""
        callbacks = {
            'novo_jogo': self.iniciar_novo_jogo,
            'continuar': lambda: print("Continuar em breve..."),
            'tutorial': self.exibir_tutorial,
            'config': self.abrir_configuracoes
        }
        self.tela_atual = MenuPrincipal(self.root, callbacks)

    def iniciar_novo_jogo(self):
        """Prepara a ficha de personagem e a interface de jogo"""
        self.tela_atual.destruir() # Remove o menu
        
        # 1. Cria um novo personagem "vazio"
        self.personagem = Personagem()
        
        # 2. Inicia a interface principal do jogo
        self.ui = JogoInterface(self.root)
        
        # 3. Conecta o botão da interface à rolagem de dados
        self.ui.btn_iniciar.configure(text="[ ROLAR ATRIBUTOS ]", command=self.clicou_rolar_dados)
        
        # 4. Mensagem inicial na janela branca
        self.ui.exibir_texto_maquina(
            "BEM-VINDO, JOVEM MAGO.\n\n"
            "Antes de partirmos para a Cidadela do Caos, precisamos definir sua força, "
            "sua vitalidade e sua conexão com as artes arcanas.\n\n"
            "Clique no botão abaixo para lançar os dados de destino."
        )

    def clicou_rolar_dados(self):
        """Inicia a animação e o sorteio"""
        self.ui.btn_iniciar.configure(state="disabled") # Evita cliques múltiplos
        self.ui.animar_dado(1500)
        
        # Sorteio via Engine
        hab, ene, sor, mag = Engine.calcular_atributos_iniciais()
        
        # Agenda a finalização para depois do GIF (1.5s)
        self.ui.root.after(1500, lambda: self.finalizar_criacao(hab, ene, sor, mag))

    def finalizar_criacao(self, hab, ene, sor, mag):
        """Aplica os resultados e prepara para a história"""
        self.personagem.habilidade = hab
        self.personagem.energia = ene
        self.personagem.sorte = sor
        self.personagem.pontos_magia = mag
        
        # Atualiza os ícones coloridos no topo
        self.ui.atualizar_stats(hab, ene, sor, mag)
        
        msg = (
            "OS DADOS FORAM LANÇADOS!\n\n"
            f"HABILIDADE: {hab}\nENERGIA: {ene}\nSORTE: {sor}\nMAGIA: {mag}\n\n"
            "Seus atributos iniciais estão definidos. Agora, você deve se preparar para "
            "ouvir a história do Vale dos Salgueiros."
        )
        self.ui.exibir_texto_maquina(msg)
        
        # Muda o botão para avançar para a introdução
        self.ui.btn_iniciar.configure(
            state="normal",
            text="[ OUVIR A HISTÓRIA ]", 
            command=lambda: self.carregar_nodo("introducao_1")
        )

    def carregar_nodo(self, chave):
        """Lógica de navegação pela história (JSON)"""
        dados = self.biblioteca_historia.get(chave)
        if dados:
            self.ui.limpar_botoes()
            self.ui.atualizar_ilustracao(dados.get("imagem"))
            self.ui.exibir_texto_maquina(dados["texto"])
            
            # Cria botões dinâmicos para as opções do JSON
            for opcao in dados["opcoes"]:
                self.ui.criar_botao_escolha(
                    opcao["texto"], 
                    lambda d=opcao["ir_para"]: self.carregar_nodo(d)
                )

    # --- Outras Telas ---
    def exibir_tutorial(self):
        # Implementar lógica de tela de tutorial ou apenas texto na interface
        pass

    def abrir_configuracoes(self):
        # Implementar tela de configurações
        pass