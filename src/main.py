#!/usr/bin/python


from __future__ import annotations

from tkinter import *
from typing import List
from pathlib import Path


class Game:


    def __init__(self, buttons: List[Button], field: Field):

        self.l = [2]*9
        self.next = False

        self.buttons = buttons
        self.field = field
        self.imgs = [X, O]


    def place(self, coord: int):
        
        self.l[coord] = int(self.next)
        self.buttons[coord].config(image = self.imgs[self.next], activebackground = self.buttons[coord]["background"], command = 0)

        if self.won() != 3:
            for button in self.buttons: button.config(command = 0, activebackground = button["background"])

        self.next = not self.next


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

        self.new_game_button = Button(self, command = new_game, text = "New game", image = NEW_GAME, height = 50, width = 600, relief = SUNKEN)
        self.new_game_button.place(x = 0, y = 600)


def new_game(first = False):

    global field

    if not first: field.destroy()

    field = Field()


def main():

    global X, O, NEW_GAME, PIXEL

    win = Tk()

    win.title("Tic Tac Toe")
    win.geometry("600x650")
    win.resizable(0, 0)

    imgs_path = f"{Path(__file__).parent.parent.resolve()}/imgs"

    X = PhotoImage(file = f"{imgs_path}/x.png")
    O = PhotoImage(file = f"{imgs_path}/o.png")
    NEW_GAME = PhotoImage(file = f"{imgs_path}/new_game.png")
    PIXEL = PhotoImage(width = 1, height = 1)

    new_game(first = True)

    win.mainloop()


if __name__ == "__main__":
    main()
