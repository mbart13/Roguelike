from colored import fg, attr

# Colors
RES = attr('reset')
GREEN = fg('green')
RED = fg('red')


class InventoryView():
    def show_inventory(self, player, selector):
        for key in player.inventory.inventory:
            if key != 'backpack':
                if player.inventory.inventory[key]:
                    print(f'{GREEN}{key}: {player.inventory.inventory[key].name}')
                else:
                    print(f'{GREEN}{key}: No item')
        
        print('\nBackpack: ')

        for item in player.inventory.inventory['backpack']:
            print(f'    {item.name}')

        print('\nPress e to equip selected item')
        print('Press d to drop selected item')
        print('Press ESC to go back to game')
        print(f"\033[{selector};0H", end='')
        print(f'--->')