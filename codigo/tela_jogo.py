from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto
import random
import ast


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
                motor.desenha_string(janela, inicio_x + h, inicio_y + v, ' ', VERDE_ESCURO, VERDE_ESCURO)
            else:
                 motor.desenha_string(janela, inicio_x + h, inicio_y + v, PAREDE, MARROM_ESCURO, MARROM_ESCURO)

    #desenha os objetos
    for obj in estado["objetos"]:
        if obj["tipo"] == MONSTRO:
            motor.desenha_string(janela, obj["posicao"][0] + inicio_x, obj["posicao"][1] + inicio_y, obj["categoria"], VERDE_ESCURO, obj["cor"])
            if obj["categoria"] == COBRA:
                for rabo in obj["anteriores"]:
                    motor.desenha_string(janela, rabo[0] + inicio_x, rabo[1] + inicio_y, "o", VERDE_ESCURO, obj["cor"])
        else:
            motor.desenha_string(janela, obj["posicao"][0] + inicio_x, obj["posicao"][1] + inicio_y, obj["tipo"], VERDE_ESCURO, obj["cor"])

    #desenha o jogador
    if estado["equipamento"] == None:
        motor.desenha_string(janela, estado["pos_jogador"][0] + inicio_x, estado["pos_jogador"][1] + inicio_y , JOGADOR, VERDE_ESCURO, AZUL)
    elif estado["equipamento"] == "Espada":
        motor.desenha_string(janela, estado["pos_jogador"][0] + inicio_x, estado["pos_jogador"][1] + inicio_y , "😠", VERDE_ESCURO, AZUL)
    elif estado["equipamento"] == "Óculos":
        motor.desenha_string(janela, estado["pos_jogador"][0] + inicio_x, estado["pos_jogador"][1] + inicio_y , "😎", VERDE_ESCURO, AZUL)
    elif estado["equipamento"] == "Repelente":
        motor.desenha_string(janela, estado["pos_jogador"][0] + inicio_x, estado["pos_jogador"][1] + inicio_y , "🤢", VERDE_ESCURO, AZUL)

    #desenha a mensagem
    motor.desenha_string(janela, inicio_x, inicio_y + altura_mapa + 2, estado["mensagem"], PRETO, BRANCO)

    #vidas
    for i in range(estado["vidas"]):
         motor.desenha_string(janela, inicio_x + i*2, inicio_y - 2, "❤", PRETO, VERMELHO)

    for i in range(estado["vidas"], estado["max_vidas"]):
             motor.desenha_string(janela, inicio_x + i*2, inicio_y - 2, "🤍", PRETO, BRANCO)

    #nivel
    motor.desenha_string(janela, inicio_x+40, inicio_y-2, f"nivel: {estado["experiencia"]["nivel"]}, XP:{estado["experiencia"]["xp"]}/10", PRETO, BRANCO)
         

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
                    if estado["equipamento"] == "Óculos":
                        estado["equipamento"] = None
                        estado["vidas"] = 1
                        estado["mensagem"] = "Seu óculos quebrou"
                    else:
                        estado['tela_atual'] = TELA_GAMEOVER

            if obj["tipo"] == POCAO_VIDA:
                if not estado["configs"]["peso"] == estado["configs"]["maximo"]:
                    estado["itens"]["cura"] += 1
                    estado["mensagem"] = "Você coletou uma poção de vida"
                estado["objetos"].remove(obj)

            elif obj["tipo"] == VIDA_MAX:
                if not estado["configs"]["peso"] == estado["configs"]["maximo"]:
                    estado["itens"]["vida_max"] += 1
                    estado["mensagem"] = "Você coletou uma poção de aumentar a vida"
                estado["objetos"].remove(obj)

            elif obj["tipo"] == ESPADA:
                if not estado["configs"]["peso"] == estado["configs"]["maximo"]:
                    estado["itens"]["espada"] += 1
                    estado["mensagem"] = "Você coletou uma espada"
                estado["objetos"].remove(obj)

            elif obj["tipo"] == OCULOS:
                if not estado["configs"]["peso"] == estado["configs"]["maximo"]:
                    estado["itens"]["oculos"] += 1
                    estado["mensagem"] = "Você coletou um óculos"
                estado["objetos"].remove(obj)

            elif obj["tipo"] == REPELENTE:
                if not estado["configs"]["peso"] == estado["configs"]["maximo"]:
                    estado["itens"]["repelente"] += 1
                    estado["mensagem"] = "Você coletou um repelente"
                estado["objetos"].remove(obj)

            elif obj["tipo"] == CHAVE:
                estado["chaves"] += 1
                estado["mensagem"] = "Você coletou uma chave... talvez eu deva tentar achar mais algumas"
                estado["objetos"].remove(obj)

            

    monstro_andar(estado)

    if estado["equipamento"] == "Espada":
        estado["configs"]["dano"] = 2
    else:
        estado["configs"]["dano"] = 1

    peso = 0
    for i in estado["itens"].values():
        peso += i
    estado["configs"]["peso"] = peso

    if tecla == "l":
        trocar_mapa(2, [1,1], estado)

    if tecla == "k":
        trocar_mapa(1, [1,1], estado)
                
                      
    if estado["pos_jogador"][0] == 49:
        trocar_mapa(2, [1,7], estado)

    if estado["pos_jogador"][0] == 0:
        trocar_mapa(1, [48,7], estado)

    if estado["pos_jogador"][1] == 0 and estado["configs"]["tela"] == 2:
        trocar_mapa(3, [24,18], estado)

    if estado["pos_jogador"][1] == 0 and estado["configs"]["tela"] == 1:
        trocar_mapa(4, [24,18], estado)

    if estado["pos_jogador"][1] == 19 and estado["configs"]["tela"] == 3:
        trocar_mapa(2, [24,1], estado)

    if estado["pos_jogador"][1] == 19 and estado["configs"]["tela"] == 4:
        trocar_mapa(1, [8,1], estado)

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['configs']['selecionado'] = 1
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
                        if estado["equipamento"] == "Óculos":
                            estado["equipamento"] = None
                            estado["vidas"] = 1
                            estado["mensagem"] = "Seu óculos quebrou"
                        else:
                            estado['tela_atual'] = TELA_GAMEOVER
                else:
                    estado["mensagem"] = f"Você atacou o montro e ele perdeu {estado["configs"]["dano"]} de vida"
                    obj["vidas"] -= estado["configs"]["dano"]
                    if obj["vidas"] <= 0:
                        if obj["categoria"] == MONSTRO:
                            estado["mensagem"] = "O monstro morreu e você ganhou 2 de xp"
                            estado["experiencia"]["xp"] += 2
                        elif obj["categoria"] == COBRA:
                            estado["mensagem"] = "O monstro morreu e você ganhou 4 de xp"
                            estado["experiencia"]["xp"] += 4

                        elif obj["categoria"] == PERSEGUIDOR:
                            estado["mensagem"] = "O monstro morreu e você ganhou 5 de xp"
                            estado["experiencia"]["xp"] += 5
                         
                        estado["objetos"].remove(obj)
                        estado["pos_jogador"] = pos_monstro
                        if estado["experiencia"]["xp"] >= 10:
                             estado["experiencia"]["xp"] = 0
                             estado["experiencia"]["nivel"] += 1
                             estado["configs"]["maximo"] += 1
                             estado["mensagem"] = "Você evoluiu de nivel e aumentou a mochila"



def monstro_andar(estado):
     for obj in estado["objetos"]:
        if obj["tipo"] == MONSTRO:
            if estado["equipamento"] == "Repelente" and ((obj["posicao"][0] - estado["pos_jogador"][0])**2 + (obj["posicao"][1] - estado["pos_jogador"][1])**2)**0.5 < 3:
                obj["pode_andar"] = False

            if obj["categoria"] == MONSTRO:
                if obj["pode_andar"] == True:
                    direcao = random.choice([1,2,3,4])

                    #cima
                    if direcao == 1:
                        if (not obj["posicao"][1] == 0) and estado["mapa"][obj["posicao"][1]-1][obj["posicao"][0]] == ' ' and not obj["posicao"][1]-1 == estado["pos_jogador"][1]:
                            obj["posicao"][1] -= 1
                    #baixo
                    if direcao == 2:
                        if (not obj["posicao"][1] == len(estado["mapa"]) - 1) and estado["mapa"][obj["posicao"][1]+1][obj["posicao"][0]] == ' ' and not obj["posicao"][1]+1 == estado["pos_jogador"][1]:
                            obj["posicao"][1] += 1
                    #esquerda
                    if direcao == 3:
                        if (not obj["posicao"][0] == 0) and estado["mapa"][obj["posicao"][1]][obj["posicao"][0]-1] == ' ' and not obj["posicao"][0]-1 == estado["pos_jogador"][0]:
                            obj["posicao"][0] -= 1
                    #direita
                    if direcao == 4:
                        if (not obj["posicao"][0] == len(estado["mapa"][0]) - 1) and estado["mapa"][obj["posicao"][1]][obj["posicao"][0]+1] == ' ' and not obj["posicao"][0]+1 == estado["pos_jogador"][0]:
                            obj["posicao"][0] += 1

                else:
                    obj["pode_andar"] = True

            elif obj["categoria"] == COBRA:
                if obj["pode_andar"] == True:
                    direcao = random.choice([1,2,3,4])

                    #cima
                    if direcao == 1:
                        if (not obj["posicao"][1] == 0) and estado["mapa"][obj["posicao"][1]-1][obj["posicao"][0]] == ' ' and not obj["posicao"][1]-1 == estado["pos_jogador"][1] and not obj["anterior"] == 2:
                            obj["anterior"] = 1

                            obj["anteriores"][2][0] = obj['anteriores'][1][0]
                            obj["anteriores"][2][1] = obj['anteriores'][1][1]

                            obj["anteriores"][1][0] = obj['anteriores'][0][0]
                            obj["anteriores"][1][1] = obj['anteriores'][0][1]

                            obj["anteriores"][0][0] = obj['posicao'][0]
                            obj["anteriores"][0][1] = obj['posicao'][1]

                            obj["posicao"][1] -= 1

                    #baixo
                    if direcao == 2:
                        if (not obj["posicao"][1] == len(estado["mapa"]) - 1) and estado["mapa"][obj["posicao"][1]+1][obj["posicao"][0]] == ' ' and not obj["posicao"][1]+1 == estado["pos_jogador"][1] and not obj["anterior"] == 1:
                            obj["anterior"] = 2

                            obj["anteriores"][2][0] = obj['anteriores'][1][0]
                            obj["anteriores"][2][1] = obj['anteriores'][1][1]

                            obj["anteriores"][1][0] = obj['anteriores'][0][0]
                            obj["anteriores"][1][1] = obj['anteriores'][0][1]

                            obj["anteriores"][0][0] = obj['posicao'][0]
                            obj["anteriores"][0][1] = obj['posicao'][1]

                            obj["posicao"][1] += 1

                    #esquerda
                    if direcao == 3:
                        if (not obj["posicao"][0] == 0) and estado["mapa"][obj["posicao"][1]][obj["posicao"][0]-1] == ' ' and not obj["posicao"][0]-1 == estado["pos_jogador"][0] and not obj["anterior"] == 4:
                            obj["anterior"] = 3

                            obj["anteriores"][2][0] = obj['anteriores'][1][0]
                            obj["anteriores"][2][1] = obj['anteriores'][1][1]

                            obj["anteriores"][1][0] = obj['anteriores'][0][0]
                            obj["anteriores"][1][1] = obj['anteriores'][0][1]

                            obj["anteriores"][0][0] = obj['posicao'][0]
                            obj["anteriores"][0][1] = obj['posicao'][1]
                            
                            obj["posicao"][0] -= 1

                    #direita
                    if direcao == 4:
                        if (not obj["posicao"][0] == len(estado["mapa"][0]) - 1) and estado["mapa"][obj["posicao"][1]][obj["posicao"][0]+1] == ' ' and not obj["posicao"][0]+1 == estado["pos_jogador"][0] and not obj["anterior"] == 3:
                            obj["anterior"] = 4

                            obj["anteriores"][2][0] = obj['anteriores'][1][0]
                            obj["anteriores"][2][1] = obj['anteriores'][1][1]

                            obj["anteriores"][1][0] = obj['anteriores'][0][0]
                            obj["anteriores"][1][1] = obj['anteriores'][0][1]

                            obj["anteriores"][0][0] = obj['posicao'][0]
                            obj["anteriores"][0][1] = obj['posicao'][1]
                            
                            obj["posicao"][0] += 1

            elif obj["categoria"] == PERSEGUIDOR:
                if obj["pode_andar"] == True:
                    if abs(obj["posicao"][1] - estado["pos_jogador"][1]) > abs(obj["posicao"][0] - estado["pos_jogador"][0]):
                        if obj["posicao"][1] - estado["pos_jogador"][1] > 0:
                            direcao = 1
                        else:
                            direcao = 2
                    else:
                        if obj["posicao"][0] - estado["pos_jogador"][0] > 0:
                            direcao = 3
                        else:
                            direcao = 4

                    #cima
                    if direcao == 1:
                        if (not obj["posicao"][1] == 0) and estado["mapa"][obj["posicao"][1]-1][obj["posicao"][0]] == ' ' and not obj["posicao"][1]-1 == estado["pos_jogador"][1]:

                            obj["posicao"][1] -= 1

                    #baixo
                    if direcao == 2:
                        if (not obj["posicao"][1] == len(estado["mapa"]) - 1) and estado["mapa"][obj["posicao"][1]+1][obj["posicao"][0]] == ' ' and not obj["posicao"][1]+1 == estado["pos_jogador"][1]:

                            obj["posicao"][1] += 1

                    #esquerda
                    if direcao == 3:
                        if (not obj["posicao"][0] == 0) and estado["mapa"][obj["posicao"][1]][obj["posicao"][0]-1] == ' ' and not obj["posicao"][0]-1 == estado["pos_jogador"][0]:
                            
                            obj["posicao"][0] -= 1

                    #direita
                    if direcao == 4:
                        if (not obj["posicao"][0] == len(estado["mapa"][0]) - 1) and estado["mapa"][obj["posicao"][1]][obj["posicao"][0]+1] == ' ' and not obj["posicao"][0]+1 == estado["pos_jogador"][0]:
                            
                            obj["posicao"][0] += 1
            

                else:
                    obj["pode_andar"] = True


        
def trocar_mapa(numero, entrada, estado):
    mapa = []
    with open(f"mapa{numero}.txt", "r", encoding="utf-8") as arquivo:
        texto = arquivo.read().split("\n")
        for linha in texto:
            eixo = []
            for caractere in linha:
                if caractere == "-":
                    eixo.append(" ")
                else:
                    eixo.append("▣")
            mapa.append(eixo)
        estado["mapa"] = mapa
    with open("objetos.txt", "r", encoding="utf-8") as arquivo:
        listas_de_objetos = [
            ast.literal_eval(linha.strip())
            for linha in arquivo
            if linha.strip()
            ]

    
    #salva de volta a posicao
    with open("objetos.txt", "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    linhas[estado["configs"]["tela"]-1] = str(estado["objetos"]) + "\n"
    with open("objetos.txt", "w", encoding="utf-8") as arquivo:
        arquivo.writelines(linhas)
    
    estado["objetos"] = listas_de_objetos[numero-1]
    estado["pos_jogador"] = entrada
    estado["configs"]["tela"] = numero
    if estado["configs"]["tela"] == 1 and estado["chaves"] == 3:
        estado["mapa"][0][7] = " "
        estado["mapa"][0][8] = " "
        estado["mapa"][0][9] = " "
        estado["mapa"][0][10] = " "