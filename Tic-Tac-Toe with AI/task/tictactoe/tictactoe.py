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

    def __init__(self, start_position, **kwargs):
        self.dimension = 3
        if 'dimension' in kwargs:
            self.dimension = kwargs['dimension']

        self.start_pos_indexes = {}
        self.generate_start_pos_indexes()
        self.game_table = {}
        self.generate_game_table()
        if len(start_position) == 0:
            return
        self.fill_start_pos(start_position)

    def generate_start_pos_indexes(self):
        count = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.start_pos_indexes[count] = (i + 1, j + 1)
                count += 1

    def generate_game_table(self):
        for val in self.start_pos_indexes.values():
            self.game_table[val] = ' '

    def fill_start_pos(self, start_position):
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
        for player in 'XO':
            winh = 0
            winv = 0
            wind = 0
            winnd = 0

            for i in range(1, self.dimension + 1):

                if self.game_table[(i, i)] == player:
                    wind += 1
                else:
                    wind = 0

                if wind == self.dimension:
                    return player

                if self.game_table[(i, self.dimension - i + 1)] == player:
                    winnd += 1
                else:
                    winnd = 0

                if winnd == self.dimension:
                    return player

                for j in range(1, self.dimension + 1):

                    if self.game_table[(i, j)] == player:
                        winh += 1
                    else:
                        winh = 0

                    if winh == self.dimension:
                        return player

                    if self.game_table[(j, i)] == player:
                        winv += 1
                    else:
                        winv = 0

                    if winv == self.dimension:
                        return player
        return ' '

    def computer_move(self, level=None, role=None):
        if level is None:
            level = "easy"
        if role is None:
            role = 'O'

        if self.state == 'Draw':
            return

        random.seed()
        move_pos = random.choice(list(k for k, v in self.game_table.items() if v == ' '))
        self.game_table[move_pos] = role
        print(f'Making move level "{level}"')
        self.set_state()
        self.print_game_table()

    def next_move(self, move_string, role=None):
        move_list = move_string.split()
        if len(move_list) != 2:
            raise WrongCoordinatesFormat
        coordinates = tuple(map(lambda x: int(x) if x in '123' else raise_exception(x), move_list))
        if self.game_table[coordinates] != ' ':
            raise ThisCellIsOccupied
        self.game_table[coordinates] = role
        if role is None:
            self.game_table[coordinates] = self.which_move()
        self.set_state()
        self.print_game_table()

    def print_game_table(self):
        print('-' * (self.dimension * 2 + 3))
        for i in range(1, self.dimension + 1):
            print('|', end=' ')
            for j in range(1, self.dimension + 1):
                print(f'{self.game_table[(i, j)]}', end=' ')
            print('|')
        print('-' * (self.dimension * 2 + 3))


def game_with_opponent(player_x, player_o, **kwargs):
    dimension = 3
    if 'dimension' in kwargs:
        dimension = kwargs['dimension']
    start_position = '_' * dimension
    try:
        game = TicTacToe(start_position, dimension=dimension)
    except WinFound as e:
        print(e)
        return
    while True:
        try:
            if player_x == 'user':
                game.next_move(input('Enter the coordinates: >'))
            else:
                game.computer_move(level=player_x, role='X')
            # print(game.state)
            if game.state == 'Draw':
                print(game.state)
                break
            if player_o == 'user':
                game.next_move(input('Enter the coordinates: >'))
            else:
                game.computer_move(level=player_o, role='O')
            if game.state == 'Draw':
                print(game.state)
                break
        except WinFound as e:
            game.print_game_table()
            print(e)
            # print('Making move level "Easy"')
            break
        except TicTacToeException as e:
            print(e)


if __name__ == '__main__':
    # start_position = input("Enter the cells: >")
    while True:
        command = input('Input command: >').lower()
        if command == 'exit':
            break
        if 'start' in command:
            if len(command.split()) != 3:
                print('Bad parameters!')
                continue
            playerX = command.split()[1]
            enabled_users_list = ['easy', 'user', ]
            if playerX not in enabled_users_list:
                print('Bad parameters!')
                continue

            playerO = command.split()[2]
            if playerO not in enabled_users_list:
                print('Bad parameters!')
                continue

            game_with_opponent(playerX, playerO, dimension=5)
