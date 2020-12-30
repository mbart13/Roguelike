import csv
from util import dice
import entities


class InteractableCreator():
    NAME = 0
    DESCR = 1
    FUNCTION = 2
    ARGUMENTS = 3
    CHARGES = 4
    USE_COST = 5
    SPAWN_RATE = 6
    MIN_RANK = 7
    MAX_RANK = 8
    MAIN_IMAGE = 9
    ADD_IMAGES = 10

    def __init__(self, rank, functions):
        self.functions = functions
        self.interactable_types_list = self.create_interactable_types_list(rank)

    def create_interactable_types_list(self, rank):
        with open('interactables.csv', newline='') as csvfile:
            interactables = csv.reader(csvfile, skipinitialspace=True)
            next(interactables)

            interactables_list = []
            for interactable_data in interactables:
                interactables_list = self.add_interactable_type(interactables_list, interactable_data, rank)

        for element in interactables_list:
            element[self.ARGUMENTS] = element[self.ARGUMENTS].strip('][').split(', ')
            i = 0
            for i in range(len(element[self.ARGUMENTS])):
                if element[self.ARGUMENTS][i].isnumeric():
                    element[self.ARGUMENTS][i] = int(element[self.ARGUMENTS][i])
            for i in range(self.ADD_IMAGES, len(element)):
                element[i] = element[i].strip('][').split(', ')

        return interactables_list

    def add_interactable_type(self, interactables_list, interactable_data, level_rank):
        if level_rank >= int(interactable_data[self.MIN_RANK]) and level_rank <= int(interactable_data[self.MAX_RANK]):
            interactable = []
            for element in interactable_data:
                interactable.append(element)

            interactables_list.append(interactable)
        return interactables_list

    def get_random_interactable_data(self):
        sum = 0
        for element in self.interactable_types_list:
            sum += int(element[self.SPAWN_RATE])

        roll = dice(sum)
        interactable = None
        rolling_sum = 1
        i = 0

        while not interactable:
            rolling_sum += int(self.interactable_types_list[i][self.SPAWN_RATE])
            if roll < rolling_sum:
                interactable = self.interactable_types_list[i]
            else:
                i += 1
        return interactable

    def generate_interactable_object(self):
        interactable_data = self.get_random_interactable_data()
        name = interactable_data[self.NAME]
        descr = interactable_data[self.DESCR]
        function = self.functions[interactable_data[self.FUNCTION]]
        argument = interactable_data[self.ARGUMENTS]
        charges = int(interactable_data[self.CHARGES])
        use_cost = int(interactable_data[self.USE_COST])

        image_map = [[0, 0, interactable_data[self.MAIN_IMAGE]]]
        for i in range(self.ADD_IMAGES, len(interactable_data)):
            if interactable_data[i] != ['']:
                interactable_data[i][0] = int(interactable_data[i][0])
                interactable_data[i][1] = int(interactable_data[i][1])
                image_map.append(interactable_data[i])

        return entities.Interactable(
                image_map=image_map,
                name=name,
                description=descr,
                interaction_function=function,
                interaction_argument=argument,
                charges=charges,
                use_cost=use_cost,
                )
