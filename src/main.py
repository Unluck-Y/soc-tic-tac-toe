#!/usr/bin/python


from __future__ import annotations

import random
import time
from pathlib import Path
from tkinter import *
from typing import Callable, List


class Game:


    def __init__(self, buttons: List[Button], field: Field):

        self.l = [2]*9
        self.next = False

        self.buttons = buttons
        self.field = field
        self.imgs = [X, O]


    def place(self, coord: int):
        
        global bot_x, bot_o
        print(coord)

        self.l[coord] = int(self.next)
        self.buttons[coord].config(image = self.imgs[self.next], activebackground = self.buttons[coord]["background"], command = 0)

        if self.won() != 3:
            for button in self.buttons: button.config(command = 0, activebackground = button["background"])
            return

        self.next = not self.next

        if self.next and bot_o:
            bot(self, 1)
        elif not self.next and bot_x:
            bot(self, 0)


    def won(self) -> int:

        for i in range(3):
            if self.l[i] != 2 and self.l[i] == self.l[i+3] == self.l[i+6]: 
                for j in range(3): self.buttons[i + j*3].config(background = "red")
                return self.l[i]
            if self.l[i*3] != 2 and self.l[i*3] == self.l[i*3+1] == self.l[i*3+2]: 
                for j in range(3): self.buttons[i*3 + j].config(background = "red")
                return self.l[i*3]
        
        if self.l[0] != 2 and self.l[0] == self.l[4] == self.l[8]:
            for j in (0, 4, 8): self.buttons[j].config(background = "red")
            return self.l[0]
        if self.l[2] != 2 and self.l[2] == self.l[4] == self.l[6]:
            for j in (2, 4, 6): self.buttons[j].config(background = "red")
            return self.l[2]

        if all(i != 2 for i in self.l): return 2

        return 3


class Field(Frame):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.pack(fill = BOTH, expand = True)

        buttons = []
        lambdas = [
            lambda: self.game.place(0),
            lambda: self.game.place(1),
            lambda: self.game.place(2),
            lambda: self.game.place(3),
            lambda: self.game.place(4),
            lambda: self.game.place(5),
            lambda: self.game.place(6),
            lambda: self.game.place(7),
            lambda: self.game.place(8)
        ]

        self.game = Game(buttons = buttons, field = self)

        for i in range(9):

            button = Button(self, command = lambdas[i], height = 200, width = 200, image = PIXEL, relief = SUNKEN)
            button.place(x = i%3*200, y = i//3*200)
            buttons.append(button)

        self.new_game_button = Button(self, command = new_game, image = NEW_GAME, height = 50, width = 600, relief = SUNKEN)
        self.new_game_button.place(x = 0, y = 600)

        self.bot_as_x_button = Button(self, command = bot_as_x, image = BOT_AS_X, height = 50, width = 300, relief = SUNKEN)
        self.bot_as_x_button.place(x = 0, y = 650)
        if bot_x: self.bot_as_x_button.config(background = "dark gray")

        self.bot_as_o_button = Button(self, command = bot_as_o, image = BOT_AS_O, height = 50, width = 300, relief = SUNKEN)
        self.bot_as_o_button.place(x = 300, y = 650)
        if bot_o: self.bot_as_o_button.config(background = "dark gray")


def bot(game: Game, xo: int):

    l = game.l

    for _ in range(2):
        for i in range(3):
            if sorted([l[i], l[i+3], l[i+6]]) == [xo, xo, 2]:
                if l[i] == 2: return game.place(i)
                if l[i+3] == 2: return game.place(i+3)
                if l[i+6] == 2: return game.place(i+6)
            if sorted([l[i*3], l[i*3+1], l[i*3+2]]) == [xo, xo, 2]:
                if l[i*3] == 2: return game.place(i*3)
                if l[i*3+1] == 2: return game.place(i*3+1)
                if l[i*3+2] == 2: return game.place(i*3+2)

        if sorted([l[0], l[4], l[8]]) == [xo, xo, 2]: 
            if l[0] == 2: return game.place(0)
            if l[4] == 2: return game.place(4)
            if l[8] == 2: return game.place(8)
        if sorted([l[2], l[4], l[6]]) == [xo, xo, 2]: 
            if l[2] == 2: return game.place(2)
            if l[4] == 2: return game.place(4)
            if l[6] == 2: return game.place(6)

        xo = not xo

    if [l[i] for i in (0, 1, 2, 4, 7)].count(2) == 3 and [l[i] for i in (0, 1, 2, 4, 7)].count(xo) == 2: return game.place(2)
    if [l[i] for i in (2, 3, 4, 5, 8)].count(2) == 3 and [l[i] for i in (2, 3, 4, 5, 8)].count(xo) == 2: return game.place(5)
    if [l[i] for i in (1, 4, 6, 7, 8)].count(2) == 3 and [l[i] for i in (1, 4, 6, 7, 8)].count(xo) == 2: return game.place(7)
    if [l[i] for i in (0, 3, 4, 5, 6)].count(2) == 3 and [l[i] for i in (0, 3, 4, 5, 6)].count(xo) == 2: return game.place(3)

    if [l[i] for i in (0, 1, 2, 3, 6)].count(2) == 3 and [l[i] for i in (0, 1, 2, 3, 6)].count(xo) == 2: return game.place(0)
    if [l[i] for i in (0, 1, 2, 5, 8)].count(2) == 3 and [l[i] for i in (0, 1, 2, 5, 8)].count(xo) == 2: return game.place(2)
    if [l[i] for i in (0, 3, 6, 7, 8)].count(2) == 3 and [l[i] for i in (0, 3, 6, 7, 8)].count(xo) == 2: return game.place(6)
    if [l[i] for i in (2, 5, 6, 7, 8)].count(2) == 3 and [l[i] for i in (2, 5, 6, 7, 8)].count(xo) == 2: return game.place(8)

    if [l[i] for i in (0, 1, 4, 7, 8)].count(2) == 3 and [l[i] for i in (0, 1, 4, 7, 8)].count(xo) == 2: return game.place(4)
    if [l[i] for i in (1, 2, 4, 6, 7)].count(2) == 3 and [l[i] for i in (1, 2, 4, 6, 7)].count(xo) == 2: return game.place(4)
    if [l[i] for i in (0, 3, 4, 5, 8)].count(2) == 3 and [l[i] for i in (0, 3, 4, 5, 8)].count(xo) == 2: return game.place(4)
    if [l[i] for i in (2, 3, 4, 5, 6)].count(2) == 3 and [l[i] for i in (2, 3, 4, 5, 6)].count(xo) == 2: return game.place(4)

    if [l[i] for i in (0, 4, 8, 1, 2)].count(2) == 3 and [l[i] for i in (0, 4, 8, 1, 2)].count(xo) == 2: return game.place(0)
    if [l[i] for i in (0, 4, 8, 2, 5)].count(2) == 3 and [l[i] for i in (0, 4, 8, 2, 5)].count(xo) == 2: return game.place(8)
    if [l[i] for i in (0, 4, 8, 6, 7)].count(2) == 3 and [l[i] for i in (0, 4, 8, 6, 7)].count(xo) == 2: return game.place(8)
    if [l[i] for i in (0, 4, 8, 3, 6)].count(2) == 3 and [l[i] for i in (0, 4, 8, 3, 6)].count(xo) == 2: return game.place(0)

    if [l[i] for i in (2, 4, 6, 0, 1)].count(2) == 3 and [l[i] for i in (2, 4, 6, 0, 1)].count(xo) == 2: return game.place(2)
    if [l[i] for i in (2, 4, 6, 5, 8)].count(2) == 3 and [l[i] for i in (2, 4, 6, 5, 8)].count(xo) == 2: return game.place(2)
    if [l[i] for i in (2, 4, 6, 7, 8)].count(2) == 3 and [l[i] for i in (2, 4, 6, 7, 8)].count(xo) == 2: return game.place(6)
    if [l[i] for i in (2, 4, 6, 0, 3)].count(2) == 3 and [l[i] for i in (2, 4, 6, 0, 3)].count(xo) == 2: return game.place(6)

    if [l[i] for i in (0, 1, 2, 4, 7)].count(2) == 3 and [l[i] for i in (0, 1, 2, 4, 7)].count(not xo) == 2: return game.place(2)
    if [l[i] for i in (2, 3, 4, 5, 8)].count(2) == 3 and [l[i] for i in (2, 3, 4, 5, 8)].count(not xo) == 2: return game.place(5)
    if [l[i] for i in (1, 4, 6, 7, 8)].count(2) == 3 and [l[i] for i in (1, 4, 6, 7, 8)].count(not xo) == 2: return game.place(7)
    if [l[i] for i in (0, 3, 4, 5, 6)].count(2) == 3 and [l[i] for i in (0, 3, 4, 5, 6)].count(not xo) == 2: return game.place(3)

    if [l[i] for i in (0, 1, 2, 3, 6)].count(2) == 3 and [l[i] for i in (0, 1, 2, 3, 6)].count(not xo) == 2: return game.place(0)
    if [l[i] for i in (0, 1, 2, 5, 8)].count(2) == 3 and [l[i] for i in (0, 1, 2, 5, 8)].count(not xo) == 2: return game.place(2)
    if [l[i] for i in (0, 3, 6, 7, 8)].count(2) == 3 and [l[i] for i in (0, 3, 6, 7, 8)].count(not xo) == 2: return game.place(6)
    if [l[i] for i in (2, 5, 6, 7, 8)].count(2) == 3 and [l[i] for i in (2, 5, 6, 7, 8)].count(not xo) == 2: return game.place(8)

    if [l[i] for i in (0, 1, 4, 7, 8)].count(2) == 3 and [l[i] for i in (0, 1, 4, 7, 8)].count(not xo) == 2: return game.place(4)
    if [l[i] for i in (1, 2, 4, 6, 7)].count(2) == 3 and [l[i] for i in (1, 2, 4, 6, 7)].count(not xo) == 2: return game.place(4)
    if [l[i] for i in (0, 3, 4, 5, 8)].count(2) == 3 and [l[i] for i in (0, 3, 4, 5, 8)].count(not xo) == 2: return game.place(4)
    if [l[i] for i in (2, 3, 4, 5, 6)].count(2) == 3 and [l[i] for i in (2, 3, 4, 5, 6)].count(not xo) == 2: return game.place(4)

    if [l[i] for i in (0, 4, 8, 1, 2)].count(2) == 3 and [l[i] for i in (0, 4, 8, 1, 2)].count(not xo) == 2: return game.place(0)
    if [l[i] for i in (0, 4, 8, 2, 5)].count(2) == 3 and [l[i] for i in (0, 4, 8, 2, 5)].count(not xo) == 2: return game.place(8)
    if [l[i] for i in (0, 4, 8, 6, 7)].count(2) == 3 and [l[i] for i in (0, 4, 8, 6, 7)].count(not xo) == 2: return game.place(8)
    if [l[i] for i in (0, 4, 8, 3, 6)].count(2) == 3 and [l[i] for i in (0, 4, 8, 3, 6)].count(not xo) == 2: return game.place(0)

    if [l[i] for i in (2, 4, 6, 0, 1)].count(2) == 3 and [l[i] for i in (2, 4, 6, 0, 1)].count(not xo) == 2: return game.place(2)
    if [l[i] for i in (2, 4, 6, 5, 8)].count(2) == 3 and [l[i] for i in (2, 4, 6, 5, 8)].count(not xo) == 2: return game.place(2)
    if [l[i] for i in (2, 4, 6, 7, 8)].count(2) == 3 and [l[i] for i in (2, 4, 6, 7, 8)].count(not xo) == 2: return game.place(6)
    if [l[i] for i in (2, 4, 6, 0, 3)].count(2) == 3 and [l[i] for i in (2, 4, 6, 0, 3)].count(not xo) == 2: return game.place(6)

    if sum(l) == 18: return game.place(random.choice((0, 2, 4, 6, 8)))

    if sum(l) >= 16:
        if l[4] != 2: return game.place(random.choice((0, 2, 6, 8)))
        else: return game.place(4)

    return game.place(random.choice([i for i in range(9) if l[i] == 2]))


def new_game(first = False):

    global field

    if not first: field.destroy()

    field = Field()

    if bot_x: bot(field.game, 0)
# ne lehessen belenyúlni

def bot_as_x():

    global bot_x, DEFAULT_BG

    bot_x = not bot_x
    
    if bot_x: field.bot_as_x_button.config(background = "dark gray")
    else: field.bot_as_x_button.config(background = DEFAULT_BG)


def bot_as_o():

    global bot_o, DEFAULT_BG

    bot_o = not bot_o

    if bot_o: field.bot_as_o_button.config(background = "dark gray")
    else: field.bot_as_o_button.config(background = DEFAULT_BG)


def main():

    global DEFAULT_BG, X, O, NEW_GAME, BOT_AS_X, BOT_AS_O, PIXEL, bot_x, bot_o

    win = Tk()

    win.title("Tic Tac Toe")
    win.geometry("600x700")
    win.resizable(0, 0)

    imgs_path = f"{Path(__file__).parent.parent.resolve()}/imgs"

    DEFAULT_BG = win.cget('bg')
    X = PhotoImage(file = f"{imgs_path}/x.png")
    O = PhotoImage(file = f"{imgs_path}/o.png")
    NEW_GAME = PhotoImage(file = f"{imgs_path}/new_game.png")
    BOT_AS_X = PhotoImage(file = f"{imgs_path}/bot_as_x.png")
    BOT_AS_O = PhotoImage(file = f"{imgs_path}/bot_as_o.png")
    PIXEL = PhotoImage(width = 1, height = 1)
    bot_x = False
    bot_o = False

    new_game(first = True)

    win.mainloop()


if __name__ == "__main__":
    main()
