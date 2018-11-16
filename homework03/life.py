import pygame
import random
from pygame.locals import *


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
        self.clist = self.cell_list()

    def draw_grid(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.clist = self.cell_list(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.clist)
            self.clist = self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> list:
        grid = [[0 for i in range(self.cell_width)] for j in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = random.randint(0, 1)
        self.clist = grid
        return self.clist

    def draw_cell_list(self, rects: list) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if rects[i][j]:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')
                pygame.draw.rect(self.screen, color, (
                    self.cell_size*j, self.cell_size*i, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: tuple) -> list:
        neighbours = []
        row, col = cell
        rows = [row - 1, row, row + 1]
        cols = [col - 1, col, col + 1]
        for i in rows:
            if 0 <= i < self.cell_height:
                for j in cols:
                    if j == col and i == row:
                        continue
                    if 0 <= j < self.cell_width:
                        neighbours.append(self.clist[i][j])
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        new_clist = []
        for row in range(len(cell_list)):
            new_clist.append([])
            for col in range(len(cell_list[row])):
                neighbours = self.get_neighbours((row, col))
                sum = 0
                for i in neighbours:
                    if i:
                        sum += 1
                if cell_list[row][col] == 1 and (sum == 2 or sum == 3):
                    new_clist[row].append(1)
                elif cell_list[row][col] == 0 and sum == 3:
                    new_clist[row].append(1)
                else:
                    new_clist[row].append(0)
        self.clist = new_clist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
