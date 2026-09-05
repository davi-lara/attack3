import sys
import os

# Oculta a mensagem de boas-vindas do pygame no terminal
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from pynput.keyboard import Controller, Key

# Inicializa o controlador de teclado virtual
keyboard = Controller()

# Inicializa o Pygame e o sistema de Joystick
pygame.init()
pygame.joystick.init()

# Verifica se há algum controle conectado
if pygame.joystick.get_count() == 0:
    print("Nenhum joystick Logitech J-UJ18 detectado!")
    print("Por favor, conecte o dispositivo e tente novamente.")
    sys.exit()

# Conecta ao primeiro joystick disponível
joy = pygame.joystick.Joystick(0)
joy.init()
print(f"Dispositivo conectado: {joy.get_name()}")
print("Mapeamento ativo. Pressione CTRL+C no terminal para fechar.")

# -------------------------------------------------------------
# DICIONÁRIO DE MAPEAMENTO (Configure suas teclas aqui!)
# -------------------------------------------------------------
# Mapeamento para os botões físicos (Botão ID: Tecla do Teclado)
# O Attack 3 possui os botões de 0 a 10 no Pygame (Gatilho costuma ser o 0)
MAPEAMENTO_BOTOES = {
    0: Key.space,  # Gatilho (Botão 1 no plástico) -> Barra de Espaço
    1: Key.enter,  # Botão traseiro/topo -> Enter
    2: "a",  # Botão do topo -> Letra 'A'
    3: "b",  # Botão do topo -> Letra 'B'
    4: "c",  # Botão do topo -> Letra 'C'
    # Adicione os botões da base (5 a 10) conforme sua necessidade:
    # 5: 'x',
    # 6: 'y',
}

# Estados para controle de repetição (evita disparar múltiplos cliques por frame)
botoes_pressionados = {}
eixo_x_pressionado = None
eixo_y_pressionado = None

# Zona morta para os eixos (ignora pequenos movimentos involuntários no centro)
ZONA_MORTA = 0.3

try:
    relogio = pygame.time.Clock()
    executando = True

    while executando:
        # Captura os eventos do sistema
        pygame.event.pump()
# --- CONTROLE DE SENSIBILIDADE (ALAVANCA DO SEU DEDO) ---
        valor_throttle = joy.get_axis(2)  # Lê a alavanca (Eixo 2)
        fator_ajuste = ((valor_throttle * -1) + 1) / 2
        multiplicador_sensibilidade = 0.2 + (fator_ajuste * 1.8)
        # --------------------------------------------------------
        # -------------------------------------------------------------
        # 1. PROCESSAMENTO DOS EIXOS (Analógico - Movimento do Manche)
        # -------------------------------------------------------------
        # Eixo 0 = Esquerda / Direita
        valor_x = joy.get_axis(0) * multiplicador_sensibilidade
        # Eixo 1 = Frente / Trás
        valor_y = joy.get_axis(1) * multiplicador_sensibilidade

        # Processa Eixo X (Esquerda / Direita) -> Mapeado para Setas
        if valor_x < -ZONA_MORTA:
            if eixo_x_pressionado != Key.left:
                if eixo_x_pressionado:
                    keyboard.release(eixo_x_pressionado)
                keyboard.press(Key.left)
                eixo_x_pressionado = Key.left
        elif valor_x > ZONA_MORTA:
            if eixo_x_pressionado != Key.right:
                if eixo_x_pressionado:
                    keyboard.release(eixo_x_pressionado)
                keyboard.press(Key.right)
                eixo_x_pressionado = Key.right
        else:
            if eixo_x_pressionado:
                keyboard.release(eixo_x_pressionado)
                eixo_x_pressionado = None

        # Processa Eixo Y (Frente / Trás) -> Mapeado para Setas
        if valor_y < -ZONA_MORTA:  # No joystick, empurrar para frente gera valor negativo
            if eixo_y_pressionado != Key.up:
                if eixo_y_pressionado:
                    keyboard.release(eixo_y_pressionado)
                keyboard.press(Key.up)
                eixo_y_pressionado = Key.up
        elif valor_y > ZONA_MORTA:  # Puxar para trás gera valor positivo
            if eixo_y_pressionado != Key.down:
                if eixo_y_pressionado:
                    keyboard.release(eixo_y_pressionado)
                keyboard.press(Key.down)
                eixo_y_pressionado = Key.down
        else:
            if eixo_y_pressionado:
                keyboard.release(eixo_y_pressionado)
                eixo_y_pressionado = None

        # -------------------------------------------------------------
        # 2. PROCESSAMENTO DOS BOTÕES
        # -------------------------------------------------------------
        num_botoes = joy.get_numbuttons()
        for i in range(num_botoes):
            estado_botao = joy.get_button(i)

            # Se o botão está configurado no nosso dicionário
            if i in MAPEAMENTO_BOTOES:
                tecla = MAPEAMENTO_BOTOES[i]

                # Se acabou de ser pressionado
                if estado_botao and not botoes_pressionados.get(i, False):
                    keyboard.press(tecla)
                    botoes_pressionados[i] = True

                # Se acabou de ser solto
                elif not estado_botao and botoes_pressionados.get(i, False):
                    keyboard.release(tecla)
                    botoes_pressionados[i] = False

        # Limita o loop a 60 verificações por segundo (reduz uso de CPU)
        relogio.tick(60)
# --- PROCESSAMENTO DOS EIXOS (DIAGONAIS) ---
        eixo_horizontal = joystick.get_axis(0)
        eixo_vertical = joystick.get_axis(1)

        ZONA_MORTA = 0.3

        # Lógica Vertical (Frente / Trás)
        if eixo_vertical < -ZONA_MORTA:
            keyboard.press('w')
            keyboard.release('s')
        elif eixo_vertical > ZONA_MORTA:
            keyboard.press('s')
            keyboard.release('w')
        else:
            keyboard.release('w')
            keyboard.release('s')

        # Lógica Horizontal (Esquerda / Direita)
        if eixo_horizontal < -ZONA_MORTA:
            keyboard.press('a')
            keyboard.release('d')
        elif eixo_horizontal > ZONA_MORTA:
            keyboard.press('d')
            keyboard.release('a')
        else:
            keyboard.release('a')
            keyboard.release('d')

except KeyboardInterrupt:
    print("\nPrograma finalizado pelo usuário.")
finally:
    # Garante que nenhuma tecla fique travada no computador ao fechar
    keyboard.release('w')
    keyboard.release('s')
    keyboard.release('a')
    keyboard.release('d')
    for i, pressionado in botoes_pressionados.items():
        if pressionado and i in MAPEAMENTO_BOTOES:
            keyboard.release(MAPEAMENTO_BOTOES[i])
            
    pygame.quit()
