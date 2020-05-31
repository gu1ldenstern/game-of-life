import pyxel
import time
import numpy as np

height = 80
sh = 80

matrix = np.zeros(height*sh).reshape(height, sh)
PALETTE = [0xFF6347, 0xFF7F50, 0xFFA500, 0xEFD334,
           0xD1E231, 0xB2EC5D, 0x30BA8F, 0x6495ED, 0x9370DB, 0xCD5C5C,
           0x000000, 0x434750,0xFFF8DC, 0xB0C4DE, 0x08457E, 0xE0B0FF]


class App:
    def __init__(self):
        pyxel.init(height, sh, caption="life", palette=PALETTE)
        self.matrix = matrix
        self.height = height
        self.sh = sh
        self.check = 0
        self.menu = 0
        self.obj_vert = 0
        self.obj_hor = 0
        self.fighter = 0
        pyxel.load('life.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.menu == 2:
            if self.check == 0:

                boundries = [[-1, -1], [-1, 0], [-1, 1], [1, 0], [0, -1],
                             [0, 1], [1, 1], [1, -1]]
                corners = [[0, 0], [0, 1], [0,79], [79, 79], [78,79], [78, 0], [78, 1], [79, 1]]
                numb = 0
                row = 0
                exceptmatrix = np.rot90(self.matrix, k=2, axes=(0, 1))
                newmatrix = np.zeros(self.height * self.sh).reshape(
                    self.height, self.sh)
                for z in self.matrix:
                    for j in z:
                        try:
                            k = [1 for i in boundries if
                                 self.matrix[row + i[0]][numb + i[1]] == 1.0]
                        except IndexError:
                            try:
                                k = [1 for i in boundries if
                                     exceptmatrix[
                                         self.height - row - 1 + i[0]][
                                         self.sh - numb - 1 + i[1]] == 1.0]
                            except IndexError:
                                if row == 79 and numb == 0:
                                    k = [1 for i in corners if self.matrix[i[0]][i[1]] == 1.0]
                                else:
                                    if row == 0 and numb == 79:
                                        k = [1 for i in corners if self.matrix[i[1]][i[0]] == 1.0]

                        if len(k) == 3 or (
                                len(k) == 2 and self.matrix[row, numb] == 1):
                            newmatrix[row, numb] = 1.0
                        numb += 1
                    numb = 0
                    row += 1

                self.matrix = newmatrix
                time.sleep(0.005)
                self.check = 1
        else:
            if self.menu == 0:
                if pyxel.btnp(pyxel.KEY_G):
                    self.fighter = 'glider'
                    self.menu = 1
                if pyxel.btnp(pyxel.KEY_T):
                    self.fighter = 'toad'
                    self.menu = 1
                if pyxel.btnp(pyxel.KEY_A):
                    self.fighter = 'acorn'
                    self.menu = 1
                if pyxel.btnp(pyxel.KEY_E):
                    self.fighter = 'engine'
                    self.menu = 1
                if pyxel.btnp(pyxel.KEY_U):
                    self.fighter = 'gun'
                    self.menu = 1
                if pyxel.btnp(pyxel.KEY_P):
                    self.fighter = 'pulsar'
                    self.menu = 1
                if pyxel.btnp(pyxel.KEY_R):
                    self.matrix = np.random.choice([1, 0], size=(height, sh))
                    self.menu = 2

            elif self.menu == 1:
                pyxel.mouse(visible=True)
                if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                    self.obj_hor = pyxel.mouse_x
                    self.obj_vert = pyxel.mouse_y
                    self.menu = 2
                    pyxel.mouse(visible=False)
                    self.choose_your_fighter()

        if pyxel.btnp(pyxel.KEY_Q):
            self.matrix = np.zeros(height*sh).reshape(height, sh)
            self.menu = 0
            pyxel.mouse(visible=False)

    def draw(self):
        if self.menu == 2:
            pyxel.cls(0)
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[1])):
                    if self.matrix[i, j] == 0.:
                        col = 10
                    else:
                        col = 8
                    pyxel.pset(i, j, col)
            self.check = 0

        else:
            if self.menu == 0:
                pyxel.blt(0, 0, 0, 0, 0, 100, 100)
                pyxel.text(0, 1, "--THE GAME OF LIFE---",
                           pyxel.frame_count % 8)
                pyxel.text(3, 10, "choose your fighter",
                           pyxel.frame_count % 8)
                pyxel.text(2, 19, "G", 1)
                pyxel.text(15, 19, "glider", 5)
                pyxel.text(49, 19, "T", 1)
                pyxel.text(63, 19, "toad", 5)
                pyxel.text(52, 35, "P", 1)
                pyxel.text(57, 47, "pulsar", 5)
                pyxel.text(3, 53, "U", 1)
                pyxel.text(49, 56, "gun", 5)
                pyxel.text(18, 65, "R - random", 5)
                pyxel.text(1, 74, "and press the button",
                       pyxel.frame_count % 8)
                pyxel.text(2, 29, "A", 1)
                pyxel.text(19, 29, "acorn", 5)
                pyxel.text(2, 39, "E", 1)
                pyxel.text(20, 40, "engine", 5)
            else:
                pyxel.cls(10)
                pyxel.text(0, 20, "click on a pixel", 5)
                pyxel.text(0, 30, "to choose a starting", 5)
                pyxel.text(0, 40, "point", 5)

                pyxel.text(0, 60, "to exit from life", 5)
                pyxel.text(0, 67, "to the main menu", 5)
                pyxel.text(0, 74, "press [Q}", 5)

    def choose_your_fighter(self):
        if self.fighter == 'glider':
            return self.paint_your_fighter([[0, 1], [1, 2], [2, 2], [2, 1], [2,0]])
        if self.fighter == 'toad':
            return self.paint_your_fighter(
                [[0, 2], [1, 0], [2, 0], [1, 3], [2, 3], [3, 1]])
        if self.fighter == 'acorn':
            return self.paint_your_fighter(
                [[0, 1], [1, 3], [2, 0], [2, 1], [2, 4], [2, 5], [2, 6]])
        if self.fighter == 'engine':
            return self.paint_your_fighter(
                [[0, 0], [0, 1], [0, 2], [0, 4], [1, 0], [2, 3], [2, 4],
                 [3, 1], [3, 2], [3, 4], [4, 0], [4, 2], [4, 4]])
        if self.fighter == 'gun':
            return self.paint_your_fighter(
                [[1, 5], [2, 5], [1, 6], [2, 6], [11, 5], [11, 6], [11, 7],
                 [12, 4], [12, 8], [13, 3], [13, 9], [14, 3], [14, 9],
                 [15, 6], [16, 4], [16, 8], [17, 5], [17, 6], [17, 7], [18, 6],
                 [21, 3], [21, 4], [21, 5], [22, 3], [22, 4], [22, 5],
                 [23, 2], [23, 6], [25, 1], [25, 2], [25, 6], [25, 7]
                    , [35, 3], [36, 3], [35, 4], [36, 4]])
        if self.fighter == 'pulsar':
            return self.paint_your_fighter(
            [[4, 1], [5, 1], [6, 1], [10, 1], [11, 1], [12, 1], [2, 3],
             [2, 4], [2, 5], [4, 6], [5, 6], [6, 6], [7, 3],
             [7, 4], [7, 5], [9, 3], [9, 4], [9, 5], [10, 6], [11, 6],
             [12, 6], [14, 3], [14, 4], [14, 5], [4, 8], [5, 8],
             [6, 8], [10, 8], [11, 8], [12, 8], [2, 9], [2, 10], [2, 11],
             [7, 9], [7, 10], [7, 11], [9, 9], [9, 10], [9, 11],
             [14, 9], [14, 10], [14, 11], [4, 13], [5, 13], [6, 13]
                , [10, 13], [11, 13], [12, 13]])

    def paint_your_fighter(self, figure):
        for i in figure:
            self.matrix[self.obj_hor + i[0]][self.obj_vert + i[1]] += 1

App()



