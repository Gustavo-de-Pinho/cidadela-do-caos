import random
import time

#como as coisas acontecem, é aqui

class Engine:
    @staticmethod
    def rolar_dados(quantidade=1):
        """Retorna uma lista com os valores de cada dado"""
        return [random.randint(1, 6) for _ in range(quantidade)]

    @staticmethod
    def calcular_atributos_iniciais():
        """Segue as regras do livro para criar o personagem"""
        hab = sum(Engine.rolar_dados(1)) + 6
        ene = sum(Engine.rolar_dados(2)) + 12
        sor = sum(Engine.rolar_dados(1)) + 6
        mag = sum(Engine.rolar_dados(2)) + 6
        return hab, ene, sor, mag