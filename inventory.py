
CAPACITY = 20  # capacity of the players inventory: 20kg


class Item:
    def __init__(self, name, weight, default_slot, special_function, special_function_argument=None, price=None):
        self.name = name
        self.weight = weight
        self.default_slot = default_slot
        self.price = price
        self.special_function = special_function
        self.special_function_argument = special_function_argument

    def use_item(self):
        self.special_function(*self.special_function_argument)

    def generate_item(self, name):
        self.name = name


class Equipable(Item):
    def __init__(self, name, weight, default_slot, bonus, price=None):
        self.name = name
        self.weight = weight
        self.default_slot = default_slot
        self.bonus = bonus
        self.price = price


class Inventory():
    def __init__(self):
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)


class Player_Inventory(Inventory):
    def __init__(self):
        self.inventory = {'backpack': [],  # default slot for usable items
                          'left_hand': None,
                          'right_hand': None,
                          'head': None,
                          'torso': None,
                          'belt': None,  # slot for extra weapon
                          }

    def add_item_to_backpack(self, item):
        self.inventory["backpack"].append(item)

    def equip_item(self, item):
        if item.default_slot is None:
            print("You can't equip this item")
        elif item.default_slot in self.inventory.keys():
            if self.inventory[item.default_slot] is None:
                self.inventory[item.default_slot] = item
            else:
                self.add_item_to_backpack(self.inventory[item.default_slot])
                self.inventory[item.default_slot] = item

    def remove_item(self, item, slot):
        if slot in self.inventory.keys():
            if slot == 'backpack':
                self.inventory[slot].remove(item)
            else:
                self.inventory[slot] = None

    # def pick_item(self, item):  --> Player

    # def drop_item(self, item):  --> Player

    def exchange_item(self, item):
        """ Exchange items with npc's, containers.
        """
        pass
