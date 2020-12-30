import entities
import random
import enemy_creator
import interactable_creator
import npcs_creator
from util import dice
import inventory

BOARD_HEIGHT = 30
BOARD_WIDTH = 90

NUM_OF_RECTANGLES = 40
RECTANGLE_MIN_WIDTH = 5
RECTANGLE_MAX_WIDTH = 15
RECTANGLE_MIN_HEIGHT = 5
RECTANGLE_MAX_HEIGHT = 10
STARTING_X = 2
STARTING_Y = 2
SQUARE_DIM = 8
NUM_VOID_RECTS = 20
CORRIDOR_HEIGHT = 3
CORRIDOR_WIDTH = 3
LOWER_CORRIDOR = BOARD_HEIGHT // 4 * 3
MIDDLE_COLUMN = BOARD_WIDTH // 2
UPPER_CORRIDOR = BOARD_HEIGHT // 4
OFFSET = 20

VIEW_RANGE_ROUNDER = 0.2


class Level:
    was_explored = False

    def __init__(self, game, player, rank):
        self.rank = rank
        self.board = self.create_board()

        self.interactables = []
        self.enemies = []
        self.npcs = []

        self.interactables.append(entities.Interactable(
            x=self.get_stairs_coords(LOWER_CORRIDOR, MIDDLE_COLUMN, OFFSET)[0],
            y=self.get_stairs_coords(LOWER_CORRIDOR, MIDDLE_COLUMN, OFFSET)[1],
            image_map=[[0, 0, f'{entities.BLUE}\u2303{entities.RES}']],
            description='Stairs leading to next level',
            interaction_function=player.go_to_next_level,
            interaction_argument=[game]
            ))
        self.interactables.append(entities.Interactable(
            x=self.get_stairs_coords(UPPER_CORRIDOR, MIDDLE_COLUMN, OFFSET)[0],
            y=self.get_stairs_coords(UPPER_CORRIDOR, MIDDLE_COLUMN, OFFSET)[1],
            image_map=[[0, 0, f'{entities.BLUE}\u2304{entities.RES}']],
            description='Stairs leading to previous level',
            interaction_function=player.go_to_previous_level,
            interaction_argument=[game]
            ))

        # Create interactables
        functions = {'player_status_change': player.stats.change_stat,
                     'player_status_change_by%': player.stats.change_stat_by_percent,
                     'player_add_temp_attr_bonus': player.stats.add_temp_attr_bonus,
                     'player_attribute_change': player.stats.change_base_attr,
                     'take_item': player.take_item,
                     'None': None,
                     '': None,
                     }

        interactables_creator = interactable_creator.InteractableCreator(self.rank, functions)
        interactables_number = 7

        for i in range(interactables_number):
            self.interactables.append(interactables_creator.generate_interactable_object())

        # Create enemies
        enemies_creator = enemy_creator.EnemyCreator(self.rank)
        enemies_number = 14 + dice(6) + rank

        for i in range(enemies_number):
            self.enemies.append(enemies_creator.generate_enemy_object())

        # Create NPCs
        npc_creator = npcs_creator.NpcCreator(functions, game.used_npc)
        if len(npc_creator.npc_types_list) > 0:
            self.npcs.append(npc_creator.generate_npc_object())
          
        club = inventory.Equipable('club', 2, 'right_hand', [['damage', 1], ['attack', 3]], 10)
        self.board[2][4].inventory.add_to_inventory(club)

    def create_board(self):

        new_map = [[Field('void', image=' ') for y in range(0, BOARD_WIDTH)] for x in range(0, BOARD_HEIGHT)]

        # draw randomly 40 floor rectangles with variable sizes
        self.draw_floor_rectangles(new_map, NUM_OF_RECTANGLES)

        # create space for player in top-left corner
        starting_point = Rectangle((STARTING_X, STARTING_Y), (SQUARE_DIM, SQUARE_DIM))
        starting_point.create_rectangle(new_map, Field, 'floor', image='\u2591')

        # add 20 void rectangles in the middle of the map
        self.draw_void_rectangles(new_map, NUM_VOID_RECTS)

        # horizontal corridors
        random_y = random.randint(1, 5)
        self.draw_corridors(new_map, BOARD_HEIGHT // 2, random_y, BOARD_WIDTH - random_y - 1, CORRIDOR_HEIGHT)
        random_y = random.randint(1, 5)
        self.draw_corridors(new_map, BOARD_HEIGHT // 4, random_y, BOARD_WIDTH - random_y - 1, CORRIDOR_HEIGHT)
        random_y = random.randint(1, 5)
        self.draw_corridors(new_map, BOARD_HEIGHT // 4 * 3, random_y, BOARD_WIDTH - random_y - 1, CORRIDOR_HEIGHT)

        # vertical corridors
        starting_y = 10
        self.draw_corridors(new_map, BOARD_HEIGHT // 4, starting_y, CORRIDOR_WIDTH, BOARD_HEIGHT // 2)
        starting_y = 80
        self.draw_corridors(new_map, BOARD_HEIGHT // 4, starting_y, CORRIDOR_WIDTH, BOARD_HEIGHT // 2)

        # draw borders
        self.draw_borders(new_map, BOARD_HEIGHT, BOARD_WIDTH, 0, 0, -1, 0)
        self.draw_borders(new_map, BOARD_HEIGHT, BOARD_WIDTH, 0, 0, 0, -1)
        self.draw_borders(new_map, BOARD_HEIGHT, BOARD_WIDTH, -1, 0, 0, 0)
        self.draw_borders(new_map, BOARD_HEIGHT, BOARD_WIDTH, 0, -1, 0, 0)

        return new_map

    def get_stairs_coords(self, corridor, column, offset):
        x, y = corridor + 1, random.randint(column, column + offset)

        return x, y

    def draw_floor_rectangles(self, new_map, quantity):
        for i in range(quantity):

            width = random.randint(RECTANGLE_MIN_WIDTH, RECTANGLE_MAX_WIDTH)
            height = random.randint(RECTANGLE_MIN_HEIGHT, RECTANGLE_MAX_HEIGHT)

            x = random.randint(1, BOARD_HEIGHT - height - 1)
            y = random.randint(1, BOARD_WIDTH - width - 1)

            new_rectangle = Rectangle((x, y), (width, height))
            new_rectangle.create_rectangle(new_map, Field, 'floor', image='\u2591')

    def draw_borders(self, new_map, height, width, floor_x_offset, floor_y_offset, void_x_offset, void_y_offset):
        for row_index in range(height):
            for column_index in range(width):
                if (new_map[row_index + floor_x_offset][column_index + floor_y_offset].surface_name == 'floor'
                   and new_map[row_index + void_x_offset][column_index + void_y_offset].surface_name == 'void'):

                    new_map[row_index + void_x_offset][column_index + void_y_offset].entity = \
                        entities.Entity(row_index + void_x_offset,
                                        column_index + void_y_offset,
                                        image_map=[[0, 0, 'X']],
                                        description='wall')

    def draw_corridors(self, new_map, start_x, start_y, width, height):
        corridor = Rectangle((start_x, start_y), (width, height))
        corridor.create_rectangle(new_map, Field, 'floor', image='\u2591')

    def draw_void_rectangles(self, new_map, quantity):
        for x in range(quantity):
            random_x = random.randint(5, 20)
            random_y = random.randint(10, 80)
            random_w = random.randint(2, 8)
            random_h = random.randint(2, 8)
            void_rectangle = Rectangle((random_x, random_y), (random_w, random_h))
            void_rectangle.create_rectangle(new_map, Field, 'void', image=' ')


class Field:
    def __init__(self, surface_name, bonus=None, image=None, entity=None):
        self.surface_name = surface_name
        self.inventory = inventory.Inventory()
        self.bonus = bonus
        self.image = image
        self.entity = entity

    def representation(self, x, y, player, developer_mode=False,):
        sight_range = player.stats.attributes['perception']['current'] + VIEW_RANGE_ROUNDER
        if (not developer_mode and
                player.find_distance(x, y) > sight_range):
            repre = ' '
        elif self.entity is not None:
            repre = self.entity.image(x, y)
        elif self.inventory.inventory:
            repre = '*'
        else:
            repre = self.image
        return repre


class Rectangle:
    def __init__(self, coords, size):
        self.x1, self.y1 = coords
        self.height, self.width = size
        self.y2 = self.y1 + self.height
        self.x2 = self.x1 + self.width

    def create_rectangle(self, new_map, obj, surface_name, image):
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                params = {'surface_name': surface_name, 'image': image}
                new_map[x][y] = obj(**params)

        return new_map
