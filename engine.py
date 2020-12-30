import entities
import world
import util
import ui
import player_development
import stats
import inventory_manager
import inventory

PLAYER_ICON = '@'
PLAYER_START_X = 2
PLAYER_START_Y = 5


class Game():
    developer_mode = False

    def __init__(self, player):
        self.is_running = False
        self.levels = []
        self.used_npc = []
        if player is None:
            self.player = entities.Player(x=PLAYER_START_X, y=PLAYER_START_Y, image_map=[[0, 0, PLAYER_ICON]])
            util.clear_screen()
            start = player_development.PlayerDeveloper()

            self.player.stats = start.run(self.player, first_time=True)
            self.player.advancement['rank'] = 1
            self.player.advancement['experience'] = 0
        else:
            self.player = player
        self.current_level = None
        self.game_messages = []

    def add_level(self):
        self.levels.append(world.Level(self, self.player, rank=len(self.levels)))

        if len(self.levels) == 1:
            self.levels[-1].interactables.pop(1)

        for element in self.levels[-1].interactables:
            element.put_entity_on_board(self.levels[-1].board)

        for element in self.levels[-1].enemies:
            element.put_entity_on_board(self.levels[-1].board)

        for element in self.levels[-1].npcs:
            element.put_entity_on_board(self.levels[-1].board)
            self.used_npc.append(element.name)

    def run(self):

        self.is_running = True
        self.add_level()
        self.current_level = self.levels[0]
        self.player.put_entity_on_board(self.current_level.board)
        self.update_icons()
        self.commands = {"w": [self.player.move_attempt, (self.current_level.board, -1, 0)],
                         "s": [self.player.move_attempt, (self.current_level.board, 1, 0)],
                         "a": [self.player.move_attempt, (self.current_level.board, 0, -1)],
                         "d": [self.player.move_attempt, (self.current_level.board, 0, 1)],
                         "t": [self.player.change, ()],
                         "p": [self.developer_mode_switch, ()],
                         "P": [self.exp_cheat, ()],
                         "S": [self.show_stats, ()],
                         "r": [self.player.pick_one_item, [self.current_level.board]],
                         "I": [self.show_inventory, ()]
                         }

        while self.is_running:
            util.clear_screen()
            ui.display_status(self, self.player, self.current_level.enemies, self.developer_mode)
            ui.display_board(self.current_level.board, self.player, self.developer_mode)
            ui.display_messages(self.game_messages)

            key = util.key_pressed()

            if key == 'q':
                self.player.stats.status['hp']['current'] = -100

            elif key in self.commands:
                self.commands[key][0](*self.commands[key][1])

            self.update()

        return self.player

    def update(self):
        self.clear_dead_enemies()
        self.move_enemies()
        self.move_npcs()
        self.player_update()
        self.message_collector()
        self.update_icons()

    def clear_dead_enemies(self):
        i = 0
        while i < len(self.current_level.enemies):
            element = self.current_level.enemies[i]
            if element.stats.status['hp']['current'] <= 0:
                self.player.advancement['experience'] += self.calculate_exp_gain(element)
                self.destroy_enemy(element)
            else:
                i += 1

    def calculate_exp_gain(self, enemy):
        attack = enemy.stats.attributes['attack']['base']
        defense = enemy.stats.attributes['defense']['base']
        damage = enemy.stats.attributes['damage']['base']
        armor = enemy.stats.attributes['armor']['base']
        hp = enemy.stats.status['hp']['max_base']
        exp = ((attack + defense + hp + (15*armor) + (5*damage))/10)
        if enemy.diagonal_movement:
            exp *= 1.1
        if enemy.speed > 1:
            exp *= 1.1
        exp = int(round(exp))
        return exp

    def destroy_enemy(self, enemy):
        for part in enemy.image_map:
            x = enemy.x + part[entities.IMAGE_MAP_DX]
            y = enemy.y + part[entities.IMAGE_MAP_DY]
            self.current_level.board[x][y].entity = None
        self.current_level.enemies.remove(enemy)

    def move_enemies(self):
        for enemy in self.current_level.enemies:
            enemy.path(self.current_level.board,
                       self.player)

    def move_npcs(self):
        for npc in self.current_level.npcs:
            npc.path(self.current_level.board)

    def add_game_message(self, message):
        self.game_messages.append(message)

    def player_update(self):
        self.reset_player_attributes()
        self.update_temp_bonuses()
        self.calculate_current_attributes()
        self.check_if_alive()

    def reset_player_attributes(self):
        for element in self.player.stats.attributes:
            base_value = self.player.stats.attributes[element]['base']
            self.player.stats.attributes[element]['current'] = base_value

    def calculate_current_attributes(self):
        # Temporary attribute bonuses:
        for element in self.player.stats.temp_attr_bunus:
            new_value = self.player.stats.attributes[element[entities.ATTRIBUTE]]['base'] + element[entities.DELTA]
            self.player.stats.attributes[element[entities.ATTRIBUTE]]['current'] = new_value

        # Item attribute bonuses:
        for key in self.player.inventory.inventory:
            if key != 'backpack' and key != 'belt':
                item = self.player.inventory.inventory[key]
                if item:
                    for bonus in item.bonus:
                        attribute = bonus[0]
                        delta = bonus[1]
                        self.player.stats.attributes[attribute]['current'] += delta

    def update_temp_bonuses(self):
        i = 0
        while i < len(self.player.stats.temp_attr_bunus):
            if self.player.stats.temp_attr_bunus[i][entities.TIME] <= 0:
                self.player.stats.temp_attr_bunus.pop(i)
            else:
                self.player.stats.temp_attr_bunus[i][entities.TIME] -= 1
                i += 1

    def check_if_alive(self):
        if self.player.stats.status['hp']['current'] <= 0:
            self.is_running = False
            util.clear_screen()
            develop = player_development.PlayerDeveloper()
            self.player.stats = develop.run(self.player)
            self.player.x = PLAYER_START_X
            self.player.y = PLAYER_START_Y
            self.player.inventory = inventory.Player_Inventory()

    def update_icons(self):
        self.player.color_icon()
        for enemy in self.current_level.enemies:
            enemy.color_icon()

    def message_collector(self):
        self.message_iterator(self.player.message_stack)

        for enemy in self.current_level.enemies:
            self.message_iterator(enemy.message_stack)

        for interactable in self.current_level.interactables:
            self.message_iterator(interactable.message_stack)

    def message_iterator(self, msg_list):
        for msg in msg_list:
            self.add_game_message(msg)
        msg_list.clear()

    def developer_mode_switch(self):
        self.developer_mode = not self.developer_mode

    def exp_cheat(self):
        self.player.advancement['experience'] += 5000

    def show_stats(self):
        player_stats = stats.StatsMenu()
        player_stats.run(self.player)

    def show_inventory(self):
        player_inventory = inventory_manager.InventoryMenu()
        player_inventory.run(self.player, self.current_level.board)
