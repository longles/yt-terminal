# ANSI codes
END_CODE = '\033[0;0m'
REFRESH_CODE = '\033[f'
RESET_CODE = '\033c'


"""
Move the cursor to the x,y position in the terminal
"""
def move_cursor(x, y) -> str:
    return f'\033[{x};{y}H'


"""
Returns an ANSI sequence to set the character color.
"""
def fg_code(rgb: tuple) -> str:
    return f'\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m'


"""
Returns an ANSI sequence to set the background color.
"""
def bg_code(rgb: tuple) -> str:
    return f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m'


"""
Turns text rainbow colored.
"""
def rainbow(text: str) -> str:
    rainbow = [
        (148, 0, 211), (75, 0, 130), (0, 0, 255),
        (0, 255, 0), (255, 255, 0), (255, 127, 0),
        (255, 0 , 0)
    ]

    return ''.join(f'{fg_code(rainbow[i % len(rainbow)])}{text[i]}{END_CODE}' for i in range(len(text)))
