from constantes import *
import motor_grafico as motor


def desenha_tela(janela, estado, altura, largura):

    motor.preenche_fundo(janela, AZUL)

    titulo = '😎 EMOTES AND DUNGEONS 😭'
    sublinhado = '===================='
    x_titulo = (largura - len(titulo)) // 2
    y_titulo = altura // 4

    motor.desenha_string(janela, x_titulo, y_titulo, titulo, AZUL, BRANCO)
    motor.desenha_string(janela, x_titulo, y_titulo + 1, sublinhado, AZUL, BRANCO)

    motor.desenha_string(janela, x_titulo-5, y_titulo + 10, "Precione ESPAÇO para iniciar", AZUL, BRANCO)
    motor.desenha_string(janela, x_titulo-7, y_titulo + 12, "Precione I para ver as instruções", AZUL, BRANCO)

    motor.mostra_janela(janela)



def atualiza_estado(estado, tecla_apertada):

    if tecla_apertada == motor.ESPACO:
        estado["tela_atual"] = TELA_JOGO

    if tecla_apertada == 'i':
        estado['tela_atual'] = TELA_INSTRUCOES
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR