import pyfiglet
from colored import fg, attr

GREEN = fg('green')
RED = fg('red')
RES = attr('reset')


class MenuController():
    def display_screen(self, data):
        game_title = pyfiglet.figlet_format("ROGUELIKE")
        print(f'{RED}{game_title}{RES}')
        print(f'{GREEN}      1. Run game')
        print(f'      2. Show help')
        print(f'      3. Quit\n')
        print(f"Press 'w' and 's' to navigate up and down, press 'enter' to select")
        print(f"\033[{data.selector};0H", end='')
        print(f'---->')
