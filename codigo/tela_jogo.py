from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto
import random


def desenha_tela(janela, estado, altura_tela, largura_tela):
    # Utilize o dicionário estado para saber onde o jogador e os outros objetos estão.
    # Por exemplo, para saber a posição do jogador, use estado['pos_jogador']
    # O mapa esta armazenado em estado['mapa'].
    motor.preenche_fundo(janela, PRETO)
    
    # O seu código deve desenhar a tela do jogo aqui a partir dos valores no dicionário "estado"

    altura_mapa = len(estado["mapa"])
    largura_mapa = len(estado["mapa"][0])

    inicio_y = (altura_tela - altura_mapa) // 2
    inicio_x = (largura_tela - largura_mapa) // 2

    #desenha o mapa
    for v in range(altura_mapa):
        for h in range(largura_mapa):
            if estado["mapa"][v][h] == ' ':
                motor.desenha_string(janela, inicio_x + h, inicio_y + v, ' ', VERDE_ESCURO, BRANCO)
            else:
                 motor.desenha_string(janela, inicio_x + h, inicio_y + v, PAREDE, MARROM_ESCURO, MARROM_ESCURO)

    #desenha os objetos
    for obj in estado["objetos"]:
        motor.desenha_string(janela, obj["posicao"][0] + inicio_x, obj["posicao"][1] + inicio_y, obj["tipo"], VERDE_ESCURO, obj["cor"])

    #desenha o jogador
    motor.desenha_string(janela, estado["pos_jogador"][0] + inicio_x, estado["pos_jogador"][1] + inicio_y , '@', VERDE_ESCURO, AZUL)

    #desenha a mensagem
    motor.desenha_string(janela, inicio_x, inicio_y + altura_mapa + 2, estado["mensagem"], PRETO, BRANCO)

    #vidas
    for i in range(estado["vidas"]):
         motor.desenha_string(janela, inicio_x + i*2, inicio_y - 2, "❤", PRETO, VERMELHO)

    for i in range(estado["vidas"], estado["max_vidas"]):
             motor.desenha_string(janela, inicio_x + i*2, inicio_y - 2, "🤍", PRETO, BRANCO)
         



    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla):
    # O seu código deve atualizar o dicionário "estado" com base na tecla apertada pelo jogador
    # Por exemplo, se o jogador apertar a seta para a esquerda (o valor da variável será "ESQUERDA"), 
    # o seu código deve atualizar o dicionário estado['pos_jogador'][0] -= 1

    # Mude o valor da chave 'tela_atual' para mudar de tela
    
    # Começamos apagando a mensagem anterior, pois ela já foi mostrada no frame anterior
    estado['mensagem'] = ''

    #gera uma lista com as posuções dos monstros safados
    pos_monstros = []
    for obj in estado["objetos"]:
         if obj["tipo"] == MONSTRO:
              pos_monstros.append(obj["posicao"])



    if tecla == motor.SETA_ESQUERDA:
        if (not estado["pos_jogador"][0] == 0) and estado["mapa"][estado["pos_jogador"][1]][estado["pos_jogador"][0] - 1] == " ":

            #vê se tem monstros ou não para atacar ou não
            if not [estado["pos_jogador"][0]-1,estado["pos_jogador"][1]] in pos_monstros: 
                estado["pos_jogador"][0] -= 1
            else:
                 atacar_monstro(estado, [estado["pos_jogador"][0]-1,estado["pos_jogador"][1]])
        else:
             estado["mensagem"] = "Você não pode andar alí doido!"

    if tecla == motor.SETA_DIREITA:
            if (not estado["pos_jogador"][0] == len(estado["mapa"][0]) - 1) and estado["mapa"][estado["pos_jogador"][1]][estado["pos_jogador"][0] + 1] == " ":

                #vê se tem monstros ou não para atacar ou não
                if not [estado["pos_jogador"][0]+1,estado["pos_jogador"][1]] in pos_monstros: 
                    estado["pos_jogador"][0] += 1
                else:
                    atacar_monstro(estado, [estado["pos_jogador"][0]+1,estado["pos_jogador"][1]])
            else:
                estado["mensagem"] = "Você não pode andar alí doido!"

    if tecla == motor.SETA_CIMA:
            if (not estado["pos_jogador"][1] == 0) and estado["mapa"][estado["pos_jogador"][1]-1][estado["pos_jogador"][0]] == " ":

                #vê se tem monstros ou não para atacar ou não
                if not [estado["pos_jogador"][0],estado["pos_jogador"][1]-1] in pos_monstros: 
                    estado["pos_jogador"][1] -= 1
                else:
                    atacar_monstro(estado, [estado["pos_jogador"][0],estado["pos_jogador"][1]-1])
            else:
                estado["mensagem"] = "Você não pode andar alí doido!"

    if tecla == motor.SETA_BAIXO:
            if (not estado["pos_jogador"][1] == len(estado["mapa"]) - 1) and estado["mapa"][estado["pos_jogador"][1]+1][estado["pos_jogador"][0]] == " ":
                #vê se tem monstros ou não para atacar ou não
                if not [estado["pos_jogador"][0],estado["pos_jogador"][1]+1] in pos_monstros: 
                    estado["pos_jogador"][1] += 1
                else:
                    atacar_monstro(estado, [estado["pos_jogador"][0],estado["pos_jogador"][1]+1])
            else:
                estado["mensagem"] = "Você não pode andar alí doido!"

    #colisões uhuul

    for obj in estado["objetos"]:
         if estado["pos_jogador"] == obj["posicao"]:
            #qual bichinho
            if obj["tipo"] == CORACAO:
                if not estado["vidas"] == estado["max_vidas"]:
                    estado["vidas"] += 1
                    estado["mensagem"] = "Você coletou um coração e restaurou uma vida"
                estado["objetos"].remove(obj)

            if obj["tipo"] == ESPINHO:
                 estado["vidas"] -= 1
                 estado["mensagem"] = "Você perdeu 1 de vida"
                 if estado["vidas"] == 0:
                      estado['tela_atual'] = SAIR

    monstro_andar(estado)
                 
                      


    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR
          

def atacar_monstro(estado, pos_monstro):
     for obj in estado["objetos"]:
          if obj["posicao"] == pos_monstro:
                obj["pode_andar"] = False
                if random.random() < obj["probabilidade"]:
                    estado["mensagem"] = "Aquele bicho te atacou! aaahh"
                    estado["vidas"] -= 1
                    if estado["vidas"] == 0:
                        estado['tela_atual'] = SAIR
                else:
                    estado["mensagem"] = "Você atacou o montro e ele perdeu 1 de vida"
                    obj["vidas"] -= 1
                    if obj["vidas"] == 0:
                         estado["mensagem"] = "O monstro morreu tadinho..."
                         estado["objetos"].remove(obj)
                         estado["pos_jogador"] = pos_monstro


def monstro_andar(estado):
     for obj in estado["objetos"]:
          if obj["tipo"] == MONSTRO:
                if obj["pode_andar"] == True:
                    direcao = random.choice([1,2,3,4])

                    #cima
                    if direcao == 1:
                        if (not obj["posicao"][1] == 0) and estado["mapa"][obj["posicao"][1]-1][obj["posicao"][0]] == ' ':
                            obj["posicao"][1] -= 1
                    #baixo
                    if direcao == 2:
                        if (not obj["posicao"][1] == len(estado["mapa"]) - 1) and estado["mapa"][obj["posicao"][1]+1][obj["posicao"][0]] == ' ':
                            obj["posicao"][1] += 1
                    #esquerda
                    if direcao == 3:
                        if (not obj["posicao"][0] == 0) and estado["mapa"][obj["posicao"][1]][obj["posicao"][0]-1] == ' ':
                            obj["posicao"][0] -= 1
                    #direita
                    if direcao == 4:
                        if (not obj["posicao"][0] == len(estado["mapa"][0]) - 1) and estado["mapa"][obj["posicao"][1]][obj["posicao"][0]+1] == ' ':
                            obj["posicao"][0] += 1

                else:
                    obj["pode_andar"] = True
