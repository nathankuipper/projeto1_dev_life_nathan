from random import randint
import ast

from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código


def gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa, mapa):
    # Implemente esta função para o nível básico
    # A função deve retornar uma posição aleatória dentro da janela que não esteja na lista de posições ocupadas.
    # Uma posição é uma lista com exatas dois elementos: a posição x e a posição y.
    # Além disso, a posição gerada deve ser adicionada à lista de posições ocupadas.
    
    # O código abaixo é apenas um exemplo. Você deve apagar este código e escrever o seu, fazendo o que foi pedido acima.
    while True:
        x = randint(1, largura_mapa-2)
        y = randint(1, altura_mapa-2)
        posicao = [x, y]
        if posicao not in posicoes_ocupadas and not mapa[y][x] == PAREDE:
            posicoes_ocupadas.append(posicao)
            break
    
    return posicao


def gera_objetos(quantidade, tipo, cor, largura_mapa, altura_mapa, posicoes_ocupadas, mapa):
    """
    Esta função já está pronta, você não precisa modificá-la.

    Gera uma lista de objetos do tipo especificado, com a quantidade especificada.
    Cada objeto é um dicionário com as chaves 'tipo', 'posicao' e 'cor'.

    Parâmetros:
    quantidade: quantidade de objetos a serem gerados
    tipo: tipo do objeto a ser gerado. É uma string como '❤'
    cor: cor do objeto a ser gerado. É uma lista com três elementos, como [255, 0, 0]
    largura_mapa: largura do mapa do jogo em caracteres
    altura_mapa: altura do mapa do jogo em caracteres
    posicoes_ocupadas: lista de posições ocupadas no mapa. Cada posição é uma lista com exatamente dois elementos: a posição x e a posição y.
    """
    objetos = []

    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa, mapa)
        objetos.append({
            'tipo': tipo,
            'posicao': posicao,
            'cor': cor,
        })

    return objetos


def inicializa_estado():
    # Cria lista de listas, cada uma com 50 espaços em branco
    # Você pode mudar esta lista, inclusive seu tamanho, à vontade
    mapa = []
    with open("mapa1.txt", "r", encoding="utf-8") as arquivo:
        texto = arquivo.read().split("\n")
        for linha in texto:
            eixo = []
            for caractere in linha:
                if caractere == "-":
                    eixo.append(" ")
                else:
                    eixo.append("▣")
            mapa.append(eixo)


    
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
    
    # Você pode colocar o jogador em outro lugar, se preferir
    pos_jogador = [largura_mapa//2, altura_mapa//2]  # Meio do mapa
    
    # Cria outros objetos do mapa
    posicoes_ocupadas = [pos_jogador]

    #guarda em um arquivo a lista dos objetos
    with open("objetos.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write("")

    linhas = []
    for i in range(4):
        posicoes_ocupadas = [pos_jogador]
        objetos = []
        if not i == 3:
            objetos += gera_objetos(4, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_objetos(5, ESPINHO, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_monstro(3, MONSTRO, ROXO, 5, 0.3, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_objetos(3, VIDA_MAX, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_objetos(4, POCAO_VIDA, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_objetos(1, ESPADA, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_objetos(1, OCULOS, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_monstro(2, COBRA, PRETO, 5, 0.3, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_monstro(1, PERSEGUIDOR, ROXO, 5, 0.3, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_objetos(1, REPELENTE, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_objetos(1, CHAVE, AMARELO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
        else:
            objetos += gera_objetos(20, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
            objetos += gera_objetos(7, VIDA_MAX, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas, mapa)
        
        with open("objetos.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(str(objetos) + "\n")

    # with open("objetos.txt", "w", encoding="utf-8") as arquivo:
    #     #print(linhas)
    #     arquivo.writelines(linhas)

    with open("objetos.txt", "r", encoding="utf-8") as arquivo:
        listas_de_objetos = [
            ast.literal_eval(linha.strip())
            for linha in arquivo
            if linha.strip()
            ]
    objetos = listas_de_objetos[0]
    
    return {
        'tela_atual': TELA_INICIO,
        'pos_jogador': pos_jogador,
        'vidas': 5,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos,
        'mapa': mapa,
        'mensagem': '',  # Use esta mensagem para mostrar mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
        'itens': {"cura":0, "vida_max":0, "espada":2, "oculos": 3, "repelente": 1, "chaves":0},
        'configs': {'selecionado': 1, "mensagem": "", "maximo": 10, "peso":0, "dano":1, "tela":1},
        'equipamento': None,
        'experiencia': {'xp': 0, 'nivel':1}
    }


def gera_monstro(quantidade, tipo, cor, vidas, probabilidade_ataque, largura_mapa, altura_mapa, posicoes_ocupadas, mapa):
    """gera monstros assustadores no mapa boooo!"""
    objetos = []

    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa, mapa)
        objetos.append({
            'tipo': MONSTRO,
            'posicao': posicao,
            'cor': cor,
            'vidas': vidas,
            'probabilidade': probabilidade_ataque,
            'pode_andar': True,
            'categoria': tipo,
            'anteriores': [[posicao[0]-1,posicao[1]], [posicao[0]-2,posicao[1]], [posicao[0]-3,posicao[1]]],
            'anterior': 4
        })

    return objetos