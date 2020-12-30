import csv
from util import dice
import entities


class EnemyCreator():
    NAME = 0
    HP = 1
    DAMAGE = 2
    ARMOR = 3
    ATTACK = 4
    DEFENSE = 5
    DESCR = 6
    AGRO_RANGE = 7
    DIAGONAL = 8
    SPEED = 9
    SPAWN_RATE = 10
    MIN_RANK = 11
    MAX_RANK = 12
    MAIN_IMAGE = 13
    ADD_IMAGES = 14

    def __init__(self, rank):
        self.enemy_types_list = self.create_enemy_types_list(rank)

    def create_enemy_types_list(self, rank):
        with open('enemies.csv', newline='') as csvfile:
            enemies = csv.reader(csvfile, skipinitialspace=True)
            next(enemies)

            enemies_list = []
            for enemy_data in enemies:
                enemies_list = self.add_enemy_type(enemies_list, enemy_data, rank)

        for element in enemies_list:
            for i in range(self.ADD_IMAGES, len(element)):
                element[i] = element[i].strip('][').split(', ')

        return enemies_list

    def add_enemy_type(self, enemies_list, enemy_data, level_rank):
        if level_rank >= int(enemy_data[self.MIN_RANK]) and level_rank <= int(enemy_data[self.MAX_RANK]):
            enemy = []
            for element in enemy_data:
                enemy.append(element)

            enemies_list.append(enemy)
        return enemies_list

    def get_random_enemy_data(self):
        sum = 0
        for element in self.enemy_types_list:
            sum += int(element[self.SPAWN_RATE])

        roll = dice(sum)
        enemy = None
        rolling_sum = 1
        i = 0

        while not enemy:
            rolling_sum += int(self.enemy_types_list[i][self.SPAWN_RATE])
            if roll < rolling_sum:
                enemy = self.enemy_types_list[i]
            else:
                i += 1
        return enemy

    def generate_enemy_object(self):
        enemy_data = self.get_random_enemy_data()

        # Prepare image map
        image_map = [[0, 0, enemy_data[self.MAIN_IMAGE]]]
        for i in range(self.ADD_IMAGES, len(enemy_data)):
            if enemy_data[i] != ['']:
                enemy_data[i][0] = int(enemy_data[i][0])
                enemy_data[i][1] = int(enemy_data[i][1])
                image_map.append(enemy_data[i])

        # Prepare stats set
        stats_set = [int(enemy_data[self.HP]),
                     int(enemy_data[self.DAMAGE]),
                     int(enemy_data[self.ARMOR]),
                     int(enemy_data[self.ATTACK]),
                     int(enemy_data[self.DEFENSE]),
                     ]

        # Prepare other
        name = enemy_data[self.NAME]
        description = enemy_data[self.DESCR]
        agro_range = int(enemy_data[self.AGRO_RANGE])
        diagonal = bool(int(enemy_data[self.DIAGONAL]))
        speed = int(enemy_data[self.SPEED])

        # return object
        return entities.Enemy(image_map=image_map,
                              name=name,
                              stats_set=stats_set,
                              description=description,
                              agro_range=agro_range,
                              diagonal_movement=diagonal,
                              speed=speed,)
