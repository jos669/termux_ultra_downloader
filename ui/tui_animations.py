import os
import random
import shutil
import sys
import time


def get_terminal_size():
    """Obtiene el tamaño de la terminal."""
    try:
        return shutil.get_terminal_size()
    except OSError:
        return (80, 24)


def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def move_cursor(x, y):
    """Mueve el cursor a una posición específica (x, y)."""
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()


def slide_in(text_block, direction="top", duration=0.5):
    """Anima un bloque de texto deslizándose desde una dirección."""
    lines = text_block.strip().split("\n")
    width, height = get_terminal_size()
    max_text_width = max(len(line) for line in lines) if lines else 0
    start_x = (width - max_text_width) // 2

    num_steps = height if direction in ["top", "bottom"] else width
    delay = duration / num_steps

    for i in range(num_steps + 1):
        clear_screen()
        if direction == "top":
            start_y = i - len(lines)
            if start_y > height // 2 - len(lines) // 2:
                break
        elif direction == "bottom":
            start_y = height - i
            if start_y < height // 2 - len(lines) // 2:
                break

        for j, line in enumerate(lines):
            y_pos = start_y + j
            if 0 < y_pos <= height:
                move_cursor(start_x, y_pos)
                sys.stdout.write(line)

        time.sleep(delay)


def reveal_lines(text_block, delay=0.05):
    """Anima un bloque de texto revelándose línea por línea."""
    lines = text_block.strip().split("\n")
    width, height = get_terminal_size()
    max_text_width = max(len(line) for line in lines) if lines else 0
    start_x = (width - max_text_width) // 2
    start_y = (height - len(lines)) // 2

    clear_screen()
    for i, line in enumerate(lines):
        move_cursor(start_x, start_y + i)
        sys.stdout.write(line)
        sys.stdout.flush()
        time.sleep(delay)


def fade_in_chars(text_block, duration=1.0):
    """Anima un bloque de texto apareciendo caracter por caracter de forma aleatoria."""
    lines = text_block.strip().split("\n")
    width, height = get_terminal_size()
    max_text_width = max(len(line) for line in lines) if lines else 0
    start_x = (width - max_text_width) // 2
    start_y = (height - len(lines)) // 2

    clear_screen()

    # Crear una lista de todas las posiciones de caracteres
    char_positions = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != " ":
                char_positions.append((start_x + j, start_y + i, char))

    random.shuffle(char_positions)
    delay = duration / len(char_positions)

    for x, y, char in char_positions:
        move_cursor(x, y)
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def play_intro_animation(header_text, logo_text=""):
    """
    Selecciona y ejecuta una animación de introducción aleatoria.
    """
    animations = [
        lambda: slide_in(f"{header_text}\n\n{logo_text}", direction="top"),
        lambda: reveal_lines(f"{header_text}\n\n{logo_text}"),
        lambda: fade_in_chars(f"{header_text}\n\n{logo_text}"),
    ]

    # Elegir y ejecutar una animación al azar
    chosen_animation = random.choice(animations)
    chosen_animation()


def animate_prompt(prompt_text):
    """Anima la aparición del prompt de input."""
    for char in prompt_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
