from colored import fg, attr

# Colors
RES = attr('reset')
GREEN = fg('green')
RED = fg('red')


class StatsView():
    def show_statistics(self, player):
        status = player.stats.status
        attr = player.stats.attributes
        for key in status:
            print(f'{RED}{key}{RES}: ', end='')
            for key_2, value in status[key].items():
                print(f' {GREEN}{key_2}: {value}{RES}', end='')
        for key in attr:
            print(f'\n{RED}{key}{RES}: ', end='')
            for key_2, value in attr[key].items():
                print(f' {GREEN}{key_2}: {value}{RES}', end='')

        print('\n\nPress ESC to go back to game')
