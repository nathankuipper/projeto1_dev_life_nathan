from constantes import *
import motor_grafico as motor


def desenha_tela(janela, estado, altura, largura):

    motor.preenche_fundo(janela, ROXO)

    titulo = 'COMO JOGAR'
    sublinhado = '===================='
    x_titulo = (largura - len(titulo)) // 2 - 10
    y_titulo = altura // 4

    motor.desenha_string(janela, x_titulo, y_titulo, titulo, ROXO, BRANCO)
    motor.desenha_string(janela, x_titulo, y_titulo + 1, sublinhado, ROXO, BRANCO)

    motor.desenha_string(janela, x_titulo-5, y_titulo + 10, "Use as setas para se locomover", ROXO, BRANCO)
    motor.desenha_string(janela, x_titulo-7, y_titulo + 12, "Aperte i para acessar o inventario", ROXO, BRANCO)
    motor.desenha_string(janela, x_titulo-7, y_titulo + 14, "Use espaço para equipar itens no inventário", ROXO, BRANCO)
    motor.desenha_string(janela, x_titulo-7, y_titulo + 16, "Aperte e para jogar fora itens no inventário", ROXO, BRANCO)
    motor.desenha_string(janela, x_titulo-7, y_titulo + 18, "Ande para cima de um monstro para atacá-lo", ROXO, BRANCO)

    motor.mostra_janela(janela)



def atualiza_estado(estado, tecla_apertada):

    if tecla_apertada == motor.ESPACO:
        estado["tela_atual"] = TELA_JOGO

    if tecla_apertada == 'i':
        estado['tela_atual'] = TELA_INICIO
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = TELA_INICIO