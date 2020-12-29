# write your code here
import random
import sys

SCORE = 'score'
FUNCTION = 'function'
COMPARE = 'compare'
INIT_BEST_CHOICE = 'init_best_choice'
DRAW = 'draw'
SPACE = ' '


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
            self.game_table[val] = SPACE

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
        if winner != SPACE:
            self.state = winner + ' wins'
            raise WinFound(winner)
        count_ = len({k: v for k, v in self.game_table.items() if v == SPACE})
        if count_ == 0:
            self.state = 'Draw'

    def which_move(self):
        count_x = len({k: v for k, v in self.game_table.items() if v == 'X'})
        count_o = len({k: v for k, v in self.game_table.items() if v == 'O'})

        if count_x <= count_o:
            return 'X'

        return 'O'

    @staticmethod
    def result_measure(role):
        res_dict = {'X': {FUNCTION:         min,
                          SCORE:            -10,
                          COMPARE:          lambda x, y: x < y,
                          INIT_BEST_CHOICE: sys.maxsize,
                          DRAW:             0,
                          },
                    'O': {FUNCTION:         max,
                          SCORE:            10,
                          COMPARE:          lambda x, y: x > y,
                          INIT_BEST_CHOICE: -sys.maxsize,
                          DRAW:             0,
                          },
                    }
        return res_dict[role]

    def minimax(self, role):

        moves_space = {k: v for k, v in self.game_table.items() if v == SPACE}

        if len(moves_space) >= (self.dimension * self.dimension - 3):
            random.seed(self.dimension * self.dimension)
            return 0, self.random_choice()

        result_function = self.result_measure(role)
        best_choice = result_function[INIT_BEST_CHOICE]
        best_choice_move = None
        choice_dict = {}

        for move in moves_space:
            self.game_table[move] = role

            if self.check_draw():
                self.game_table[move] = SPACE
                choice_dict[move] = result_function[DRAW]
                continue

            win_role = self.check_win()
            if win_role == role:
                self.game_table[move] = SPACE
                choice_dict[move] = result_function[SCORE]
                continue

            if win_role == 'XO'.replace(role, ''):
                self.game_table[move] = SPACE
                choice_dict[move] = self.result_measure('XO'.replace(role, ''))[SCORE] * 10
                continue

            if win_role == SPACE:
                choice, choice_move = self.minimax('XO'.replace(role, ''))
                choice_dict[choice_move] = choice

            self.game_table[move] = SPACE

        for item, val in choice_dict.items():
            if result_function[COMPARE](val, best_choice):
                best_choice_move = item
                best_choice = val

        return best_choice, best_choice_move

    def find_next_move(self, role):
        next_moves = {'X': [], 'O': [], }
        for player in 'XO':
            wind = 0
            winnd = 0
            wind_pos = None
            winnd_pos = None

            for i in range(1, self.dimension + 1):

                if self.game_table[(i, i)] == player:
                    wind += 1
                elif self.game_table[(i, i)] == SPACE:
                    wind_pos = (i, i)
                else:
                    wind = 0
                    wind_pos = None

                if wind == (self.dimension - 1) and (not wind_pos is None):
                    next_moves[player].append(wind_pos)

                if self.game_table[(i, self.dimension - i + 1)] == player:
                    winnd += 1
                elif self.game_table[(i, self.dimension - i + 1)] == SPACE:
                    winnd_pos = (i, self.dimension - i + 1)
                else:
                    winnd = 0
                    winnd_pos = None

                if winnd == (self.dimension - 1) and (not winnd_pos is None):
                    next_moves[player].append(winnd_pos)

                winh = 0
                winv = 0
                winh_pos = None
                winv_pos = None

                for j in range(1, self.dimension + 1):

                    if self.game_table[(i, j)] == player:
                        winh += 1
                    elif self.game_table[(i, j)] == SPACE:
                        winh_pos = (i, j)
                    else:
                        winh = 0
                        winh_pos = None

                    if winh == (self.dimension - 1) and (not winh_pos is None):
                        next_moves[player].append(winh_pos)

                    if self.game_table[(j, i)] == player:
                        winv += 1
                    elif self.game_table[(j, i)] == SPACE:
                        winv_pos = (j, i)
                    else:
                        winv = 0
                        winv_pos = None

                    if winv == (self.dimension - 1) and (not winv_pos is None):
                        next_moves[player].append(winv_pos)

        if len(next_moves[role]) > 0:
            return next_moves[role][0]

        opponent_role = 'XO'.replace(role, '')

        if len(next_moves[opponent_role]) > 0:
            return next_moves[opponent_role][0]

        center_pos = (2, 2)
        if self.game_table[center_pos] == ' ':
            return center_pos

        return self.random_choice()

    def check_draw(self):
        return len({k: v for k, v in self.game_table.items() if v == SPACE}) < 1

    def check_win(self):
        for player in 'XO':
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

                winh = 0
                winv = 0
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
        return SPACE

    def computer_move(self, level=None, role=None):
        if level is None:
            level = "easy"
        if role is None:
            role = 'O'

        move_pos = None

        if self.state == 'Draw':
            return
        if level == 'easy':
            move_pos = self.random_choice()
        elif level == 'medium':
            move_pos = self.find_next_move(role)
        elif level == 'hard':
            # move_pos = self.minimax(role)[1]
            # move_pos = self.random_choice()
            move_pos = self.find_next_move(role)
        self.game_table[move_pos] = role
        print(f'Making move level "{level}"')
        self.set_state()
        self.print_game_table()

    def random_choice(self):
        random.seed()
        move_pos = random.choice(list(k for k, v in self.game_table.items() if v == ' '))
        return move_pos

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
    # game = TicTacToe('XXOOXXXOO', dimension=3)
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
            enabled_users_list = ['easy', 'medium', 'hard', 'user', ]
            if playerX not in enabled_users_list:
                print('Bad parameters!')
                continue

            playerO = command.split()[2]
            if playerO not in enabled_users_list:
                print('Bad parameters!')
                continue

            game_with_opponent(playerX, playerO, dimension=3)
