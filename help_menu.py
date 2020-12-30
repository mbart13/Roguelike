import util
import help_ui


class HelpMenu():

    def run(self):
        self.is_running = True
        while self.is_running:
            util.clear_screen()
            ui = help_ui.HelpView()
            ui.show_help()
            key = util.key_pressed()
            if key == '\x1b':
                self.is_running = False
