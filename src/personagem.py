import random

class Personagem:
    def __init__(self):
        # Atributos principais
        self.habilidade_inicial = self.rolar_dados(1) + 6
        self.energia_inicial = self.rolar_dados(2) + 12
        self.sorte_inicial = self.rolar_dados(1) + 6
        
        # Atributos atuais (que vão mudar durante o jogo)
        self.habilidade = self.habilidade_inicial
        self.energia = self.energia_inicial
        self.sorte = self.sorte_inicial
        
        # Magia: 2 dados + 6 determinam quantos PONTOS de magia você tem
        # Cada feitiço custa 1 ponto (exceto alguns casos específicos)
        self.pontos_magia_inicial = self.rolar_dados(2) + 6
        self.pontos_magia = self.pontos_magia_inicial
        
        # Lista de feitiços escolhidos
        self.encantos = []

    def rolar_dados(self, quantidade=1):
        """Simula a rolagem de dados de 6 faces"""
        return sum(random.randint(1, 6) for _ in range(quantidade))

    def resetar(self):
        """Reinicia os atributos para um novo jogo"""
        self.__init__()

    def status_formatado(self):
        """Retorna os valores para serem usados na interface"""
        return (self.habilidade, self.energia, self.sorte, self.pontos_magia)