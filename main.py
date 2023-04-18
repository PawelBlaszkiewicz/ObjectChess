global transition_dict
global transition_dict1


def count_coordinates(tab, move, num):
    coordinates = {}
    for piece in tab.keys():
        if move in tab[piece]:
            if piece.get_position()[num] in coordinates.keys():
                a = coordinates[piece.get_position()[num]]
                a += 1
                coordinates[piece.get_position()[num]] = a
            else:
                coordinates[piece.get_position()[num]] = 1
    return coordinates


def rank_moves_and_coordinates(tab):
    ranking = {}
    for val in tab.values():
        for move in val:
            if move in ranking.keys():
                a = ranking[move]
                a += 1
                ranking[move] = a
            else:
                ranking[move] = 1

    good_moves = [i for i in ranking if ranking[i] == 1]
    for i in good_moves:
        if i in ranking.keys():
            for piece in tab.keys():
                if i in tab[piece]:
                    tab[piece].pop(tab[piece].index(i))
            del ranking[i]
    return ranking, tab, good_moves


def format_multiple_knight_moves(ranking, tab, good_moves, cap_switch):
    for move in ranking.keys():
        coordinates0 = count_coordinates(tab, move, 0)
        coordinates1 = count_coordinates(tab, move, 1)

        for piece in tab.keys():
            x = piece.get_position()[0]
            y = piece.get_position()[1]
            if x in coordinates0.keys() and y in coordinates1.keys():
                if cap_switch == 0:
                    pmove = 'N'
                elif cap_switch == 1:
                    pmove = 'Nx'
                if coordinates0[x] == 1:
                    pmove = pmove + '{}{}{}'.format(get_chess_coordinates(y, x)[1], move[-2], move[-1])
                elif coordinates1[y] == 1:
                    pmove = pmove + '{}{}{}'.format(get_chess_coordinates(y, x)[0], move[-2], move[-1])
                else:
                    pmove = pmove + '{}{}{}{}'.format(get_chess_coordinates(y, x)[0],
                                               get_chess_coordinates(y, x)[1], move[-2], move[-1])
                good_moves.append(pmove)
    return good_moves


def pawn_promotion(color, desired_piece, coordinates):
    promoted_pawn = Queen(coordinates, color)
    if desired_piece == 'R':
        promoted_pawn = Rook(coordinates, color)
    elif desired_piece == 'B':
        promoted_pawn = Bishop(coordinates, color)
    elif desired_piece == 'N':
        promoted_pawn = NKnight(coordinates, color)
    return promoted_pawn


class Board:

    def __init__(self, all_pieces):
        self._pieces = all_pieces
        self.__board = []
        self.white = {}
        self.black = {}
        self.__flag = 1
        self.__possible_moves = []

    def get_pieces(self):
        return self._pieces

    def get_board(self):
        return self.__board

    def get_flag(self):
        return self.__flag

    def get_moves(self):
        return self.__possible_moves

    def set_flag(self):
        if self.__flag == 1:
            self.__flag = 0
        else:
            self.__flag = 1

    def set_board(self, board):

        self.__board = board

    def add_moves(self, moves):
        self.__possible_moves.append(moves)

    def set_pieces(self):
        self._pieces.clear()
        self._pieces.update(self.white)
        self._pieces.update(self.black)

    def show_board(self):
        print(f'- |+++++++++++++++++++++++++++++++++++++++| ')
        for i in range(7, -1, -1):
            print(end=f'{i + 1} ')  # Here in future showing game moves on the right side of the board and maybe
            print(end='| ')  # after game saving
            for j in range(8):
                if isinstance(self.__board[i][j], str):
                    print(f'{self.__board[i][j]}', end=' | ')
                elif (i + j) % 2 == 1:
                    print(f'//', end=' | ')
                else:
                    print(f' ', end='  | ')
            if i > 0:
                print(f'\n- |----+----+----+----+----+----+----+----| ')
        print(f'\n- |+++++++++++++++++++++++++++++++++++++++| ')
        print(f'  - A  - B  - C  - D  - E  - F  - G  - H  -')

    def sort_pieces(self):
        for key in self.get_pieces().keys():
            piece = self.get_pieces()[key]
            working_dict = {key: piece}
            if piece.get_color() == 'white':
                self.white.update(working_dict)
            else:
                self.black.update(working_dict)

    def set_pieces_on_board(self):
        board = [[0] * 8 for i in range(8)]

        for piece in self.get_pieces().values():
            board[piece.get_position()[0]][piece.get_position()[1]] = piece.get_name()

        self.set_board(board)
        self.show_board()

    def clear_prev_pos_for_pieces(self):
        if self.get_flag() == 1:
            for figure in self.white.values():
                figure.set_prev_position([])
        else:
            for figure in self.black.values():
                figure.set_prev_position([])

    def move_white_piece(self, piece, coordinates):
        self.clear_prev_pos_for_pieces()
        a = [i for i in self.white if self.white[i] == piece][0]
        piece.set_prev_position(piece.get_position())
        piece.change_position(coordinates)
        self.white[a] = piece
        self.set_flag()

    def move_black_piece(self, piece, coordinates):
        self.clear_prev_pos_for_pieces()
        a = [i for i in self.black if self.black[i] == piece][0]
        piece.set_prev_position(piece.get_position())
        piece.change_position(coordinates)
        self.black[a] = piece
        self.set_flag()

    def short_castling(self, king, rook):
        self.clear_prev_pos_for_pieces()
        if self.get_flag() == 1:
            a = [i for i in self.white if self.white[i] == king][0]
            b = [i for i in self.white if self.white[i] == rook][0]
            king.set_prev_position([0, 4])
            rook.set_prev_position([0, 7])
            king.change_position([0, 6])
            rook.change_position([0, 5])
            self.white[a] = king
            self.white[b] = rook
        else:
            a = [i for i in self.black if self.black[i] == king][0]
            b = [i for i in self.black if self.black[i] == rook][0]
            king.set_prev_position([7, 4])
            rook.set_prev_position([7, 7])
            king.change_position([7, 6])
            rook.change_position([7, 5])
            self.black[a] = king
            self.black[b] = rook
        self.set_flag()

    def long_castling(self, king, rook):
        self.clear_prev_pos_for_pieces()
        if self.get_flag() == 1:
            a = [i for i in self.white if self.white[i] == king][0]
            b = [i for i in self.white if self.white[i] == rook][0]
            king.set_prev_position([0, 4])
            rook.set_prev_position([0, 0])
            king.change_position([0, 2])
            rook.change_position([0, 3])
            self.white[a] = king
            self.white[b] = rook
        else:
            a = [i for i in self.black if self.black[i] == king][0]
            b = [i for i in self.black if self.black[i] == rook][0]
            king.set_prev_position([7, 4])
            rook.set_prev_position([7, 0])
            king.change_position([7, 2])
            rook.change_position([7, 3])
            self.black[a] = king
            self.black[b] = rook
        self.set_flag()
        return 0

    def pawn_capture(self, coordinates, first_coor, move):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
            a = -1
            other_pieces_d = self.black
        else:  # black to move
            piece_list = self.black.values()
            a = 1
            other_pieces_d = self.white

        for piece in piece_list:
            if piece.get_name()[1] == 'P' and piece.get_position()[1] == first_coor[1] \
                    and piece.get_position()[0] == coordinates[0] + a:  # check if good place for diagonal pawn capture

                if self.get_board()[coordinates[0]][coordinates[1]] == 0:  # check if en passant
                    b = [i for i in other_pieces_d if other_pieces_d[i].get_position() ==
                         [coordinates[0] + a, coordinates[1]] and other_pieces_d[i].get_name()[1] == 'P']

                    if len(b) > 0 and len(other_pieces_d[b[0]].get_prev_position()) > 0 and\
                            other_pieces_d[b[0]].get_prev_position()[0] == \
                            other_pieces_d[b[0]].get_position()[0] - a - a:

                        del other_pieces_d[b[0]]
                        move_flag = 1
                        if self.get_flag() == 1:
                            self.move_white_piece(piece, coordinates)
                        else:
                            self.move_black_piece(piece, coordinates)

                    print("En passant, kmiocie!")
                    break
                else:  # normal capture
                    b = [i for i in other_pieces_d if other_pieces_d[i].get_position() == coordinates]
                    if len(b) > 0:
                        if other_pieces_d[b[0]].get_position()[0] == 7:  # white promotion after capture
                            move_flag = 1

                            if len(move) < 5:
                                promoted_pawn = pawn_promotion('white', 'Q', coordinates)
                            else:
                                promoted_pawn = pawn_promotion('white', move[5], coordinates)

                            for i in range(8):
                                if i not in self.white.keys():
                                    work_dict = {i: promoted_pawn}
                                    self.white.update(work_dict)  # add promoted piece
                                    break

                            del other_pieces_d[b[0]]  # delete captured piece from dict
                            c = [i for i in self.white if self.white[i] == piece]
                            del self.white[c[0]]  # delete pawn
                            self.set_flag()

                        elif other_pieces_d[b[0]].get_position()[0] == 0:  # black promotion after capture
                            move_flag = 1

                            if len(move) < 5:
                                promoted_pawn = pawn_promotion('black', 'Q', coordinates)
                            else:
                                promoted_pawn = pawn_promotion('black', move[5], coordinates)

                            for i in range(8):
                                if i not in self.black.keys():
                                    work_dict = {i: promoted_pawn}
                                    self.black.update(work_dict)  # add promoted piece
                                    break

                            del other_pieces_d[b[0]]  # delete captured piece from dict
                            c = [i for i in self.black if self.black[i] == piece]
                            del self.black[c[0]]  # delete pawn
                            self.set_flag()

                        elif self.get_flag() == 1:  # normal capture
                            self.move_white_piece(piece, coordinates)
                            del other_pieces_d[b[0]]  # delete captured piece from dict
                            move_flag = 1
                        else:
                            self.move_black_piece(piece, coordinates)
                            del other_pieces_d[b[0]]  # delete captured piece from dict
                            move_flag = 1
                        print('he ATTACK!')
                        break
        if move_flag == 0:
            print(f'Nie możesz wykonać bicia {move}.')
            print(f'Zaproponuj inny ruch.')

    def pawn_move(self, coordinates, move):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
            a = -1
        else:
            piece_list = self.black.values()
            a = 1

        for piece in piece_list:
            if piece.get_name()[1] == 'P' and piece.get_position()[1] == coordinates[1] \
                    and self.get_board()[coordinates[0]][coordinates[1]] == 0:
                if self.get_flag() == 1 and piece.get_position()[0] == 1 and coordinates[0] == 3 \
                        and self.get_board()[coordinates[0] + a][coordinates[1]] == 0:  # jump over 2 squares
                    move_flag = 1
                    self.move_white_piece(piece, coordinates)
                    break
                elif self.get_flag() == 0 and piece.get_position()[0] == 6 and coordinates[0] == 4 \
                        and self.get_board()[coordinates[0] + a][coordinates[1]] == 0:
                    move_flag = 1
                    self.move_black_piece(piece, coordinates)
                    break
                elif piece.get_position()[0] == coordinates[0] + a:
                    if coordinates[0] == 7:  # white promotion
                        move_flag = 1
                        if len(move) < 3:
                            promoted_pawn = pawn_promotion('white', 'Q', coordinates)
                        else:
                            promoted_pawn = pawn_promotion('white', move[3], coordinates)

                        for i in range(8):
                            if i not in self.white.keys():
                                work_dict = {i: promoted_pawn}
                                self.white.update(work_dict)
                                break

                        b = [i for i in self.white if self.white[i] == piece]
                        del self.white[b[0]]
                        break
                    elif coordinates[0] == 0:  # black promotion
                        move_flag = 1
                        if len(move) < 3:
                            promoted_pawn = pawn_promotion('white', 'Q', coordinates)
                        else:
                            promoted_pawn = pawn_promotion('white', move[3], coordinates)

                        for i in range(8, 16):
                            if i not in self.black.keys():
                                work_dict = {i: promoted_pawn}
                                self.black.update(work_dict)
                                break

                        b = [i for i in self.black if self.black[i] == piece]
                        del self.black[b[0]]
                        break
                    else:
                        move_flag = 1
                        if self.get_flag() == 1:
                            self.move_white_piece(piece, coordinates)
                        else:
                            self.move_black_piece(piece, coordinates)
                        break
        if move_flag == 0:
            print(f'{move} jest niewykonalne. Wykonaj inny ruch.')

    def capture_piece_from_adequate_square(self, piece, move, coordinates, other_pieces_d, b):
        move_flag = 0
        if move[1] in [str(1), str(2), str(3), str(4), str(5), str(6), str(7), str(8)] \
                and piece.get_position()[0] == get_board_list_coordinates('a', move[1])[1]:
            if self.get_flag() == 1:
                self.move_white_piece(piece, coordinates)
                del other_pieces_d[b[0]]
                move_flag = 1
            elif self.get_flag() == 0:
                self.move_black_piece(piece, coordinates)
                del other_pieces_d[b[0]]
                move_flag = 1
        elif move[1] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] and \
                piece.get_position()[1] == get_board_list_coordinates(move[1], 1)[0]:
            if self.get_flag() == 1:
                self.move_white_piece(piece, coordinates)
                del other_pieces_d[b[0]]
                move_flag = 1
            elif self.get_flag() == 0:
                self.move_black_piece(piece, coordinates)
                del other_pieces_d[b[0]]
                move_flag = 1
        return move_flag

    def normal_capture(self, piece, coordinates, other_pieces_d, b):
        move_flag = 0
        if self.get_flag() == 1:  # normal capture
            self.move_white_piece(piece, coordinates)
            del other_pieces_d[b[0]]
            move_flag = 1
        elif self.get_flag() == 0:
            self.move_black_piece(piece, coordinates)
            del other_pieces_d[b[0]]
            move_flag = 1
        return move_flag

    def move_piece_from_adequate_square(self, piece, coordinates, move):
        move_flag = 0
        if move[1] in [str(1), str(2), str(3), str(4), str(5), str(6), str(7), str(8)] \
                and piece.get_position()[0] == get_board_list_coordinates('a', move[1])[1]:
            if self.get_flag() == 1:
                self.move_white_piece(piece, coordinates)
                move_flag = 1
            elif self.get_flag() == 0:
                self.move_black_piece(piece, coordinates)
                move_flag = 1
        elif move[1] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] and \
                piece.get_position()[1] == get_board_list_coordinates(move[1], 1)[0]:
            if self.get_flag() == 1:
                self.move_white_piece(piece, coordinates)
                move_flag = 1
            elif self.get_flag() == 0:
                self.move_black_piece(piece, coordinates)
                move_flag = 1
        return move_flag

    def normal_move(self, piece, coordinates):
        move_flag = 0
        if self.get_flag() == 1:  # normal move
            self.move_white_piece(piece, coordinates)
            move_flag = 1
        elif self.get_flag() == 0:
            self.move_black_piece(piece, coordinates)
            move_flag = 1
        return move_flag

    def knight_capture(self, coordinates, move, knight_moves):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
            other_pieces_d = self.black
        else:  # black to move
            piece_list = self.black.values()
            other_pieces_d = self.white

        for piece in piece_list:
            if piece.get_name()[1] == 'N':
                change = [piece.get_position()[0] - coordinates[0], piece.get_position()[1] - coordinates[1]]
                if change in knight_moves:
                    b = [i for i in other_pieces_d if other_pieces_d[i].get_position() == coordinates]
                    if len(b) > 0:
                        if move[2] == 'x':  # if need to choose from 2 or more knights on row or column
                            move_flag = self.capture_piece_from_adequate_square(
                                piece, move, coordinates, other_pieces_d, b)
                        else:
                            move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
        if move_flag == 0:
            print(f'Nie możesz wykonać bicia {move}.')
            print(f'Zaproponuj inny ruch.')
        else:
            print('he JUMP and ATTACK!')

    def knight_move(self, coordinates, move, knight_moves):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
        else:
            piece_list = self.black.values()

        for piece in piece_list:
            if piece.get_name()[1] == "N":
                change = [piece.get_position()[0] - coordinates[0], piece.get_position()[1] - coordinates[1]]
                if change in knight_moves and self.get_board()[coordinates[0]][coordinates[1]] == 0:
                    if len(move) > 3:
                        move_flag = self.move_piece_from_adequate_square(piece, coordinates, move)
                        if move_flag == 1:
                            break
                    else:
                        move_flag = self.normal_move(piece, coordinates)
        if move_flag == 0:
            print(f'Nie możesz wykonać ruchu {move}.')
            print(f'Zaproponuj inny ruch.')
        else:
            print('he JUMP!')

    def bishop_capture(self, coordinates, move, letter):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
            other_pieces_d = self.black
        else:  # black to move
            piece_list = self.black.values()
            other_pieces_d = self.white

        for piece in piece_list:
            if piece.get_name()[1] == letter and move_flag == 0:  # check if bish on adequate diagonal to capture
                if abs(piece.get_position()[0] - coordinates[0]) == (abs(piece.get_position()[1] - coordinates[1])):
                    b = [i for i in other_pieces_d if other_pieces_d[i].get_position() == coordinates]
                    if len(b) > 0:  # check if on coordinates is capturable piece
                        if abs(piece.get_position()[0] - coordinates[0]) == 1:
                            if move[2] == 'x':
                                move_flag = self.capture_piece_from_adequate_square(
                                    piece, move, coordinates, other_pieces_d, b)
                            else:
                                move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
                        elif abs(piece.get_position()[0] - coordinates[0]) > 1:
                            row_change = piece.get_position()[0] - coordinates[0]
                            column_change = piece.get_position()[1] - coordinates[1]
                            c = 0
                            if row_change * column_change > 0:
                                if row_change < 0:
                                    for i in range(1, abs(row_change)):
                                        if self.get_board()[piece.get_position()[0] + i][
                                                piece.get_position()[1] + i] != 0:
                                            c += 1
                                    if c == 0:
                                        if move[2] == 'x':
                                            move_flag = self.capture_piece_from_adequate_square(
                                                piece, move, coordinates, other_pieces_d, b)
                                        else:
                                            move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
                                else:
                                    for i in range(1, abs(row_change)):
                                        if self.get_board()[piece.get_position()[0] - i][
                                                piece.get_position()[1] - i] != 0:
                                            c += 1
                                    if c == 0:
                                        if move[2] == 'x':
                                            move_flag = self.capture_piece_from_adequate_square(
                                                piece, move, coordinates, other_pieces_d, b)
                                        else:
                                            move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
                            elif row_change < 0:
                                for i in range(1, abs(row_change)):
                                    if self.get_board()[piece.get_position()[0] + i][piece.get_position()[1] - i] != 0:
                                        c += 1
                                if c == 0:
                                    if move[2] == 'x':
                                        move_flag = self.capture_piece_from_adequate_square(
                                            piece, move, coordinates, other_pieces_d, b)
                                    else:
                                        move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
                            elif column_change < 0:
                                for i in range(1, abs(row_change)):
                                    if self.get_board()[piece.get_position()[0] - i][piece.get_position()[1] + i] != 0:
                                        c += 1
                                if c == 0:
                                    if move[2] == 'x':
                                        move_flag = self.capture_piece_from_adequate_square(
                                            piece, move, coordinates, other_pieces_d, b)
                                    else:
                                        move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
        if move_flag == 0 and letter == 'B':
            print(f'Nie możesz wykonać ruchu {move}.')
            print(f'Zaproponuj inny ruch.')
        return move_flag

    def bishop_move(self, coordinates, move, letter):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
        else:
            piece_list = self.black.values()

        for piece in piece_list:
            if piece.get_name()[1] == letter and move_flag == 0:  # check if bish on adequate diagonal to move
                if abs(piece.get_position()[0] - coordinates[0]) == (abs(piece.get_position()[1] - coordinates[1])) \
                        and self.get_board()[coordinates[0]][coordinates[1]] == 0:
                    if abs(piece.get_position()[0] - coordinates[0]) == 1:
                        if len(move) > 3:
                            move_flag = self.move_piece_from_adequate_square(piece, coordinates, move)
                        else:
                            move_flag = self.normal_move(piece, coordinates)
                    elif abs(piece.get_position()[0] - coordinates[0]) > 1:
                        row_change = piece.get_position()[0] - coordinates[0]
                        column_change = piece.get_position()[1] - coordinates[1]
                        c = 0
                        if row_change * column_change > 0:
                            if row_change < 0:
                                for i in range(1, abs(row_change)):
                                    if self.get_board()[piece.get_position()[0] + i][piece.get_position()[1] + i] != 0:
                                        c += 1
                                if c == 0:
                                    if len(move) > 3:
                                        move_flag = self.move_piece_from_adequate_square(
                                            piece, coordinates, move)
                                    else:
                                        move_flag = self.normal_move(piece, coordinates)
                            else:
                                for i in range(1, abs(row_change)):
                                    if self.get_board()[piece.get_position()[0] - i][piece.get_position()[1] - i] != 0:
                                        c += 1
                                if c == 0:
                                    if len(move) > 3:
                                        move_flag = self.move_piece_from_adequate_square(
                                            piece, coordinates, move)
                                    else:
                                        move_flag = self.normal_move(piece, coordinates)
                        elif row_change < 0:
                            for i in range(1, abs(row_change)):
                                if self.get_board()[piece.get_position()[0] + i][piece.get_position()[1] - i] != 0:
                                    c += 1
                            if c == 0:
                                if len(move) > 3:
                                    move_flag = self.move_piece_from_adequate_square(
                                        piece, coordinates, move)
                                else:
                                    move_flag = self.normal_move(piece, coordinates)
                        elif column_change < 0:
                            for i in range(1, abs(row_change)):
                                if self.get_board()[piece.get_position()[0] - i][piece.get_position()[1] + i] != 0:
                                    c += 1
                            if c == 0:
                                if len(move) > 3:
                                    move_flag = self.move_piece_from_adequate_square(
                                        piece, coordinates, move)
                                else:
                                    move_flag = self.normal_move(piece, coordinates)
        if move_flag == 0 and letter == 'B':
            print(f'Nie możesz wykonać ruchu {move}.')
            print(f'Zaproponuj inny ruch.')
        return move_flag

    def rook_capture(self, coordinates, move, letter):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
            other_pieces_d = self.black
        else:  # black to move
            piece_list = self.black.values()
            other_pieces_d = self.white

        for piece in piece_list:  # check if rook
            if piece.get_name()[1] == letter and move_flag == 0:
                b = [i for i in other_pieces_d if other_pieces_d[i].get_position() == coordinates]
                if len(b) > 0:  # there is sth to capture
                    if piece.get_position()[0] == coordinates[0]:  # horizontal lines
                        change = piece.get_position()[1] - coordinates[1]
                        if change == 1 or change == -1:
                            if move[2] == 'x':
                                move_flag = self.capture_piece_from_adequate_square(
                                    piece, move, coordinates, other_pieces_d, b)
                            else:
                                move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
                        elif change > 1:
                            c = 0
                            for i in range(1, change):
                                if self.get_board()[piece.get_position()[0]][piece.get_position()[1] - i] != 0:
                                    c += 1
                            if c == 0:
                                if move[2] == 'x':
                                    move_flag = self.capture_piece_from_adequate_square(
                                        piece, move, coordinates, other_pieces_d, b)
                                else:
                                    move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
                        elif change < -1:
                            c = 0
                            for i in range(-1, change, -1):
                                if self.get_board()[piece.get_position()[0]][piece.get_position()[1] - i] != 0:
                                    c += 1
                            if c == 0:
                                if move[2] == 'x':
                                    move_flag = self.capture_piece_from_adequate_square(
                                        piece, move, coordinates, other_pieces_d, b)
                                else:
                                    move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)

                    elif piece.get_position()[1] == coordinates[1]:  # vertical lines
                        change = piece.get_position()[0] - coordinates[0]
                        if change == 1 or change == -1:
                            if move[2] == 'x':
                                move_flag = self.capture_piece_from_adequate_square(
                                    piece, move, coordinates, other_pieces_d, b)
                            else:
                                move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
                        elif change > 1:
                            c = 0
                            for i in range(1, change):
                                if self.get_board()[piece.get_position()[0] - i][piece.get_position()[1]] != 0:
                                    c += 1
                            if c == 0:
                                if move[2] == 'x':
                                    move_flag = self.capture_piece_from_adequate_square(
                                        piece, move, coordinates, other_pieces_d, b)
                                else:
                                    move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
                        elif change < -1:
                            c = 0
                            for i in range(-1, change, -1):
                                if self.get_board()[piece.get_position()[0] - i][piece.get_position()[1]] != 0:
                                    c += 1
                            if c == 0:
                                if move[2] == 'x':
                                    move_flag = self.capture_piece_from_adequate_square(
                                        piece, move, coordinates, other_pieces_d, b)
                                else:
                                    move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
        if move_flag == 0 and letter == 'R':
            print(f'Nie możesz wykonać ruchu {move}.')
            print(f'Zaproponuj inny ruch.')
        return move_flag

    def rook_move(self, coordinates, move, letter):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
        else:
            piece_list = self.black.values()

        for piece in piece_list:  # check if rook and free final square
            if piece.get_name()[1] == letter and self.get_board()[coordinates[0]][coordinates[1]] == 0 \
                    and move_flag == 0:

                if piece.get_position()[0] == coordinates[0]:  # horizontal lines
                    change = piece.get_position()[1] - coordinates[1]
                    if change == 1 or change == -1:
                        if len(move) > 3:
                            move_flag = self.move_piece_from_adequate_square(piece, coordinates, move)
                        else:
                            move_flag = self.normal_move(piece, coordinates)
                    elif change > 1:
                        c = 0
                        for i in range(1, change):
                            if self.get_board()[piece.get_position()[0]][piece.get_position()[1] - i] != 0:
                                c += 1
                        if c == 0:
                            if len(move) > 3:
                                move_flag = self.move_piece_from_adequate_square(piece, coordinates, move)
                            else:
                                move_flag = self.normal_move(piece, coordinates)
                    elif change < -1:
                        c = 0
                        for i in range(-1, change, -1):
                            if self.get_board()[piece.get_position()[0]][piece.get_position()[1] - i] != 0:
                                c += 1
                        if c == 0:
                            if len(move) > 3:
                                move_flag = self.move_piece_from_adequate_square(piece, coordinates, move)
                            else:
                                move_flag = self.normal_move(piece, coordinates)

                elif piece.get_position()[1] == coordinates[1]:  # vertical lines
                    change = piece.get_position()[0] - coordinates[0]
                    if change == 1 or change == -1:
                        if len(move) > 3:
                            move_flag = self.move_piece_from_adequate_square(piece, coordinates, move)
                        else:
                            move_flag = self.normal_move(piece, coordinates)
                    elif change > 1:
                        c = 0
                        for i in range(1, change):
                            if self.get_board()[piece.get_position()[0] - i][piece.get_position()[1]] != 0:
                                c += 1
                        if c == 0:
                            if len(move) > 3:
                                move_flag = self.move_piece_from_adequate_square(piece, coordinates, move)
                            else:
                                move_flag = self.normal_move(piece, coordinates)
                    elif change < -1:
                        c = 0
                        for i in range(-1, change, -1):
                            if self.get_board()[piece.get_position()[0] - i][piece.get_position()[1]] != 0:
                                c += 1
                        if c == 0:
                            if len(move) > 3:
                                move_flag = self.move_piece_from_adequate_square(piece, coordinates, move)
                            else:
                                move_flag = self.normal_move(piece, coordinates)
        if move_flag == 0 and letter == 'R':
            print(f'Nie możesz wykonać ruchu {move}.')
            print(f'Zaproponuj inny ruch.')
        return move_flag

    def king_capture(self, coordinates, move, king_moves):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
            other_pieces_d = self.black
        else:  # black to move
            piece_list = self.black.values()
            other_pieces_d = self.white

        for piece in piece_list:
            if piece.get_name()[1] == 'K':
                change = [piece.get_position()[0] - coordinates[0], piece.get_position()[1] - coordinates[1]]
                if change in king_moves:
                    b = [i for i in other_pieces_d if other_pieces_d[i].get_position() == coordinates]
                    if len(b) > 0:
                        move_flag = self.normal_capture(piece, coordinates, other_pieces_d, b)
        if move_flag == 0:
            print(f'Nie możesz wykonać bicia {move}.')
            print(f'Zaproponuj inny ruch.')

    def king_move(self, coordinates, move, king_moves):
        move_flag = 0
        if self.get_flag() == 1:  # white to move
            piece_list = self.white.values()
        else:
            piece_list = self.black.values()

        for piece in piece_list:
            if piece.get_name()[1] == "K":
                change = [piece.get_position()[0] - coordinates[0], piece.get_position()[1] - coordinates[1]]
                if change in king_moves and self.get_board()[coordinates[0]][coordinates[1]] == 0:
                    move_flag = self.normal_move(piece, coordinates)
        if move_flag == 0:
            print(f'Nie możesz wykonać ruchu {move}.')
            print(f'Zaproponuj inny ruch.')

    def castles(self, move):
        move_flag = 0
        if self.get_flag() == 1:
            piece_list = self.white.values()
            row = 0
        else:
            piece_list = self.black.values()
            row = 7

        for piece in piece_list:
            if piece.get_name()[1] == 'K' and piece.get_position()[1] == 4:
                if move == 'O-O' and self.get_board()[row][5] == 0 and self.get_board()[row][6] == 0:
                    for piece2 in piece_list:
                        if piece2.get_name()[1] == 'R' and piece2.get_position()[1] == 7:
                            self.short_castling(piece, piece2)
                            move_flag = 1
                elif move == 'O-O-O' and self.get_board()[row][1] == 0 and self.get_board()[row][2] == 0 and \
                        self.get_board()[row][3] == 0:
                    for piece2 in piece_list:
                        if piece2.get_name()[1] == 'R' and piece2.get_position()[1] == 0:
                            self.long_castling(piece, piece2)
                            move_flag = 1
        if move_flag == 0:
            print(f'Nie możesz wykonać roszady {move}.')
            print(f'Zaproponuj inny ruch.')

    def pawn_possible_moves(self, color):
        piece_list = []
        if color == 'white':
            piece_list = self.white.values()
            a = 1
        elif color == 'black':
            piece_list = self.black.values()
            a = -1
        moves = []

        for piece in piece_list:  # moves forward
            if piece.get_name()[1] == 'P':
                if self.get_board()[piece.get_position()[0] + a][piece.get_position()[1]] == 0:  # 1 square move
                    move = '{}{}'.format(get_chess_coordinates(piece.get_position()[1], piece.get_position()[0])[0],
                                         get_chess_coordinates(piece.get_position()[1], piece.get_position()[0])[1] + a)
                    moves.append(move)
                if 0 <= piece.get_position()[0] + a + a <= 7:
                    if self.get_board()[piece.get_position()[0] + a][piece.get_position()[1]] == 0 \
                            and self.get_board()[piece.get_position()[0] + a + a][piece.get_position()[1]] == 0 \
                            and (piece.get_position()[0] == 1 or piece.get_position()[0] == 6):  # 2 square move
                        move = '{}{}'.format(get_chess_coordinates(piece.get_position()[1], piece.get_position()[0])[0],
                                             get_chess_coordinates(piece.get_position()[1], piece.get_position()[0])[
                                                 1] + a + a)
                        moves.append(move)
                if piece.get_position()[0] + a in [0, 7]:  # promotion
                    for letter in ['Q', 'R', 'B', 'N']:
                        move = '{}{}{}{}'.format(get_chess_coordinates(piece.get_position()[1],
                                                                       piece.get_position()[0])[0],
                                                 get_chess_coordinates(piece.get_position()[1],
                                                                       piece.get_position()[0])[1] + a,
                                                 '=', letter)
                        moves.append(move)
                if 0 <= piece.get_position()[1] + 1 <= 7:  # captures(to the right)
                    cap_moves = self.format_pawn_capture(piece, a, 1, 'w', 'b')
                    if len(cap_moves) > 0:
                        for move in cap_moves:
                            moves.append(move)
                    cap_moves = self.format_pawn_capture(piece, a, 1, 'b', 'w')
                    if len(cap_moves) > 0:
                        for move in cap_moves:
                            moves.append(move)
                if 0 <= piece.get_position()[1] - 1 <= 7:  # captures(to the left)
                    cap_moves = self.format_pawn_capture(piece, a, -1, 'w', 'b')
                    if len(cap_moves) > 0:
                        for move in cap_moves:
                            moves.append(move)
                    cap_moves = self.format_pawn_capture(piece, a, -1, 'b', 'w')
                    if len(cap_moves) > 0:
                        for move in cap_moves:
                            moves.append(move)
        return moves

    def format_pawn_capture(self, piece, a, b, color1, color2):  # pawn, a(lower, higher according to pawn color, b - right,left cap)
        moves = []
        if piece.get_name()[0] == color1:
            if str(self.get_board()[piece.get_position()[0] + a][piece.get_position()[1] + b])[0] == color2:  # basic cap
                if piece.get_position()[0] + a in [0, 7]:  # promotion
                    for letter in ['Q', 'R', 'B', 'N']:
                        move = '{}{}{}{}{}{}'.format(get_chess_coordinates(piece.get_position()[1],
                                                                           piece.get_position()[0])[0],
                                                     'x', get_chess_coordinates(piece.get_position()[1] + b,
                                                                                piece.get_position()[0] + a)[0],
                                                     get_chess_coordinates(piece.get_position()[1],
                                                                           piece.get_position()[0] + a)[1],
                                                     '=', letter)
                        moves.append(move)
                move = '{}{}{}{}'.format(get_chess_coordinates(piece.get_position()[1],
                                                               piece.get_position()[0])[0],
                                         'x', get_chess_coordinates(piece.get_position()[1] + b,
                                                                    piece.get_position()[0] + a)[0],
                                         get_chess_coordinates(piece.get_position()[1],
                                                               piece.get_position()[0] + a)[1])
                moves.append(move)
            elif piece.get_position()[0] == 4 and color1 == 'w' and \
                    str(self.get_board()[piece.get_position()[0]][piece.get_position()[1] + b])[0] == color2:  # check if en passant
                other_pawn = [i for i in self.black if self.black[i].get_name()[1] == 'P'
                     and self.black[i].get_position() == [piece.get_position()[0], piece.get_position()[1] + b]]

                if len(other_pawn) > 0 and len(self.black[other_pawn[0]].get_prev_position()) > 0 and\
                        self.black[other_pawn[0]].get_prev_position()[0] == \
                        self.black[other_pawn[0]].get_position()[0] + a + a:
                    move = '{}{}{}{}'.format(get_chess_coordinates(piece.get_position()[1],
                                                                   piece.get_position()[0])[0],
                                             'x', get_chess_coordinates(piece.get_position()[1] + b,
                                                                        piece.get_position()[0] + a)[0],
                                             get_chess_coordinates(piece.get_position()[1],
                                                                   piece.get_position()[0] + a)[1])
                    moves.append(move)
            elif piece.get_position()[0] == 3 and color1 == 'b' and \
                    str(self.get_board()[piece.get_position()[0]][piece.get_position()[1] + b])[0] == color2:  # check if en passant
                other_pawn = [i for i in self.white if self.white[i].get_name()[1] == 'P'
                     and self.white[i].get_position() == [piece.get_position()[0], piece.get_position()[1] + b]]
                if len(other_pawn) > 0 and self.white[other_pawn[0]].get_prev_position()[0] == \
                        self.white[other_pawn[0]].get_position()[0] + a + a:
                    move = '{}{}{}{}'.format(get_chess_coordinates(piece.get_position()[1],
                                                                   piece.get_position()[0])[0],
                                             'x', get_chess_coordinates(piece.get_position()[1] + b,
                                                                        piece.get_position()[0] + a)[0],
                                             get_chess_coordinates(piece.get_position()[1],
                                                                   piece.get_position()[0] + a)[1])
                    moves.append(move)
        return moves

    def knight_possible_moves(self, color):
        if color == 'white':
            piece_list = self.white.values()
            color2 = 'b'
        else:
            piece_list = self.black.values()
            color2 = 'w'

        knight_moves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, 2], [1, -2], [2, 1], [2, -1]]
        tab = {}
        tab_caps = {}

        for piece in piece_list:  # moves forward
            if piece.get_name()[1] == 'N':
                moves = []
                captures = []
                for change in knight_moves:  # every possible move without capture
                    if 0 <= piece.get_position()[0]+change[0] <= 7 and 0 <= piece.get_position()[1]+change[1] <= 7:
                        if self.get_board()[piece.get_position()[0]+change[0]][piece.get_position()[1]+change[1]] == 0:
                            move = '{}{}{}'.format(piece.get_name()[1],
                                                   get_chess_coordinates(
                                                piece.get_position()[1]+change[1], piece.get_position()[0]+change[0])[0],
                                                get_chess_coordinates(
                                                    piece.get_position()[1]+change[1], piece.get_position()[0]+change[0])[1])
                            moves.append(move)
                        elif str(self.get_board()[piece.get_position()[0]+change[0]][piece.get_position()[1]+change[1]])[0] == color2:
                            capture = '{}{}{}{}'.format('N', 'x', get_chess_coordinates(
                                                piece.get_position()[1]+change[1], piece.get_position()[0]+change[0])[0],
                                                        get_chess_coordinates(piece.get_position()[1] + change[1],
                                                            piece.get_position()[0] + change[0])[1])
                            captures.append(capture)
                    tab[piece] = moves
                    tab_caps[piece] = captures

        ranking, tab, good_moves = rank_moves_and_coordinates(tab)
        cap_ranking, tab_caps, good_captures = rank_moves_and_coordinates(tab_caps)

        good_moves = format_multiple_knight_moves(ranking, tab, good_moves, 0)
        good_captures = format_multiple_knight_moves(cap_ranking, tab_caps, good_captures, 1)
        for i in range(len(good_captures)):
            good_moves.append(good_captures[i])

        return good_moves                        # also correct reading knights jumps if f.e. Ng3e2 cus rn it's only for Nge2

    def check_moves(self):
        if self.get_flag() == 1:
            m = self.pawn_possible_moves('white')
            print(f'Possible pawn moves: ', end='')
            print(*m, sep=', ')
            mn = self.knight_possible_moves('white')
            print(f'Possible knight moves: ', end='')
            print(*mn, sep=', ')
        # else:
        #     m = self.pawn_possible_moves('black')
        #     print(f'Possible pawn moves: ', end='')
        #     print(*m, sep=', ')

    def make_move(self, move):

        print("\n")
        print(f'Soldier! Order from your commander: {move}!')
        if move[0].isupper() is True:
            if move[0] == 'N':  # Knight
                knight_moves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, 2], [1, -2], [2, 1], [2, -1]]
                if move[1] == 'x' or move[2] == 'x':
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    self.knight_capture(coordinates, move, knight_moves)

                else:
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    self.knight_move(coordinates, move, knight_moves)
            elif move[0] == 'B':  # Bishop
                if move[1] == 'x' or move[2] == 'x':
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    self.bishop_capture(coordinates, move, "B")
                else:
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    self.bishop_move(coordinates, move, "B")
            elif move[0] == 'R':  # Rook
                if move[1] == 'x' or move[2] == 'x':
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    self.rook_capture(coordinates, move, "R")
                else:
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    self.rook_move(coordinates, move, "R")
            elif move[0] == 'Q':
                move_flag = 0
                if move[1] == 'x' or move[2] == 'x':
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    if move_flag == 0:
                        move_flag = self.bishop_capture(coordinates, move, "Q")
                    if move_flag == 0:
                        move_flag = self.rook_capture(coordinates, move, "Q")
                else:
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    if move_flag == 0:
                        move_flag = self.bishop_move(coordinates, move, "Q")
                    if move_flag == 0:
                        move_flag = self.rook_move(coordinates, move, "Q")
                if move_flag == 0:
                    print(f'Nie możesz wykonać ruchu {move}.')
                    print(f'Zaproponuj inny ruch.')
            elif move[0] == 'K':
                king_moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, 1], [1, 0], [1, -1]]
                if move[1] == 'x' or move[2] == 'x':
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    self.king_capture(coordinates, move, king_moves)

                else:
                    coordinates = get_board_list_coordinates(move[-2], move[-1])
                    coordinates.reverse()

                    self.king_move(coordinates, move, king_moves)
            elif move[0] == 'O':
                self.castles(move)

        elif move[0].islower() is True:  # pawns
            if move[1] == 'x':  # capture
                coordinates = get_board_list_coordinates(move[2], move[3])
                coordinates.reverse()
                first_coor = get_board_list_coordinates(move[0], 1)
                first_coor.reverse()

                self.pawn_capture(coordinates, first_coor, move)

            else:  # just pawn move
                coordinates = get_board_list_coordinates(move[0], move[1])
                coordinates.reverse()

                self.pawn_move(coordinates, move)
        else:
            print("Wrong command!!1!")
            return 0
        self.set_pieces()
        self.update_board()
        self.check_moves()

    def update_board(self):
        board = [[0] * 8 for i in range(8)]
        for piece in self.white.values():
            board[piece.get_position()[0]][piece.get_position()[1]] = piece.get_name()
        for piece in self.black.values():
            board[piece.get_position()[0]][piece.get_position()[1]] = piece.get_name()
        self.set_board(board)
        self.show_board()


class Piece:

    def __init__(self, name, position, color, val):
        self.__name = name
        self.__position = position
        self.__color = color
        self.__value = val
        self.__prev_position = []

    def get_name(self):
        return self.__color[0] + self.__name[0]

    def get_position(self):
        return self.__position

    def get_color(self):
        return self.__color

    def get_prev_position(self):
        return self.__prev_position

    def set_prev_position(self, coordinates):
        self.__prev_position = coordinates

    def change_position(self, coordinates):
        self.__position = coordinates


class Pawn(Piece):

    def __init__(self, position, color):
        super().__init__(__class__.__name__, position, color, 1)
        self.__possible_moves = []

    def promotion(self):
        return 0


class Bishop(Piece):

    def __init__(self, position, color):
        super().__init__(__class__.__name__, position, color, 3)
        self.__possible_moves = []


class NKnight(Piece):

    def __init__(self, position, color):
        super().__init__(__class__.__name__, position, color, 3)
        self.__possible_moves = []


class Rook(Piece):

    def __init__(self, position, color):
        super().__init__(__class__.__name__, position, color, 5)
        self.__possible_moves = []


class Queen(Piece):

    def __init__(self, position, color):
        super().__init__(__class__.__name__, position, color, 9)
        self.__possible_moves = []


class King(Piece):

    def __init__(self, position, color):
        super().__init__(__class__.__name__, position, color, 0)
        self.__possible_moves = []


def show(piece):  # działa dobrze
    print(f'{piece.get_color()} {piece.get_name()} on {transition_dict[piece.get_position()[1]]}'
          f'{transition_dict1[piece.get_position()[0]]} ')


def get_board_list_coordinates(x, y):
    a = [i for i in transition_dict if transition_dict[i] == x][0]
    b = [i for i in transition_dict1 if transition_dict1[i] == int(y)][0]
    return [int(a), int(b)]


def get_chess_coordinates(x, y):
    return [transition_dict[x], transition_dict1[y]]


def prepare_pieces():
    pieces_d = {}
    for i in range(8):
        pieces_d["pawn{}".format(i)] = Pawn([1, i], 'white')
        pieces_d["pawn{}".format(i + 8)] = Pawn([6, i], 'black')

    pieces_d.update(bishop1=Bishop([0, 2], 'white'), bishop2=Bishop([0, 5], 'white'))
    pieces_d.update(bishop3=Bishop([7, 2], 'black'), bishop4=Bishop([7, 5], 'black'))
    pieces_d.update(knight1=NKnight([0, 1], 'white'), knight2=NKnight([0, 6], 'white'))
    pieces_d.update(knight3=NKnight([7, 1], 'black'), knight4=NKnight([7, 6], 'black'))
    pieces_d.update(rook1=Rook([0, 0], 'white'), rook2=Rook([0, 7], 'white'))
    pieces_d.update(rook3=Rook([7, 0], 'black'), rook4=Rook([7, 7], 'black'))
    pieces_d.update(queen1=Queen([0, 3], 'white'), queen2=Queen([7, 3], 'black'))
    pieces_d.update(king1=King([0, 4], 'white'), king2=King([7, 4], 'black'))

    return pieces_d


def set_chessboard():
    pieces = prepare_pieces()
    board = Board(pieces)
    board.set_pieces_on_board()
    return board


def short_castles_test(board):
    board.make_move("e4")
    board.make_move("e5")
    board.make_move("Bc4")
    board.make_move("Be7")
    board.make_move("Nf3")
    board.make_move("Nf6")
    board.make_move("O-O")
    board.make_move("O-O")


def long_castles_test(board):
    board.make_move("e4")
    board.make_move("e5")
    board.make_move("Qe2")
    board.make_move("Nc6")
    board.make_move("Nc3")
    board.make_move("b6")
    board.make_move("b3")
    board.make_move("Bb7")
    board.make_move("Bb2")
    board.make_move("Qh4")
    board.make_move("O-O-O")
    board.make_move("O-O-O")


def print_hi(name):
    print(f'Hi, I am {name} \n')
    board = set_chessboard()
    board.sort_pieces()  # In future showing game moves on the right side of the board and maybe saving to pgn
    moves = ['e4', 'f5', 'exf5', 'g6', 'fxg6', 'Nf6', 'gxh7', 'Ng8',
             'hxg8=N', 'd6', 'Nf6', 'Kf7', 'Ne4', 'Bg4', 'Ng3', 'Be2', 'Nc3', 'Rh5']  # write moves in order once
    for move in moves:
        board.make_move(move)

    # c = str(input())  #write moves in console
    # moves = c.split(',')
    # for move in moves:
    #     board.make_move(move)

    # board.make_move("a4")
    # board.make_move("b5")
    # board.make_move("axb5")
    # board.make_move("a4")
    # board.make_move("Nf3")
    # board.make_move("e6")
    # board.make_move("d3")
    # board.make_move("exf5")
    # board.make_move("Nbd2")
    # board.make_move("Ne4")
    # board.make_move("Ng5")
    # board.make_move("h6")
    # board.make_move("Ndxe4")
    # board.make_move("0-0")
    for i in range(10):  # write 1 move at a time in console
        i = str(input())
        board.make_move(i)
    # for piece in board.get_pieces().values():
    #     if piece.get_name()[1] == 'P':
    #         print(piece.get_name(), piece.get_position())


if __name__ == '__main__':
    transition_dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}  # przejście na szachowy układ
    transition_dict1 = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}  # przejście na szachowy układ
    print_hi('PyChess')
