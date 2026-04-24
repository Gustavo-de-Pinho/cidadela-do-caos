import random
import time

class Engine:
    @staticmethod
    def rolar_dados(quantidade=1):
        """Retorna uma lista com os valores de cada dado"""
        return [random.randint(1, 6) for _ in range(quantidade)]

    @staticmethod
    def calcular_atributos_iniciais():
        """Segue as regras do livro para criar o personagem"""
        hab = random.randint(1, 6) + 6
        ene = random.randint(1, 6) + random.randint(1, 6) + 12
        sor = random.randint(1, 6) + 6
        mag = random.randint(1, 6) + random.randint(1, 6) + 6
        return hab, ene, sor, mag