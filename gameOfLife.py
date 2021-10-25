import pygame
import numpy as np
from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt
from quantum import quantum_grid
import time

PURPLE = (60, 30, 60)
WHITE = (255, 255, 255)
GREY = (175, 165, 160)
ORANGE = (230, 85, 30)


def color_cell(grid, pixel_size, color, row, col):
    pygame.draw.rect(grid,
                     color,
                     (col * pixel_size, row * pixel_size, pixel_size - 1, pixel_size - 1))


def init_cells(grid, pixel_size, live_cells):
    new_cells = np.zeros((grid_size, grid_size))
    for row in range(live_cells.shape[0]):
        for col in range(live_cells.shape[1]):

            cell_color = PURPLE

            if(live_cells[row, col] == -1):
                cell_color = ORANGE
                new_cells[row, col] = -1
            elif(live_cells[row, col] == 1):
                cell_color = WHITE
                new_cells[row, col] = 1
            color_cell(grid, pixel_size, cell_color, row, col)
    return new_cells


def update_cells(grid, pixel_size, live_cells):
    new_cells = np.zeros((grid_size, grid_size))
    for row in range(live_cells.shape[0]):
        for col in range(live_cells.shape[1]):
            neighbors = np.absolute(
                np.sum(live_cells[row - 1: row + 2, col - 1: col + 2]) - live_cells[row, col])

            cell_color = PURPLE

            if(live_cells[row, col] == -1):
                cell_color = ORANGE
                new_cells[row, col] = -1
            elif(live_cells[row, col] == 1):
                if(neighbors < 2 or neighbors > 3):
                    cell_color = GREY
                else:
                    cell_color = WHITE
                    new_cells[row, col] = 1
            elif(live_cells[row, col] == 0 and neighbors == 3):
                cell_color = WHITE
                new_cells[row, col] = 1
            color_cell(grid, pixel_size, cell_color, row, col)
    return new_cells


def generate_classical(grid_size):
    live_cells = np.zeros((grid_size, grid_size))
    for row in range(live_cells.shape[0]):
        for col in range(live_cells.shape[1]):
            value = np.random.random_integers(0, 1001 + 1)
            if value == 0:
                live_cells[row, col] = -1
            elif value <= 250:
                live_cells[row, col] = 1
    return live_cells


def generate_quantum(grid_size):
    return quantum_grid(grid_size)


def game(grid_size, pixel_size, live_cells, pause_time_on_spawn):
    grid = pygame.display.set_mode(
        (grid_size * pixel_size,
         grid_size * pixel_size))

    grid.fill(PURPLE)
    live_cells = init_cells(grid, pixel_size, live_cells)
    pygame.display.update()

    time.sleep(pause_time_on_spawn)

    clock = pygame.time.Clock()
    while 1 == 1:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        grid.fill(PURPLE)
        live_cells = update_cells(grid, pixel_size, live_cells)
        pygame.display.update()


if __name__ == "__main__":
    # Creates n x n size grid for the game
    grid_size = 100

    # Size of each individual creature
    pixel_size = 8

    # Option to generate the board using classical methods or quantum
    #live_cells = generate_classical(grid_size)
    live_cells = generate_quantum(grid_size)

    # Allows you to wait a few seconds so that you can see the created board
    pause_time_on_spawn = 3

    game(grid_size, pixel_size, live_cells, pause_time_on_spawn)
