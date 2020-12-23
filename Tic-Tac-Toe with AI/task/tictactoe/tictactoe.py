# write your code here
import random


class TicTacToeException(Exception):
    pass


class WrongCoordinatesFormat(TicTacToeException):
    def __str__(self):
        # return 'Coordinates should be two digits separated by space'
        return 'You should enter numbers!'


class CoordinatesShouldBeNumbers(TicTacToeException):
    def __str__(self):
        return 'You should enter numbers!'


class CoordinatesShouldBeFrom1To3(TicTacToeException):
    def __str__(self):
        return 'Coordinates should be from 1 to 3!'


class ThisCellIsOccupied(TicTacToeException):
    def __str__(self):
        return 'This cell is occupied! Choose another one!'


class WinFound(TicTacToeException):
    def __init__(self, winner):
        self.win = winner

    def __str__(self):
        return self.win + ' wins'


def raise_exception(number):
    if not number.isdigit():
        raise CoordinatesShouldBeNumbers

    if number not in '123':
        raise CoordinatesShouldBeFrom1To3


class TicTacToe:
    game_table = {(1, 1): " ", (1, 2): " ", (1, 3): " ",
                  (2, 1): " ", (2, 2): " ", (2, 3): " ",
                  (3, 1): " ", (3, 2): " ", (3, 3): " ", }
    start_pos_indexes = {0: (1, 1), 1: (1, 2), 2: (1, 3),
                         3: (2, 1), 4: (2, 2), 5: (2, 3),
                         6: (3, 1), 7: (3, 2), 8: (3, 3), }

    def __init__(self, start_position):
        if len(start_position) == 0:
            return

        for index, symbol in enumerate(start_position.upper()):
            if symbol == '_':
                continue

            if symbol == 'X':
                self.game_table[self.start_pos_indexes[index]] = 'X'

            if symbol == 'O':
                self.game_table[self.start_pos_indexes[index]] = 'O'

        self.set_state()
        self.print_game_table()

    def set_state(self):
        self.state = 'Game not finished'
        winner = self.check_win()
        if winner != ' ':
            self.state = winner + ' wins'
            raise WinFound(winner)
        count_ = len({k: v for k, v in self.game_table.items() if v == ' '})
        if count_ == 0:
            self.state = 'Draw'

    def which_move(self):
        count_x = len({k: v for k, v in self.game_table.items() if v == 'X'})
        count_o = len({k: v for k, v in self.game_table.items() if v == 'O'})

        if count_x <= count_o:
            return 'X'

        return 'O'

    def check_win(self):
        if self.game_table[(1, 1)] == self.game_table[(1, 2)] == self.game_table[(1, 3)]:
            return self.game_table[(1, 1)]
        if self.game_table[(2, 1)] == self.game_table[(2, 2)] == self.game_table[(2, 3)]:
            return self.game_table[(2, 1)]
        if self.game_table[(3, 1)] == self.game_table[(3, 2)] == self.game_table[(3, 3)]:
            return self.game_table[(3, 1)]

        if self.game_table[(1, 1)] == self.game_table[(2, 1)] == self.game_table[(3, 1)]:
            return self.game_table[(1, 1)]
        if self.game_table[(1, 2)] == self.game_table[(2, 2)] == self.game_table[(3, 3)]:
            return self.game_table[(1, 2)]
        if self.game_table[(1, 3)] == self.game_table[(2, 3)] == self.game_table[(3, 3)]:
            return self.game_table[(1, 3)]

        if self.game_table[(1, 1)] == self.game_table[(2, 2)] == self.game_table[(3, 3)]:
            return self.game_table[(1, 1)]
        if self.game_table[(3, 1)] == self.game_table[(2, 2)] == self.game_table[(1, 3)]:
            return self.game_table[(3, 1)]
        return ' '

    def computer_move(self, level=None):
        if level is None:
            level = "easy"
            random.seed()
        move_pos = random.choice(list(k for k, v in self.game_table.items() if v == ' '))
        self.game_table[move_pos] = 'O'
        print(f'Making move level "{level}"')
        self.print_game_table()
        self.set_state()

    def next_move(self, move_string):
        move_list = move_string.split()
        if len(move_list) != 2:
            raise WrongCoordinatesFormat
        coordinates = tuple(map(lambda x: int(x) if x in '123' else raise_exception(x), move_list))
        if self.game_table[coordinates] != ' ':
            raise ThisCellIsOccupied
        self.game_table[coordinates] = self.which_move()
        self.set_state()
        self.print_game_table()

    def print_game_table(self):
        print('-' * 9)
        for i in range(1, 4):
            print(f'| {self.game_table[(i, 1)]} {self.game_table[(i, 2)]} {self.game_table[(i, 3)]} |')
        print('-' * 9)


if __name__ == '__main__':
    # start_position = input("Enter the cells: >")
    start_position = '_________'
    try:
        game = TicTacToe(start_position)
    except WinFound as e:
        print(e)
        exit(0)
    while True:
        try:
            game.next_move(input('Enter the coordinates: >'))
            # print(game.state)
            game.computer_move()
        except WinFound as e:
            game.print_game_table()
            print(e)
            # print('Making move level "Easy"')
            break
        except TicTacToeException as e:
            print(e)
