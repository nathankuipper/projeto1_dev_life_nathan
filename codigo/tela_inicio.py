from constantes import *
import motor_grafico as motor


def desenha_tela(janela, estado, altura, largura):

    motor.preenche_fundo(janela, BRANCO)

    motor.desenha_string(janela, 1, 1, '', BRANCO, PRETO)
    motor.desenha_string(janela, 1, 2, '----------', BRANCO, PRETO)

    motor.mostra_janela(janela)



def atualiza_estado(estado, tecla_apertada):


    if tecla_apertada == 'i':
        estado['tela_atual'] = TELA_JOGO
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR