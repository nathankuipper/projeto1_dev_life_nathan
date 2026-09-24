from constantes import *
import motor_grafico as motor


def desenha_tela(janela, estado, altura, largura):
    # Você pode usar esta função como base para a sua função desenha_tela do arquivo tela_jogo.py
    # Esta tela é mostrada quando o jogador aperta a tecla 'i' (você provavelmente vai querer 
    # alterar este arquivo no nível avançado)
    motor.preenche_fundo(janela, BRANCO)

    motor.desenha_string(janela, 1, 1, 'INVENTARIO', BRANCO, PRETO)
    motor.desenha_string(janela, 1, 2, '----------', BRANCO, PRETO)

    #itens
    motor.desenha_string(janela, 5, 9, 'ITENS', BRANCO, PRETO)
    motor.desenha_string(janela, 5, 10, '----------', BRANCO, PRETO)
    motor.desenha_string(janela, 5, 12, f"Poção de cura: {estado["itens"]["cura"]}", BRANCO, PRETO)
    motor.desenha_string(janela, 5, 14, f"Poção aumentar vida: {estado["itens"]["vida_max"]}", BRANCO, PRETO)
    motor.desenha_string(janela, 5, 16, f"Espada: {estado["itens"]["espada"]}", BRANCO, PRETO)
    motor.desenha_string(janela, 5, 18, f"Óculos: {estado["itens"]["oculos"]}", BRANCO, PRETO)

    #desenhar a seta selecionada
    motor.desenha_string(janela, 2, estado["configs"]["selecionado"]*2 + 10, ">>>", BRANCO, PRETO)

    #desenhar o equipamento
    motor.desenha_string(janela, 50, 9, 'EQUIPAMENTO', BRANCO, PRETO)
    motor.desenha_string(janela, 50, 10, '----------', BRANCO, PRETO)
    motor.desenha_string(janela, 50, 14, f"|{estado["equipamento"]}|", BRANCO, PRETO)

    #mensagem
    motor.desenha_string(janela, 1, 25, estado["configs"]["mensagem"], BRANCO, PRETO)

    #peso
    motor.desenha_string(janela, 50, 25, f'CAPACIDADE: {estado["configs"]["peso"]}/{estado["configs"]["maximo"]}', BRANCO, PRETO)
    for i in range(estado["configs"]["peso"]):
        motor.desenha_string(janela, 50+i, 26, '|', BRANCO, PRETO)

    motor.mostra_janela(janela)



def atualiza_estado(estado, tecla_apertada):
    mensagens = ["Restaura dois pontos de vida", "Aumenta em um sua vida máxima", "Aumenta seu dano", "Te proteje caso você morra"]

    peso = 0
    for i in estado["itens"].values():
        peso += i
    estado["configs"]["peso"] = peso
        

    #selecionar item
    if tecla_apertada == motor.SETA_BAIXO:
        estado["configs"]["selecionado"] += 1
        if estado["configs"]["selecionado"] == 5:
            estado["configs"]["selecionado"] = 1

    if tecla_apertada == motor.SETA_CIMA:
            estado["configs"]["selecionado"] -= 1
            if estado["configs"]["selecionado"] == 0:
                estado["configs"]["selecionado"] = 4

    if tecla_apertada == motor.ESPACO:
        if estado["configs"]["selecionado"] == 1 and estado["itens"]["cura"] > 0:
            estado["itens"]["cura"] -= 1
            if not estado["vidas"] > estado["max_vidas"] - 2:
                estado["vidas"] += 2
            else:
                estado["vidas"] = estado["max_vidas"]

        if estado["configs"]["selecionado"] == 2 and estado["itens"]["vida_max"] > 0:
            estado["itens"]["vida_max"] -= 1
            estado["max_vidas"] += 1

        if estado["configs"]["selecionado"] == 3 and estado["itens"]["espada"] > 0:
            estado["itens"]["espada"] -= 1
            if estado["equipamento"] == "Espada":
                estado["itens"]["espada"] += 1

            if estado["equipamento"] == "Óculos":
                estado["itens"]["oculos"] += 1

            estado["equipamento"] = "Espada"

        if estado["configs"]["selecionado"] == 4 and estado["itens"]["oculos"] > 0:
            estado["itens"]["oculos"] -= 1
            if estado["equipamento"] == "Espada":
                estado["itens"]["espada"] += 1

            if estado["equipamento"] == "Óculos":
                estado["itens"]["oculos"] += 1
                
            estado["equipamento"] = "Óculos"

    if tecla_apertada == "e":
        if estado["configs"]["selecionado"] == 1 and estado["itens"]["cura"] > 0:
            estado["itens"]["cura"] -= 1

        if estado["configs"]["selecionado"] == 2 and estado["itens"]["vida_max"] > 0:
            estado["itens"]["vida_max"] -= 1

        if estado["configs"]["selecionado"] == 3 and estado["itens"]["espada"] > 0:
            estado["itens"]["espada"] -= 1

        if estado["configs"]["selecionado"] == 4 and estado["itens"]["oculos"] > 0:
            estado["itens"]["oculos"] -= 1
    
        
    peso = 0
    for i in estado["itens"].values():
        peso += i
    estado["configs"]["peso"] = peso

    estado["configs"]["mensagem"] = mensagens[estado["configs"]["selecionado"]-1]


    if tecla_apertada == 'i':
        estado['tela_atual'] = TELA_JOGO
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR