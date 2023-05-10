from main import *
from time import sleep


def alphabeta(depth, a, b, game):
    if depth == 0:
        game.evaluate()
        print(game.evaluation)
        return game.evaluation
    node_rate, new_rate = 10000, 0

    game.board.if_checks_pins()
    for move in game.board.get_moves()[0]:
        game_copy = copy.deepcopy(game)
        game_copy.board.if_checks_pins()
        game_copy.board.make_move(move)
        game_copy.board.set_pieces()
        game_copy.board.update_board()
        new_rate = -alphabeta(depth-1, a, b, game_copy)
        if new_rate < node_rate:
            node_rate = new_rate
        if node_rate < a:
            a = node_rate
        if a > b:
            break
    return node_rate


def play_chess():
    print('Hi')
    game = Game()
    movesss = ['e4', 'Nf3', 'Ne5', 'Qf3', 'Qh5']  # 'e4', 'Nf3', 'Ne5', 'Qf3', 'Qh5'
    moevs = []  # 'a6', 'a5', 'a4', 'f6'
    while game.get_winner() == 0:
        if game.board.get_flag() == 1:
            if len(movesss) > 0:
                game.lets_play(movesss[0])
                movesss.pop(0)
            else:
                game.lets_play('')
        else:
            if len(moevs) > 0:
                game.lets_play(moevs[0])
                moevs.pop(0)
            else:
                game.board.all_moves()
                game.board.if_checks_pins()
                moves = game.board.get_moves()[0]
                best = 10000
                i = 0
                print(moves)
                for move in moves:
                    # i += 1
                    # print(f'{i} - {move}, ', end='')
                    game_copy = copy.deepcopy(game)
                    game_copy.board.if_checks_pins()
                    game_copy.board.make_move(move)
                    game_copy.board.set_pieces()
                    game_copy.board.update_board()
                    if game_copy.get_winner() == -1:
                        my_move = move
                    elif game.get_winner() == 0:
                        ab = alphabeta(2, 10000, -10000, game_copy)
                        if ab < best:
                            best = ab
                            my_move = move
                game.lets_play(my_move)


if __name__ == '__main__':
    play_chess()