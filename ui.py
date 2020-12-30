from colored import fg, attr

NUM_MSG = 8

GREEN = fg('green')
YELLOW = fg('yellow_1')
ORANGE = fg('orange_red_1')
RED = fg('red')
RES = attr('reset')


def display_status(game, player, enemies, developer_mode):
    print(f'{RED}Level: {game.current_level.rank + 1} \
    HP {player.stats.status["hp"]["current"]}/{player.stats.status["hp"]["max_current"]} \
    Rank: {player.advancement["rank"]} \
    Experience gathered: {player.advancement["experience"]}{RES}\n')


def display_board(board, player, developer_mode):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    game_board = ''

    for row in board:
        x = board.index(row)
        for obj in row:
            y = row.index(obj)
            game_board += str(obj.representation(x, y, player,
                                                 developer_mode=developer_mode,
                                                 ))
        game_board += '\n'

    print(game_board)


def display_messages(game_messages):
    game_messages = game_messages[::-1]
    for message in game_messages[:NUM_MSG]:
        print(f'{RED}{message}{RES}')
