import pygame
import random
from copy import deepcopy
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
        self.grid = self.cell_list()

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.grid = self.cell_list(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.grid)
            self.update_cell_list(self.grid)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> list:
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        grid = [[0 for i in range(self.cell_width)] for j in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = random.randint(0, 1)
        self.grid = grid
        return self.grid

    def draw_cell_list(self, rects: list) -> None:
        """ Отображение списка клеток
        """

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if rects[i][j]:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')
                pygame.draw.rect(self.screen, color, (
                    self.cell_size*j, self.cell_size*i, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки
        """
        neighbours = []
        row, col = cell
        w = self.cell_width - 1
        h = self.cell_height - 1
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i != row and j != col) and (0 <= i <= h and 0 <= j <= w):
                    neighbours.append(self.grid[i][i])
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_grid = deepcopy(self.grid)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                s = sum(self.get_neighbours((i, j)))
                if self.grid[i][j]:
                    if s < 2 or s > 3:
                        new_grid[i][j] = 0
                    else:
                        if s == 3:
                            new_grid[i][j] = 1
        self.grid = new_grid
        return self.grid


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
