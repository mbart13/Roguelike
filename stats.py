import util
import stats_ui


class StatsMenu():
    def run(self, player):
        self.is_running = True
        while self.is_running:
            util.clear_screen()
            ui = stats_ui.StatsView()
            ui.show_statistics(player)
            key = util.key_pressed()
            if key == '\x1b':
                self.is_running = False
