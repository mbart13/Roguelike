import csv
from util import dice
import inventory


class ItemCreator():
    NAME = 0
    WEIGHT = 1
    SLOT = 2
    PRICE = 3
    SPAWN_RATE = 4
    MIN_RANK = 5
    MAX_RANK = 6
    BONUS = 7
    ADD_BONUS = 8

    def __init__(self, rank):
        self.items_types_list = self.create_items_types_list(rank)

    def create_items_types_list(self, rank):
        with open('equipables.csv', newline='') as csvfile:
            items_list = csv.reader(csvfile, skipinitialspace=True)
            next(items_list)

            item_list = []
            for items_data in items_list:
                item_list = self.add_item_type(item_list, items_data, rank)

        for element in item_list:
            i = 0
            for i in range(self.BONUS, len(element)):
                element[i] = element[i].strip('][').split(', ')

        return item_list

    def add_item_type(self, item_list, item_dat, level_rank):
        if level_rank >= int(item_dat[self.MIN_RANK]) and level_rank <= int(item_dat[self.MAX_RANK]):
            item = []
            for element in item_dat:
                item.append(element)

            item_list.append(item)
        return item_list

    def get_random_item_data(self):
        sum = 0
        for element in self.items_types_list:
            sum += int(element[self.SPAWN_RATE])

        roll = dice(sum)
        item = None
        rolling_sum = 1
        i = 0

        while not item:
            rolling_sum += int(self.items_types_list[i][self.SPAWN_RATE])
            if roll < rolling_sum:
                item = self.items_types_list[i]
            else:
                i += 1
        return item

    def generate_item_object(self):
        item_dat = self.get_random_item_data()
        name = item_dat[self.NAME]
        weight = int(item_dat[self.WEIGHT])
        slot = item_dat[self.SLOT]
        price = int(item_dat[self.PRICE])

        bonus = [item_dat[self.BONUS]]
        for i in range(self.ADD_BONUS, len(item_dat)):
            if item_dat[i] != ['']:
                item_dat[i][1] = int(item_dat[i][1])
                bonus.append(item_dat[i])

        return inventory.Equipable(name,
                                   weight,
                                   slot,
                                   bonus,
                                   price=price,)
