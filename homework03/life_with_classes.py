import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_cell_list(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.clist.grid[i][j].is_alive():
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')
                pygame.draw.rect(self.screen, color, (
                    self.cell_size*j, self.cell_size*i, self.cell_size, self.cell_size))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = CellList(self.cell_height, self.cell_width, randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list()
            self.clist.update()
            
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row: int, col: int, state: bool =False) -> None:
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self) -> bool:
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False, open_file=False, file_clist=[]):
        self.nrows = nrows
        self.ncols = ncols
        self.grid = []

        if randomize:
            for i in range(self.nrows):
                self.grid.append([])
                for j in range(self.ncols):
                    self.grid[i].append(Cell(i, j, random.randint(0, 1)))
        else:
            for i in range(self.nrows):
                self.grid.append([])
                for j in range(self.ncols):
                    self.grid[i].append(Cell(i, j))

        if open_file:
            self.grid = file_clist

    def get_neighbours(self, cell) -> list:
        neighbours = []
        row, col = cell.row, cell.col
        rows = [row - 1, row, row + 1]
        cols = [col - 1, col, col + 1]
        for i in rows:
            if 0 <= i < self.nrows:
                for j in cols:
                    if j == col and i == row:
                        continue
                    if 0 <= j < self.ncols:
                        if self.grid[i][j].is_alive():
                            neighbours.append(Cell(i,j,True))
                        else:
                            neighbours.append(Cell(i,j,False))
        return neighbours

    def update(self):
        new_clist = deepcopy(self.grid)
        sum = 0
        for cell in self:
            neighbours = self.get_neighbours(cell)
            for i in neighbours:
                if i:
                    sum += 1
            if cell.is_alive():
                if sum < 2 or sum > 3:
                    new_clist[cell.row][cell.col].alive = 0
            else:
                if sum == 3:
                    new_clist[cell.row][cell.col].alive = 1
        self.clist = new_clist
        return self

    def __iter__(self):
        self.i_row, self.i_col = 0, 0
        return self

    def __next__(self):
        if self.i_row == self.nrows:
            raise StopIteration
        i_grid = self.grid[self.i_row][self.i_col]
        self.i_col += 1
        if self.i_col == self.ncols:
            self.i_col = 0
            self.i_row += 1
        return i_grid

    def __str__(self) -> str:
        str = ""
        for i in range(self.nrows):
            for j in range(self.ncols):
                if (self.grid[i][j].is_alive()):
                    str += '1 '
                else:
                    str += '0 '
            str += '\n'
        return str

    @classmethod
    def from_file(cls, filename):
        filegrid = []
        with open(filename) as file:
            for nrow, line in enumerate(file):
                row = [Cell(nrow, ncol, int(state))
                       for ncol, state in enumerate(line) if state in "01"]
                filegrid.append(row)
        clist = cls(len(filegrid), len(filegrid[0]))
        clist.grid = filegrid
        return clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
