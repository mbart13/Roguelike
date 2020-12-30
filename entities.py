import random
import math
import util
from util import dice
from world import BOARD_HEIGHT
from world import BOARD_WIDTH
from colored import fg, attr
import inventory
import item_creator

# Colors
RES = attr('reset')
GREEN = fg('green')
YELLOW = fg('yellow_1')
ORANGE = fg('orange_red_1')
BLUE = fg('blue')
RED = fg('red')
PURPLE = fg('deep_pink_4b')
ORANGE = fg('dark_orange')

# New player stats
P_HP = 20
P_DMG = 2
P_ARM = 0
P_ATT = 60
P_DEF = 30
P_PER = 5
P_CHA = 3

# Image map
IMAGE_MAP_DX = 0
IMAGE_MAP_DY = 1
IMAGE = 2

# Stats set
HP = 0
DAMAGE = 1
ARMOR = 2
ATTACK = 3
DEFENSE = 4
PERCEPTION = 5
CHARISMA = 6

# Temp Attr Bonus
ATTRIBUTE = 0
DELTA = 1
TIME = 2

# NPC interactions
FUNCTION = 0
ARGUMENT = 1
MESSAGE = 2


class Entity:

    message_stack = []

    def __init__(self,
                 x=random.randint(1, BOARD_HEIGHT-1),
                 y=random.randint(1, BOARD_WIDTH-1),
                 image_map=[[0, 0, 'P']],
                 description="PLACEHOLDER_This doesn't look like anything to me.",
                 colour=None
                 ):

        self.x = x
        self.y = y
        self.image_map = image_map
        self.description = description
        self.colour = colour

    def put_entity_on_board(self, board):
        self.find_free_space(board)

        for element in self.image_map:
            board[self.x + element[IMAGE_MAP_DX]][self.y + element[IMAGE_MAP_DY]].entity = self

    def find_free_space(self, board):
        is_place_free = False
        while self.check_space_if_free(board, self.x, self.y) is False:
            if is_place_free is False:
                self.x = random.randint(0, BOARD_HEIGHT-1)
                self.y = random.randint(0, BOARD_WIDTH-1)

    def check_space_if_free(self, board, x, y):
        is_place_free = True
        for element in self.image_map:
            if (x + element[IMAGE_MAP_DX]) > (len(board) - 1) or (y + element[IMAGE_MAP_DY]) > (len(board[0]) - 1):
                is_place_free = False
            else:
                target = board[x + element[IMAGE_MAP_DX]][y + element[IMAGE_MAP_DY]]
                if (target.entity is not None and target.entity is not self) or target.surface_name == 'void':
                    is_place_free = False
        return is_place_free

    def image(self, x=None, y=None):
        image = '\u0494'
        if len(self.image_map) == 1:
            image = self.image_map[0][IMAGE]
        else:
            if x is None:
                x = self.x
            if y is None:
                y = self.y

            for element in self.image_map:
                if x == self.x + element[IMAGE_MAP_DX] and y == self.y + element[IMAGE_MAP_DY]:
                    image = element[IMAGE]

        if self.colour is not None:
            image = f"{self.colour}{image}{RES}"

        return image


class MovingEntity(Entity):
    def move_attempt(self, board, dx, dy):
        # Check for move possibility
        if self.check_space_if_free(board, self.x + dx, self.y + dy):
            self.move(board, dx, dy)

    def move(self, board, dx, dy):
        # Disappear from original location
        for element in self.image_map:
            board[self.x + element[IMAGE_MAP_DX]][self.y + element[IMAGE_MAP_DY]].entity = None

        # Update coordinates
        self.x += dx
        self.y += dy

        # Appear in target
        for element in self.image_map:
            board[self.x + element[IMAGE_MAP_DX]][self.y + element[IMAGE_MAP_DY]].entity = self

    def color_icon(self):
        current = self.stats.status["hp"]["current"]
        max_current = self.stats.status["hp"]["max_current"]
        q1 = 1/4 * max_current
        median = max_current / 2
        q3 = 3/4 * max_current

        if current > q3:
            color = GREEN
        elif current > median and current <= q3:
            color = YELLOW
        elif current > q1 and current <= median:
            color = ORANGE
        elif current <= q1:
            color = RED

        self.colour = color


class Player(MovingEntity):
    def __init__(self,
                 x,
                 y,
                 image_map,
                 stats_set=[P_HP, P_DMG, P_ARM, P_ATT, P_DEF, P_PER, P_CHA],
                 name="Jimmy",
                 inventory=inventory.Player_Inventory(),
                 description="This is the main hero.",
                 colour=None,
                 ):

        self.x = x
        self.y = y
        self.image_map = image_map
        self.colour = colour
        self.name = name
        self.inventory = inventory
        self.description = description
        hp = stats_set[HP]
        dmg = stats_set[DAMAGE]
        arm = stats_set[ARMOR]
        att = stats_set[ATTACK]
        dfs = stats_set[DEFENSE]
        per = stats_set[PERCEPTION]
        cha = stats_set[CHARISMA]
        self.stats = Stats(hp=hp, dmg=dmg, arm=arm, att=att, dfs=dfs, per=per, cha=cha)
        self.advancement = {'rank': 1,
                            'experience': 600}
        self.item_generator = item_creator.ItemCreator(0)

    def move_attempt(self, board, dx, dy):
        target = [board, self.x + dx, self.y + dy]
        target_entity = board[self.x + dx][self.y + dy].entity
        if self.check_space_if_free(*target):
            self.move(board, dx, dy)
        elif isinstance(target_entity, Interactable):
            target_entity.interact()
        elif isinstance(target_entity, Npc):
            charisma = self.stats.attributes['charisma']['current']
            target_entity.interact(charisma)
        elif isinstance(target_entity, Enemy):
            target_entity.strike(self.stats)

    def change(self):
        for element in self.image_map:
            if element[IMAGE] == "@":
                element[IMAGE] = "#"
            else:
                element[IMAGE] = "@"

    def find_distance(self, x, y):
        delta_x = abs(self.x - x)
        delta_y = abs(self.y - y)
        return math.sqrt(delta_x**2 + delta_y**2)

    def go_to_next_level(self, game):
        for element in self.image_map:
            game.current_level.board[self.x + element[IMAGE_MAP_DX]][self.y + element[IMAGE_MAP_DY]].entity = None

        if game.current_level.was_explored:
            rank_index = game.current_level.rank + 1
            game.current_level = game.levels[rank_index]
            message = f'You are back in level {game.current_level.rank + 1}'
            self.message_stack.append(message)
        else:
            game.current_level.was_explored = True
            self.advancement['experience'] += 100*len(game.levels)
            game.add_level()
            game.current_level = game.levels[-1]
            message = f'You are in level {game.current_level.rank + 1}'
            self.message_stack.append(message)

        for interactable in game.current_level.interactables:
            if interactable.description == 'Stairs leading to previous level':
                x = interactable.x
                y = interactable.y
        self.x = x
        self.y = y + 1
        game.player.put_entity_on_board(game.current_level.board)
        game.commands = {"w": [game.player.move_attempt, (game.current_level.board, -1, 0)],
                         "s": [game.player.move_attempt, (game.current_level.board, 1, 0)],
                         "a": [game.player.move_attempt, (game.current_level.board, 0, -1)],
                         "d": [game.player.move_attempt, (game.current_level.board, 0, 1)],
                         "t": [game.player.change, ()],
                         "p": [game.developer_mode_switch, ()],
                         "P": [game.exp_cheat, ()],
                         "S": [game.show_stats, ()],
                         "r": [game.player.pick_one_item, [game.current_level.board]],
                         "I": [game.show_inventory, ()]
                         }

    def go_to_previous_level(self, game):
        for element in self.image_map:
            game.current_level.board[self.x + element[IMAGE_MAP_DX]][self.y + element[IMAGE_MAP_DY]].entity = None
        rank_index = game.current_level.rank - 1
        game.current_level = game.levels[rank_index]
        message = f'You are back in level {game.current_level.rank + 1}'
        self.message_stack.append(message)

        for interactable in game.current_level.interactables:
            if interactable.description == 'Stairs leading to next level':
                x = interactable.x
                y = interactable.y
        self.x = x
        self.y = y - 1
        game.player.put_entity_on_board(game.current_level.board)
        game.commands = {"w": [game.player.move_attempt, (game.current_level.board, -1, 0)],
                         "s": [game.player.move_attempt, (game.current_level.board, 1, 0)],
                         "a": [game.player.move_attempt, (game.current_level.board, 0, -1)],
                         "d": [game.player.move_attempt, (game.current_level.board, 0, 1)],
                         "t": [game.player.change, ()],
                         "p": [game.developer_mode_switch, ()],
                         "P": [game.exp_cheat, ()],
                         "S": [game.show_stats, ()],
                         "r": [game.player.pick_one_item, [game.current_level.board]],
                         "I": [game.show_inventory, ()]
                         }

    def strike(self, attacker):
        attack_result = attacker.stats.attributes['attack']['current'] - dice(100)
        defense_result = self.stats.attributes['defense']['current'] - dice(100)
        fight_result = attack_result - defense_result
        if attack_result > 0 and fight_result > 0:
            self.deal_damage(attacker.stats, fight_result)
        else:
            self.message_stack.append(f'{attacker.name} missed.')

    def deal_damage(self, attacker_stats, fight_result):
        damage_done = attacker_stats.attributes['damage']['current'] - self.stats.attributes['armor']['current']
        if damage_done < 0:
            damage_done = 0

        damage_done += round((fight_result // 50) * 0.3 * damage_done)
        if damage_done < 1:
            damage_done = 1
        self.stats.change_stat('hp', -damage_done)
        self.message_stack.append(f'You are hit for {damage_done} damage.')

    def pick_one_item(self, board):
        if board[self.x][self.y].inventory.inventory:
            self.inventory.add_item_to_backpack(board[self.x][self.y].inventory.inventory[-1])
            self.message_stack.append(f'You picked up {board[self.x][self.y].inventory.inventory[-1].name}.')
            board[self.x][self.y].inventory.inventory.pop()

    def take_item(self):
        new_item = self.item_generator.generate_item_object()
        self.inventory.inventory['backpack'].append(new_item)
        self.message_stack.append(f'You picked up {new_item.name}')


class Stats():
    def __init__(self, hp=1, dmg=1, arm=1, att=1, dfs=1, per=1, cha=1):
        self.status = {"hp": {'max_base': hp,
                              'max_current': hp,
                              'current': hp,
                              'advances': 0
                              }}

        self.attributes = {'damage':  {'base': dmg,
                                       'current': dmg,
                                       'advances': 0},
                           'armor':   {'base': arm,
                                       'current': arm,
                                       'advances': 0},
                           'attack':  {'base': att,
                                       'current': att,
                                       'advances': 0},
                           'defense': {'base': dfs,
                                       'current': dfs,
                                       'advances': 0},
                           'perception': {'base': per,
                                          'current': per,
                                          'advances': 0},
                           'charisma': {'base': cha,
                                        'current': cha,
                                        'advances': 0},
                           }

        self.temp_attr_bunus = []

    def change_stat(self, stat, delta):
        self.status[stat]['current'] += delta
        self.trim_current_stat(stat)

    def change_base_attr(self, stat, delta):
        self.attributes[stat]['base'] += delta

    def change_stat_by_percent(self, stat, delta_percent):
        change = round(self.status[stat]['max_current'] * (delta_percent/100))
        self.change_stat(stat, change)

    def trim_current_stat(self, stat):
        if self.status[stat]['current'] > self.status[stat]['max_current']:
            self.status[stat]['current'] = self.status[stat]['max_current']

    def add_temp_attr_bonus(self, attribute, delta, time):
        self.temp_attr_bunus.append([attribute, delta, time])


class Interactable(Entity):
    def __init__(self,
                 x=random.randint(1, BOARD_HEIGHT-1),
                 y=random.randint(1, BOARD_WIDTH-1),
                 image_map=[[0, 0, 'P']],
                 name="PLACEHOLDER_Very weird thing, indeed",
                 description="Placeholder for missing description.",
                 inventory=None,
                 interaction_function=None,
                 interaction_argument=None,
                 charges=1,
                 use_cost=0,
                 colour=PURPLE):

        self.x = x
        self.y = y
        self.image_map = image_map
        self.name = name
        self.description = description
        self.inventory = inventory
        self.interaction_function = interaction_function
        self.interaction_argument = interaction_argument
        self.charges = charges
        self.use_cost = use_cost
        self.colour = colour

    def interact(self):
        if self.charges > 0 and self.interaction_function is not None:
            if self.interaction_argument != ['']:
                self.interaction_function(*self.interaction_argument)
            else:
                self.interaction_function()
            self.charges -= self.use_cost


class Enemy(MovingEntity):
    def __init__(self,
                 x=random.randint(1, BOARD_HEIGHT-1),
                 y=random.randint(1, BOARD_WIDTH-1),
                 image_map=[0, 0, '%'],
                 name="PLACEHOLDER_Unnamed monstrosity",
                 stats_set=[1000, 999, 999, 120, 120],
                 description="PLACEHOLDER_An undescribed monstrosity.",
                 agro_range=10,
                 diagonal_movement=False,
                 speed=1,
                 colour=None
                 ):

        self.x = x
        self.y = y
        self.image_map = image_map
        self.name = name
        self.description = description
        hp = stats_set[HP]
        dmg = stats_set[DAMAGE]
        arm = stats_set[ARMOR]
        att = stats_set[ATTACK]
        dfs = stats_set[DEFENSE]
        self.stats = Stats(hp=hp, dmg=dmg, arm=arm, att=att, dfs=dfs)
        self.available_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        if diagonal_movement:
            self.available_moves = [[1, 0], [-1, 0], [0, 1], [0, -1],
                                    [1, 1], [-1, -1], [1, -1], [-1, 1]]
        self.agro_range = agro_range
        self.diagonal_movement = diagonal_movement
        self.speed = speed
        self.colour = colour

    def strike(self, attacker_stats):
        attack_result = attacker_stats.attributes['attack']['current'] - dice(100)
        defense_result = self.stats.attributes['defense']['current'] - dice(100)
        fight_result = attack_result - defense_result
        if attack_result > 0 and fight_result > 0:
            self.deal_damage(attacker_stats, fight_result)
        else:
            self.message_stack.append(f'You tried to hit {self.name}, but missed.')

    def deal_damage(self, attacker_stats, fight_result):
        damage_done = attacker_stats.attributes['damage']['current'] - self.stats.attributes['armor']['current']
        if damage_done < 0:
            damage_done = 0
        damage_done += round((fight_result // 30) * 0.3 * damage_done)
        if damage_done < 1:
            damage_done = 1
        self.stats.change_stat('hp', -damage_done)

        self.message_stack.append(f'{self.name} is hit for {damage_done} damage.')
        if self.stats.status["hp"]["current"] <= 0:
            self.message_stack.append(f'{self.name} is dead.')

    def path(self, board, player):
        if player.find_distance(self.x, self.y) >= self.agro_range:
            direction = random.choice(self.available_moves)
            self.move_attempt(board, *direction)
        else:
            for i in range(self.speed):
                direction = self.find_move_to_player(player)
                self.move_attempt(board, *direction)

    def find_move_to_player(self, player):
        X = 0
        Y = 1
        direction = [0, 0]
        delta = [player.x - self.x, player.y - self.y]

        if abs(delta[X]) > abs(delta[Y]):
            direction[X] = util.signum(delta[X])
            if self.diagonal_movement:
                direction[Y] = util.signum(delta[Y])

        elif abs(delta[X]) < abs(delta[Y]):
            direction[Y] = util.signum(delta[Y])
            if self.diagonal_movement:
                direction[X] = util.signum(delta[X])

        else:
            if self.diagonal_movement:
                direction[X] = util.signum(delta[X])
                direction[Y] = util.signum(delta[Y])
            else:
                axis = random.randint(0, 1)
                direction[axis] = int(math.copysign(1, delta[axis]))

        return direction

    def move_attempt(self, board, dx, dy):
        target = [board, self.x + dx, self.y + dy]
        target_entity = board[self.x + dx][self.y + dy].entity

        if self.check_space_if_free(*target):
            self.move(board, dx, dy)
        elif isinstance(target_entity, Player):
            target_entity.strike(self)


class Npc(MovingEntity):
    available = True

    def __init__(self,
                 x=random.randint(1, BOARD_HEIGHT-1),
                 y=random.randint(1, BOARD_WIDTH-1),
                 image_map=[[0, 0, 'M']],
                 name="PLACEHOLDER_Mysterious Stranger (from Fallout?)",
                 description="He has long coat and scoped Magnum 44.",
                 interaction_function_positive=None,
                 interaction_argument_positive=None,
                 interaction_message_positive=None,
                 interaction_function_neutral=None,
                 interaction_argument_neutral=None,
                 interaction_message_neutral=None,
                 interaction_function_negative=None,
                 interaction_argument_negative=None,
                 interaction_message_negative=None,
                 threshold_neutral=1,
                 threshold_positive=2,
                 colour=ORANGE):

        self.x = x
        self.y = y
        self.image_map = image_map
        self.name = name
        self.description = description
        self.colour = colour
        self.interactions = {'positive': [interaction_function_positive,
                                          interaction_argument_positive,
                                          interaction_message_positive],
                             'neutral': [interaction_function_neutral,
                                         interaction_argument_neutral,
                                         interaction_argument_neutral],
                             'negative': [interaction_function_negative,
                                          interaction_argument_negative,
                                          interaction_message_negative],
                             }
        self.threshold_neutral = threshold_neutral
        self.threshold_positive = threshold_positive

    def interact(self, charisma):
        if self.available > 0:
            self.available = 0
            if charisma < self.threshold_neutral:
                if self.interactions['negative'][FUNCTION] is not None:
                    self.interactions['negative'][FUNCTION](*self.interactions['negative'][ARGUMENT])
                    self.message_stack.append(self.interactions['negative'][MESSAGE])
            elif charisma < self.threshold_positive:
                if self.interactions['neutral'][FUNCTION] is not None:
                    self.interactions['neutral'][FUNCTION](*self.interactions['neutral'][ARGUMENT])
                    self.message_stack.append(self.interactions['neutral'][MESSAGE])
            else:
                if self.interactions['positive'][FUNCTION] is not None:
                    self.interactions['positive'][FUNCTION](*self.interactions['positive'][ARGUMENT])
                    self.message_stack.append(self.interactions['positive'][MESSAGE])

    def path(self, board):
        direction = [0, 0]
        move_value = random.choice([-1, -1, 0, 1, 1])
        move_axis = random.choice([0, 1])
        direction[move_axis] = move_value
        self.move_attempt(board, *direction)
