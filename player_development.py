import entities
import player_development_ui
import util


class PlayerDeveloper():
    def run(self, player, first_time=False):
        self.is_running = True
        self.first_time = first_time
        self.old_player = player
        self.new_stats = entities.Stats(hp=player.stats.status['hp']['max_base'],
                                        dmg=player.stats.attributes['damage']['base'],
                                        arm=player.stats.attributes['armor']['base'],
                                        att=player.stats.attributes['attack']['base'],
                                        dfs=player.stats.attributes['defense']['base'],
                                        per=player.stats.attributes['perception']['base'],
                                        cha=player.stats.attributes['charisma']['base'],
                                        )

        for element in self.new_stats.attributes:
            self.new_stats.attributes[element]['advances'] = self.old_player.stats.attributes[element]['advances']

        for element in self.new_stats.status:
            self.new_stats.status[element]['advances'] = self.old_player.stats.status[element]['advances']

        self.new_rank = self.calculate_rank()
        self.points_to_spend = (self.new_rank - self.old_player.advancement['rank']) * 4

        self.selector = 4
        self.commands = {"w": [self.selector_up, ()],
                         "s": [self.selector_down, ()],
                         "a": [self.lower_stat, ()],
                         "d": [self.increase_stat, ()],
                         "F": [self.stop_running, ()],
                         }

        self.attributes_list = [['damage', 1, 1],
                                ['attack', 5, 1],
                                ['armor', 1, 4],
                                ['defense', 3, 1],
                                ['perception', 1, 2],
                                ['charisma', 1, 3]]
        self.status_list = [['hp', 2, 1]]

        ui = player_development_ui.AdvanceScreenController()
        while self.is_running:
            ui.display_screen(self)
            key = util.key_pressed()

            if key in self.commands:
                self.commands[key][0](*self.commands[key][1])

            util.clear_screen()

        for element in self.new_stats.status:
            new_value = self.new_stats.status[element]['max_base']
            self.new_stats.status[element]['max_current'] = new_value
            self.new_stats.status[element]['current'] = new_value
            if first_time:
                self.new_stats.status[element]['advances'] = 0

        for element in self.new_stats.attributes:
            new_value = self.new_stats.attributes[element]['base']
            self.new_stats.attributes[element]['current'] = new_value
            if first_time:
                self.new_stats.attributes[element]['advances'] = 0

        return self.new_stats

    def stop_running(self):
        self.is_running = False

    def selector_up(self):
        if self.selector > 4:
            self.selector -= 1

    def selector_down(self):
        if self.selector < 10:
            self.selector += 1

    def increase_stat(self):
        if self.selector >= 5:
            self.increase_attribute()
        else:
            self.increase_status()

    def increase_attribute(self):
        attribute = self.attributes_list[self.selector - 5][0]
        delta = self.attributes_list[self.selector - 5][1]
        price_multiplier = self.attributes_list[self.selector - 5][2]
        price = (self.new_stats.attributes[attribute]['advances']+1) * price_multiplier
        if price <= self.points_to_spend:
            self.new_stats.attributes[attribute]['base'] += delta
            self.new_stats.attributes[attribute]['advances'] += 1
            self.points_to_spend -= price

    def increase_status(self):
        status = self.status_list[self.selector - 4][0]
        delta = self.status_list[self.selector - 4][1]
        price_multiplier = self.status_list[self.selector - 4][2]
        price = (self.new_stats.status[status]['advances']+1) * price_multiplier
        if price <= self.points_to_spend:
            self.new_stats.status[status]['max_base'] += delta
            self.new_stats.status[status]['advances'] += 1
            self.points_to_spend -= price

    def lower_stat(self):
        pass

    def calculate_rank(self):
        new_rank = self.old_player.advancement['rank']
        exp_to_next = new_rank*100
        while exp_to_next < self.old_player.advancement['experience']:
            self.old_player.advancement['experience'] -= exp_to_next
            new_rank += 1
            exp_to_next = new_rank*100

        return new_rank
