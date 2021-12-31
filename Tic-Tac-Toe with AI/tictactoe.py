import random
import re
import sys
import copy


class TicTacToe:
    def __init__(self):
        self._player = 'X'
        self._game_board = [[' ' for _ in range(3)] for _ in range(3)]

    def _print_board(self):
        print('---------')
        for row in self._game_board:
            print('| ' + ' '.join(s for s in row) + ' |')
        print('---------')

    def _check_input(self, coord):
        if len(coord.split()) == 1 or len(coord.split()) > 2:
            print('You should enter numbers!')
            return False
        row, column = coord.split()
        if not row.isnumeric() or not column.isnumeric():
            print('You should enter numbers!')
            return False
        if int(row) not in range(1, 4) or int(column) not in range(1, 4):
            print('Coordinates should be from 1 to 3!')
            return False
        if self._game_board[int(row) - 1][int(column) - 1] != ' ':
            print('This cell is occupied! Choose another one!')
            return False
        return True

    def game_status(self, game_board):
        for side in ('X', 'O'):
            for i in range(3):
                horizontal = True
                vertical = True
                for j in range(3):
                    horizontal = horizontal and game_board[i][j] == side
                    vertical = vertical and game_board[j][i] == side
                if horizontal or vertical:
                    return f'{side} wins'

            right_diagonal = True
            left_diagonal = True
            for i, j in zip(range(3), reversed(range(3))):
                right_diagonal = right_diagonal and game_board[i][i] == side
                left_diagonal = left_diagonal and game_board[i][j] == side
            if right_diagonal or left_diagonal:
                return f'{side} wins'

        return 'Draw' if (sum(c.count(' ') for c in game_board)) == 0 else 'next'

    def _swap_side(self):
        self._player = 'O' if self._player == 'X' else 'X'

    def _move_player(self):
        while True:
            coord = input('Enter the coordinates:')
            if self._check_input(coord):
                self._game_board[int(coord[0]) - 1][int(coord[-1]) - 1] = self._player
                break

    def _easy_AI(self):
        while True:
            row = random.randint(0, 2)
            column = random.randint(0, 2)
            if self._game_board[row][column] == ' ':
                self._game_board[row][column] = self._player
                break

    def _move_AI(self, level):
        if level == 'easy':
            self._easy_AI()
            return

        temp_board = copy.deepcopy(self._game_board)
        evaluation_results = dict()
        for i in range(3):
            for j in range(3):
                if temp_board[i][j] == ' ':
                    for side in ('X', 'O'):
                        temp_board[i][j] = side
                        evaluation_results.setdefault((i, j), 0)
                        if self.game_status(temp_board) == 'X wins':
                            evaluation_results[(i, j)] += 10 if self._player == 'X' else 20
                        elif self.game_status(temp_board) == 'O wins':
                            evaluation_results[(i, j)] += 10 if self._player == 'O' else 20
                        temp_board[i][j] = ' '

        if level == 'medium' and sum(evaluation_results.values()) == 0:
            self._easy_AI()
            return
        if level == 'hard' and self._game_board[1][1] == ' ':
            self._game_board[1][1] = self._player
            return

        row, column = max(evaluation_results, key=evaluation_results.get)
        self._game_board[row][column] = self._player

    def _command_menu(self):
        while True:
            command = input('Input command:')
            if command == 'exit':
                sys.exit(0)
            elif re.match('start (easy|user|medium|hard) (easy|user|medium|hard)', command):
                return command.split()[1:]
            else:
                print('Bad parameters!')

    def start(self):
        while True:
            first_player, second_player = self._command_menu()
            if first_player == 'user':
                self._print_board()

            game_status = 'next'
            while game_status == 'next':
                for player in (first_player, second_player):
                    if player == 'user':
                        self._move_player()
                    elif player == 'easy':
                        print('Making move level "easy"')
                        self._move_AI('easy')
                    elif player == 'medium':
                        print('Making move level "medium"')
                        self._move_AI('medium')
                    elif player == 'hard':
                        print('Making move level "hard"')
                        self._move_AI('hard')
                    self._swap_side()
                    self._print_board()

                    game_status = self.game_status(self._game_board)
                    if game_status != 'next':
                        print(game_status + '\n')
                        break


if __name__ == '__main__':
    TicTacToe().start()
