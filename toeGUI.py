#   Tic-Tac-Toe         #
#   Dec 2016            #
#   by Jeremy Dothager  #
#########################

from tkinter import Tk, Menu, PhotoImage, Button
from toe import init_squares, determine_first, board_is_full
from random import shuffle, randrange
from sys import exit

""" TODO:
    - add score keeper
"""


class MyGUI:

    def __init__(self, master):
        self.master = master
        # title at top of window
        master.title('Tic-Tac-Toe')
        # variables
        self.turn = str
        self.difficulty = 'easy'
        self.square_list = []
        self.button_list = []
        self.winning_squares_list = []
        self.corner_side_list = [[0, 2, 6, 8], [1, 3, 5, 7]]
        self.win_condition_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                                   [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.x_image = PhotoImage(file='X.png')
        self.x_win_image = PhotoImage(file='X_win.png')
        self.o_image = PhotoImage(file='O.png')
        self.o_win_image = PhotoImage(file='O_win.png')
        self.no_image = PhotoImage(file='empty.png')
        # setup
        self.init_menu()
        self.center_window()
        self.master.grid_columnconfigure(index=0, pad=130)
        self.master.grid_rowconfigure(index=0, pad=30)
        # create the buttons
        self.reset_button = Button(self.master, text='Reset', command=self.reset)
        self.create_buttons()
        # begin the game
        self.reset()

    def center_window(self):
        """ set the size of the window and center it"""
        width = 600
        height = 500
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) / 2
        y = (screen_height - height) / 2
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def init_menu(self):
        """ setup the menus"""
        bar_menu = Menu(self.master)
        self.master.config(menu=bar_menu)
        # add a file button to the menu
        file_menu = Menu(bar_menu, tearoff=0)
        file_menu.add_command(label='Reset', command=self.reset)
        file_menu.add_command(label='Exit', command=exit)
        # add a game button to the menu
        game_menu = Menu(bar_menu, tearoff=0)
        level_menu = Menu(bar_menu, tearoff=0)
        level_menu.add_command(label='Easy', command=self.diff_easy)
        level_menu.add_command(label='Hard', command=self.diff_hard)
        # set all menus to the top bar menu
        bar_menu.add_cascade(label='File', menu=file_menu)
        bar_menu.add_cascade(label='Game', menu=game_menu)
        game_menu.add_cascade(label='Difficulty', menu=level_menu)

    def create_buttons(self):
        """ create the buttons and layout, store into self.button_list"""
        # create the buttons
        for i in range(9):
            b = Button(self.master, image=self.no_image, command=lambda j=i: self.button_action(j))
            self.button_list.append(b)
        # button layout
        self.button_list[0].grid(column=0, row=0, sticky='es')
        self.button_list[1].grid(column=1, row=0, sticky='s')
        self.button_list[2].grid(column=2, row=0, sticky='s')
        self.button_list[3].grid(column=0, row=1, sticky='e')
        self.button_list[4].grid(column=1, row=1)
        self.button_list[5].grid(column=2, row=1)
        self.button_list[6].grid(column=0, row=2, sticky='e')
        self.button_list[7].grid(column=1, row=2)
        self.button_list[8].grid(column=2, row=2)
        self.reset_button.grid(column=1, row=3, pady=25, ipadx=25, ipady=25)

    def diff_easy(self):
        """ easy mode"""
        self.difficulty = 'easy'
        self.reset()

    def diff_hard(self):
        """ hard mode"""
        self.difficulty = 'hard'
        self.reset()

    def clear_buttons(self):
        """ assign each square button no_image"""
        for each in self.button_list:
            each.config(image=self.no_image)

    def game_is_won(self):
        """ check for win condition and return a bool and list of winning squares: bool, list"""
        # check if either side has won
        for idx in self.win_condition_list:
            if all(i in 'X' for i in
                   (self.square_list[idx[0]].value, self.square_list[idx[1]].value, self.square_list[idx[2]].value)):
                return True, idx
            elif all(i in 'O' for i in
                     (self.square_list[idx[0]].value, self.square_list[idx[1]].value, self.square_list[idx[2]].value)):
                return True, idx
        return False, []

    def winning_squares(self):
        """ highlight the winning squares"""
        # check for win condition
        if self.game_is_won()[0]:
            for each in self.game_is_won()[1]:
                if self.turn == 'comp':
                    self.button_list[each].config(image=self.o_win_image)
                else:
                    self.button_list[each].config(image=self.x_win_image)

    def button_action(self, button):
        """ determines if player input is valid"""
        if self.turn == 'player' and not self.game_is_won()[0] and not self.square_list[button].filled:
            self.square_list[button].set_x()
            self.button_list[button].config(image=self.x_image)
            # check for win condition
            self.winning_squares()
            # pass the turn to the computer
            self.turn = 'comp'
            self.computer_turn()

    def computer_turn(self):
        """ computer's play logic"""
        if not self.game_is_won()[0] and not board_is_full(self.square_list):
            # if easy mode, make random move
            if self.difficulty == 'easy':
                thinking = True
                while thinking:
                    square = randrange(9)
                    if not self.square_list[square].filled:
                        thinking = False
                        self.set_check(square)
            else:
                # attempt to win or to block the player win
                if self.win_or_block():
                    return
                # take center square if available
                if not self.square_list[4].filled:
                    self.set_check(4)
                    return
                # take a corner at random, otherwise take a random side
                shuffle(self.corner_side_list[0])
                shuffle(self.corner_side_list[1])
                for i in (0, 1):
                    for j in (0, 1, 2, 3):
                        if not self.square_list[self.corner_side_list[i][j]].filled:
                            self.set_check(self.corner_side_list[i][j])
                            return

    def set_check(self, square):
        """ helper for self.computer_turn"""
        # set the square
        self.square_list[square].set_o()
        # change the image
        self.button_list[square].config(image=self.o_image)
        # check for win
        self.winning_squares()
        # pass the turn
        self.turn = 'player'

    def win_or_block(self):
        """ helper for self.computer_turn, check for the win/block. return True if move was made, False if not"""
        for counter in (0, 1):
            for index in range(len(self.square_list)):
                if not self.square_list[index].filled:
                    if counter == 0:
                        self.square_list[index].set_o()
                    else:
                        self.square_list[index].set_x()
                    if self.game_is_won()[0]:
                        self.set_check(index)
                        return True
                    else:
                        self.square_list[index].value = ' '
                        self.square_list[index].filled = False
        return False

    def reset(self):
        """ start a new game"""
        self.clear_buttons()
        self.square_list = init_squares()
        self.turn = determine_first()
        if self.turn == 'comp':
            self.computer_turn()


def main():
    root = Tk()
    my_gui = MyGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
