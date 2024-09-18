from enum import Enum

'''
Enum.member.name: Retorna o Nome do Enumerador.
Enum.member.value: Retorna o Valor do Enumerador.
Enum(member_name): Converte uma string para um Enumerador.
Enum(value): Converte um valor para um Enumerador.
'''
class Direcao(Enum):
    DIREITA = 1
    ESQUERDA = 2