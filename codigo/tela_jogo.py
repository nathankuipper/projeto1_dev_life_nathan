from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto


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
            motor.desenha_string(janela, inicio_x + h, inicio_y + v, ' ', VERDE_ESCURO, BRANCO)

    #desenha os objetos
    for obj in estado["objetos"]:
        motor.desenha_string(janela, obj["posicao"][0] + inicio_x, obj["posicao"][1] + inicio_y, obj["tipo"], VERDE_ESCURO, obj["cor"])

    #desenha o jogador
    motor.desenha_string(janela, estado["pos_jogador"][0] + inicio_x, estado["pos_jogador"][1] + inicio_y , '@', VERDE_ESCURO, AZUL)

    #desenha as vidas
    motor.desenha_string(janela, inicio_x, inicio_y - 2, str(estado["vidas"]), PRETO, VERMELHO)

    #desenha a mensagem
    motor.desenha_string(janela, inicio_x, inicio_y + altura_mapa + 2, estado["mensagem"], PRETO, BRANCO)



    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla):
    # O seu código deve atualizar o dicionário "estado" com base na tecla apertada pelo jogador
    # Por exemplo, se o jogador apertar a seta para a esquerda (o valor da variável será "ESQUERDA"), 
    # o seu código deve atualizar o dicionário estado['pos_jogador'][0] -= 1

    # Mude o valor da chave 'tela_atual' para mudar de tela
    
    # Começamos apagando a mensagem anterior, pois ela já foi mostrada no frame anterior
    estado['mensagem'] = ''

    # Escreva seu código para atualizar o dicionário "estado" com base na tecla apertada pelo jogador aqui
    # APAGUE ESTA LINHA E ESCREVA SEU CÓDIGO AQUI

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR