import random

from utils.colors import Colors

INPUT_STYLES = [
    # 1. Minimal Arrow
    f"{Colors.CYAN}└──> {Colors.WHITE}Acción:# {Colors.RESET}",
    # 2. Hacker Prompt
    f"{Colors.CYAN}root@urlvideo<~># {Colors.WHITE}execute: {Colors.RESET}",
    # 3. Double Arrow
    f"{Colors.CYAN}»» {Colors.WHITE}Input: {Colors.RESET}",
    # 4. Square Brackets
    f"{Colors.CYAN}[{Colors.WHITE} CMD {Colors.CYAN}]─> {Colors.RESET}",
    # 5. Curly Braces
    "{Colors.CYAN}{{{Colors.WHITE}} prompt {Colors.CYAN}}}◈ {Colors.RESET}",
    # 6. Glitch Style
    f"{Colors.CYAN}▓▒░{Colors.WHITE} C:/_> {Colors.RESET}",
    # 7. Portal
    f"{Colors.CYAN}⟐⟐⟐ {Colors.WHITE}INPUT {Colors.CYAN}⟐⟐⟐\n{Colors.WHITE}>> {Colors.RESET}",
    # 8. Simple Line
    f"{Colors.CYAN}═══════════════════════════════════\n{Colors.WHITE} ► {Colors.RESET}",
    # 9. Tech Box
    f"{Colors.CYAN}╭─{Colors.WHITE} orden {Colors.CYAN}─╮\n╰─> {Colors.RESET}",
    # 10. Diamond
    f"{Colors.CYAN}◇◆◇ {Colors.WHITE}Select Option: {Colors.RESET}",
    # 11. Cyberpunk
    f"{Colors.CYAN}<< {Colors.WHITE}RUN: {Colors.RESET}",
    # 12. Brackets and Colon
    f"{Colors.CYAN}[{Colors.WHITE}*{Colors.CYAN}] : {Colors.RESET}",
    # 13. Double Line
    f"{Colors.CYAN}═══════>> {Colors.WHITE}OPCIÓN{Colors.RESET}",
    # 14. Underlined
    f"{Colors.WHITE}Comando\n{Colors.CYAN}-------{Colors.WHITE}> {Colors.RESET}",
    # 15. Dots
    f"{Colors.CYAN}... {Colors.WHITE}acción: {Colors.RESET}",
    # 16. Parentheses
    f"{Colors.CYAN}({Colors.WHITE}input{Colors.CYAN})> {Colors.RESET}",
    # 17. Angle Brackets
    f"{Colors.CYAN}< {Colors.WHITE}cmd{Colors.CYAN} > {Colors.RESET}",
    # 18. Vertical Line
    f"{Colors.CYAN}| {Colors.WHITE}op: {Colors.RESET}",
    # 19. Hash
    f"{Colors.CYAN}# {Colors.WHITE}_ {Colors.RESET}",
    # 20. Simple Prompt
    f"{Colors.CYAN}> {Colors.RESET}",
]

# Paletas de colores para asegurar variedad y consistencia
COLOR_PALETTES = [
    {"color_1": Colors.CYAN, "color_2": Colors.WHITE},
    {"color_1": Colors.MAGENTA, "color_2": Colors.WHITE},
    {"color_1": Colors.GREEN, "color_2": Colors.WHITE},
    {"color_1": Colors.YELLOW, "color_2": Colors.WHITE},
    {"color_1": Colors.BLUE, "color_2": Colors.WHITE},
    {"color_1": Colors.RED, "color_2": Colors.YELLOW},
]


def get_random_input_style():
    """
    Selecciona un estilo de input y una paleta de colores al azar,
    y devuelve el string formateado.
    """
    style_template = random.choice(INPUT_STYLES)
    palette = random.choice(COLOR_PALETTES)

    # Formatear el template con la paleta de colores y el reset
    return style_template.format(
        color_1=palette["color_1"], color_2=palette["color_2"], reset=Colors.RESET
    )
