from src.personagem import Personagem
from src.engine import Engine

class JogoController:
    def __init__(self, interface):
        self.ui = interface
        self.personagem = Personagem()
        
        # Conecta o botão da interface ao método do controlador
        self.ui.btn_iniciar.configure(command=self.clicou_iniciar)

    def clicou_iniciar(self):
        """Lógica disparada quando o jogador clica em Iniciar"""
        # 1. Pedir para a View rodar a animação
        self.ui.animar_dado(1500)
        
        # 2. Lógica de sorteio (Model/Engine)
        hab, ene, sor, mag = Engine.calcular_atributos_iniciais()
        
        # 3. Atualizar o Model (Personagem) em segredo
        self.personagem.habilidade = hab
        self.personagem.energia = ene
        self.personagem.sorte = sor
        self.personagem.pontos_magia = mag
        
        # 4. Agendar a atualização da View (Output visual) após o tempo do dado
        self.ui.root.after(1500, lambda: self.finalizar_setup(hab, ene, sor, mag))

    def finalizar_setup(self, hab, ene, sor, mag):
        self.ui.atualizar_stats(hab, ene, sor, mag)
        msg = (
            "OS DADOS FORAM LANÇADOS!\n\n"
            "Sua jornada começa com:\n" 
            f"{hab} pontos de Habilidade, \n" 
            f"{ene} pontos de energia, \n"
            f"{sor} pontos de sorte, \n"
            f"{mag} pontos de Magia.\n"
            "Prepare-se, pois os perigos da Cidadela não perdoam erros."
        )
        self.ui.exibir_texto(msg)