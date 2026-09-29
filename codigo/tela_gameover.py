from constantes import *
import motor_grafico as motor
import inicializacao


def desenha_tela(janela, estado, altura, largura):

    motor.preenche_fundo(janela, VERMELHO)

    titulo = '!!!VOCÊ MORREU!!!'
    sublinhado = '===================='
    x_titulo = (largura - len(titulo)) // 2
    y_titulo = altura // 4

    motor.desenha_string(janela, x_titulo, y_titulo, titulo, VERMELHO, BRANCO)
    motor.desenha_string(janela, x_titulo, y_titulo + 1, sublinhado, VERMELHO, BRANCO)

    motor.desenha_string(janela, x_titulo-5, y_titulo + 10, "MAIS SORTE NA PRÓXIMA VEZ", VERMELHO, BRANCO)
    motor.desenha_string(janela, x_titulo-7, y_titulo + 12, "Precione ESPAÇO para vencerrar o jogo", VERMELHO, BRANCO)

    motor.mostra_janela(janela)



def atualiza_estado(estado, tecla_apertada):

    if tecla_apertada == motor.ESPACO:
        inicializacao.inicializa_estado()
        estado["tela_atual"] = SAIR

    if tecla_apertada == 'i':
        estado['tela_atual'] = TELA_INSTRUCOES
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR