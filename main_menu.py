import menu_ui
import util
import engine
import help_menu


class Menu():
    def run(self):
        self.is_running = True
        self.selector = 8

        self.commands = {"w": [self.selector_up, ()],
                         "s": [self.selector_down, ()],
                         "F": [self.stop_running, ()],
                         }

        ui = menu_ui.MenuController()

        while self.is_running:

            util.clear_screen()
            ui.display_screen(self)
            key = util.key_pressed()

            if key in self.commands:
                self.commands[key][0](*self.commands[key][1])

            if key == '\r' and self.selector == 8:
                player = None
                key = "C"
                while key == 'C'or key == 'c':
                    game = engine.Game(player)
                    player = game.run()
                    del game
                    print("Press C to continue the game, anything else to end this attempt.")
                    key = util.key_pressed()

            if key == '\r' and self.selector == 9:
                show_help = help_menu.HelpMenu()
                show_help.run()

            if key == '\r' and self.selector == 10:
                util.clear_screen()
                quit()

            util.clear_screen()

    def stop_running(self):
        self.is_running = False

    def selector_up(self):
        if self.selector > 8:
            self.selector -= 1

    def selector_down(self):
        if self.selector < 10:
            self.selector += 1
