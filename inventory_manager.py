import util
import inventory_manager_ui


class InventoryMenu():
    def run(self, player, board):
        self.is_running = True
        self.selector = 8
        self.player_inventory = player.inventory
        while self.is_running:
            util.clear_screen()
            ui = inventory_manager_ui.InventoryView()
            ui.show_inventory(player, self.selector)
            key = util.key_pressed()
            if key == '\x1b':
                self.is_running = False
            elif key == 's':
                self.selector_down()
            elif key == 'w':
                self.selector_up()
            elif key == 'e':
                if player.inventory.inventory['backpack']:
                    item = player.inventory.inventory['backpack'].pop(self.selector - 8)
                    player.inventory.equip_item(item)
            elif key == 'd':
                if player.inventory.inventory['backpack']:
                    item = player.inventory.inventory['backpack'].pop(self.selector - 8)
                    board[player.x][player.y].inventory.inventory.append(item)

    def selector_up(self):
        if self.selector > 8:
            self.selector -= 1

    def selector_down(self):
        if self.selector < 7 + len(self.player_inventory.inventory['backpack']):
            self.selector += 1
