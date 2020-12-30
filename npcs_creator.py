import csv
import random
import entities


class NpcCreator():
    NAME = 0
    DESCR = 1
    POS_FUNCTION = 2
    POS_ARGUMENTS = 3
    POS_MESSAGE = 4
    NEU_FUNCTION = 5
    NEU_ARGUMENTS = 6
    NEU_MESSAGE = 7
    NGT_FUNCTION = 8
    NGT_ARGUMENTS = 9
    NGT_MESSAGE = 10
    TRSH_NEU = 11
    TRSH_POS = 12
    MAIN_IMAGE = 13
    ADD_IMAGES = 14

    def __init__(self, functions, used_npc):
        self.used_npc = used_npc
        self.functions = functions
        self.npc_types_list = self.create_npc_types_list()

    def create_npc_types_list(self):
        with open('npcs.csv', newline='', encoding='utf8') as csvfile:
            npcs = csv.reader(csvfile, skipinitialspace=True)
            next(npcs)

            npcs_list = []
            for npc_data in npcs:
                npcs_list = self.add_npc_type(npcs_list, npc_data)

        for element in npcs_list:
            element[self.POS_ARGUMENTS] = self.convert_string_to_list(element[self.POS_ARGUMENTS])
            element[self.NEU_ARGUMENTS] = self.convert_string_to_list(element[self.NEU_ARGUMENTS])
            element[self.NGT_ARGUMENTS] = self.convert_string_to_list(element[self.NGT_ARGUMENTS])

            for i in range(self.ADD_IMAGES, len(element)):
                element[i] = element[i].strip('][').split(', ')

        return npcs_list

    def convert_string_to_list(self, string_like_list):
        string_like_list = string_like_list.strip('][').split(', ')
        i = 0
        for i in range(len(string_like_list)):
            if string_like_list[i].isnumeric():
                string_like_list[i] = int(string_like_list[i])
        return string_like_list

    def add_npc_type(self, npcs_list, npc_data):
        npc = []
        for element in npc_data:
            npc.append(element)
        if npc[self.NAME] not in self.used_npc:
            npcs_list.append(npc)
        return npcs_list

    def get_random_npc_data(self):
        i = random.randint(0, len(self.npc_types_list)-1)
        return self.npc_types_list.pop(i)

    def generate_npc_object(self):
        npc_data = self.get_random_npc_data()
        name = npc_data[self.NAME]
        descr = npc_data[self.DESCR]
        pos_function = self.functions[npc_data[self.POS_FUNCTION]]
        pos_argument = npc_data[self.POS_ARGUMENTS]
        pos_message = npc_data[self.POS_MESSAGE]
        neu_function = self.functions[npc_data[self.NEU_FUNCTION]]
        neu_argument = npc_data[self.NEU_ARGUMENTS]
        neu_message = npc_data[self.NEU_MESSAGE]
        ngt_function = self.functions[npc_data[self.NGT_FUNCTION]]
        ngt_argument = npc_data[self.NGT_ARGUMENTS]
        ngt_message = npc_data[self.NGT_ARGUMENTS]
        thr_neu = int(npc_data[self.TRSH_NEU])
        thr_pos = int(npc_data[self.TRSH_POS])

        image_map = [[0, 0, npc_data[self.MAIN_IMAGE]]]
        for i in range(self.ADD_IMAGES, len(npc_data)):
            if npc_data[i] != ['']:
                npc_data[i][0] = int(npc_data[i][0])
                npc_data[i][1] = int(npc_data[i][1])
                image_map.append(npc_data[i])

        return entities.Npc(
                image_map=image_map,
                name=name,
                description=descr,
                interaction_function_positive=pos_function,
                interaction_argument_positive=pos_argument,
                interaction_message_positive=pos_message,
                interaction_function_neutral=neu_function,
                interaction_argument_neutral=neu_argument,
                interaction_message_neutral=neu_message,
                interaction_function_negative=ngt_function,
                interaction_argument_negative=ngt_argument,
                interaction_message_negative=ngt_message,
                threshold_neutral=thr_neu,
                threshold_positive=thr_pos,
                )
