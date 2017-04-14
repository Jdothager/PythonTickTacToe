#   Tic-Tac-Toe         #
#   Dec 2016            #
#   by Jeremy Dothager  #
#########################
""" TODO:
    - add computer difficulty levels
    - implement GUI
    - add a score tracker... maybe write to a file? so that score can be stored when program is closed?
"""


from random import randrange, shuffle


class Square:
    """ objects to represent each square of the board"""
    def __init__(self):
        self.value = ' '
        self.filled = False

    def set_x(self):
        self.value = 'X'
        self.filled = True

    def set_o(self):
        self.value = 'O'
        self.filled = True


def init_squares():
    # returns a list of nine Square objects
    return [Square() for i in range(9)]


def print_board(sl):
    spacing = (' '*5 + '|')*2
    dash = '-'*18
    print('\n\n' + spacing)
    print('  ' + sl[0].value + '  |  ' + sl[1].value + '  |  ' + sl[2].value)
    print(spacing)
    print(dash)
    print(spacing)
    print('  ' + sl[3].value + '  |  ' + sl[4].value + '  |  ' + sl[5].value)
    print(spacing)
    print(dash)
    print(spacing)
    print('  ' + sl[6].value + '  |  ' + sl[7].value + '  |  ' + sl[8].value)
    print(spacing)
    return


def determine_first():
    order = randrange(2)
    if order == 1:
        return 'player'
    else:
        return 'comp'


def players_turn(sl):
    """ gets the players input, verify that it is a valid move by calling get_move()
        if valid: perform move and return True
        if not valid: return False
    """
    move = get_move()
    if move[0]:
        move = move[1]
    else:
        return False
    while sl[move-1].filled:
        print_board(sl)
        print('that spot is full')
        move = get_move()
    sl[move-1].set_x()
    return True


def get_move():
    """ returns a tuple: (bool, move)
        when bool = False return, signals to break out of main sequence and go to game_over()"""
    new = ['new', 'New', 'NEW', 'new game', 'New Game', 'NEW GAME']
    leave = ['exit', 'Exit', 'EXIT', 'e', 'E', 'Q', 'q', 'quit', 'Quit', 'QUIT']
    is_valid = False
    # continue asking until valid input is received
    while not is_valid:
        move = input('where do you want to go?:\n')
        if move in leave:
            exit()
        elif move in new:
            return False, 0
        elif len(move) == 1 and move.isdigit():
            if move != '0':
                is_valid = True
    # convert move position to button position on number pad
    move = int(move)
    if move == 1:
        move = 7
    elif move == 2:
        move = 8
    elif move == 3:
        move = 9
    elif move == 7:
        move = 1
    elif move == 8:
        move = 2
    elif move == 9:
        move = 3
    return True, move


def comps_turn(sl):
    # iterate through the squares and assign if game can be won this turn
    for square in sl:
        if not square.filled:
            square.set_o()
            if game_is_won(sl):
                return
            else:
                square.value = ' '
                square.filled = False
    # iterate through the squares and attempt to block the player from winning
    for square in sl:
        if not square.filled:
            square.set_x()
            if game_is_won(sl):
                square.set_o()
                return
            else:
                square.value = ' '
                square.filled = False
    # take center square if available
    if not sl[4].filled:
        sl[4].set_o()
        return
    # fill corner square if available at random
    corner_list = [0, 2, 6, 8]
    shuffle(corner_list)
    for corner in corner_list:
        if not sl[corner].filled:
            sl[corner].set_o()
            return
    # take remaining side spot at random
    side_list = [1, 3, 5, 7]
    shuffle(side_list)
    for side in side_list:
        if not sl[side].filled:
            sl[side].set_o()
            return


def game_is_won(sl):
    # check if either side has won
    if (sl[0].value == sl[1].value == sl[2].value == 'X' or sl[3].value == sl[4].value == sl[5].value == 'X' or
        sl[6].value == sl[7].value == sl[8].value == 'X' or sl[0].value == sl[3].value == sl[6].value == 'X' or
        sl[1].value == sl[4].value == sl[7].value == 'X' or sl[2].value == sl[5].value == sl[8].value == 'X' or
        sl[0].value == sl[4].value == sl[8].value == 'X' or sl[2].value == sl[4].value == sl[6].value == 'X' or
        sl[0].value == sl[1].value == sl[2].value == 'O' or sl[3].value == sl[4].value == sl[5].value == 'O' or
        sl[6].value == sl[7].value == sl[8].value == 'O' or sl[0].value == sl[3].value == sl[6].value == 'O' or
        sl[1].value == sl[4].value == sl[7].value == 'O' or sl[2].value == sl[5].value == sl[8].value == 'O' or
            sl[0].value == sl[4].value == sl[8].value == 'O' or sl[2].value == sl[4].value == sl[6].value == 'O'):
        return True
    else:
        return False


def board_is_full(sl):
    # logic to check if board is full
    for square in sl:
        if not square.filled:
            return False
    else:
        return True


def game_over():
    # ask to play again
    yes = ['y', 'Y', 'yes', 'YES', 'Yes', 'yeah', 'hells yeah', '']
    no = ['n', 'N', 'no', 'NO', 'No', 'nope']
    valid_answer = False
    print('Game Over')
    while not valid_answer:
        answer = input('Would you like to play again? y or n:\n')
        if answer in yes:
            return True
        elif answer in no:
            return False


def main():
    game_on = True
    while game_on:
        turn = determine_first()
        square_list = init_squares()
        print_board(square_list)
        while not game_is_won(square_list) and not board_is_full(square_list):
            if turn == 'player':
                # get player's move as well as check for exit signal
                if not players_turn(square_list):
                    break
                print_board(square_list)
                turn = 'comp'
            elif turn == 'comp':
                comps_turn(square_list)
                print_board(square_list)
                turn = 'player'
        # determine if it was a draw
        if not game_is_won(square_list) and board_is_full(square_list):
            turn = 'draw'
        # announce the winner
        if turn == 'comp':
            print('You have Won!')
        elif turn == 'player':
            print('The Computer has Won!')
        else:
            print('Draw')
        # ask to play again
        game_on = game_over()
    print('Bye!')


if __name__ == '__main__':
    main()
