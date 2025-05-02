import random
import sys
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

DEFAULT_GRID_SIZE = 100
DEFAULT_BURN_PROB = 0.3
DEFAULT_BURN_DURATION = 3
DEFAULT_SIMULATION_STEPS = 100

MIN_GRID_SIZE = 1
MIN_BURN_PROB = 0.0
MAX_BURN_PROB = 1.0
MIN_BURN_DURATION = 1
MIN_SIM_STEPS = 1

STATE_UNBURNED = -1
STATE_FADING = 1
STATE_BURNED = 0

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1), (1, 0), (1, 1)]

COLORS = ['green', 'black', 'red']


def main():
    GRID_SIZE, P_BURN, T_BURN, STEPS = get_parameters()

    grid, current_queue, next_queue, cmap, norm = initialize_simulation_environment(GRID_SIZE, T_BURN)

    run_simulation(STEPS, grid, current_queue, next_queue, P_BURN, T_BURN, cmap, norm)

    show_plot()



def get_parameters():
    grid_size = get_input("Enter grid size", DEFAULT_GRID_SIZE, int, MIN_GRID_SIZE)
    p_burn = get_input("Enter burn probability", DEFAULT_BURN_PROB, float, MIN_BURN_PROB, MAX_BURN_PROB)
    t_burn = get_input("Enter burn duration", DEFAULT_BURN_DURATION, int, MIN_BURN_DURATION)
    steps = get_input("Enter number of simulation steps", DEFAULT_SIMULATION_STEPS, int, MIN_SIM_STEPS)
    return grid_size, p_burn, t_burn, steps


def get_input(prompt, default_value, value_type=int, min_value=None, max_value=None):
    try:
        raw = input_with_default(prompt, default_value)
        value = value_type(raw)
        validate_range(value, prompt, min_value, max_value)
        return value
    except ValueError:
        print(f"Invalid input. Please enter a valid {value_type.__name__}.")
        sys.exit(1)


def input_with_default(prompt, default_value):
    return input(f"{prompt} (default {default_value}): ").strip() or str(default_value)


def validate_range(value, prompt, min_value=None, max_value=None):
    checks = [
        (min_value, lambda v, limit: v < limit, f"{prompt} must be ≥ {min_value}."),
        (max_value, lambda v, limit: v > limit, f"{prompt} must be ≤ {max_value}."),
    ]
    for limit, check, message in checks:
        if limit is not None and check(value, limit):
            print(message)
            sys.exit(1)
            
            

def initialize_simulation_environment(grid_size, t_burn):
    grid = initialize_grid(grid_size)
    current_queue, next_queue = initialize_queue()
    
    ignite_center(grid, current_queue, t_burn)

    cmap, norm = create_colormap(t_burn)
    
    plt.figure()
    
    return grid, current_queue, next_queue, cmap, norm


def initialize_grid(size):
    return np.full((size, size), STATE_UNBURNED)


def initialize_queue():
    return deque(), deque()


def ignite_center(grid, current_queue, T_BURN):
    center = len(grid) // 2
    grid[center, center] = T_BURN
    current_queue.append((center, center))


def create_colormap(t_burn):
    cmap = colors.ListedColormap(COLORS)
    bounds = [STATE_UNBURNED - 0.5, STATE_BURNED - 0.5, 0.5, t_burn + 0.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    return cmap, norm



def run_simulation(steps, grid, current_queue, next_queue, p_burn, t_burn, cmap, norm):
    for step in range(steps):
        visualize(grid, cmap, norm, step)
        update_fire(grid, current_queue, next_queue, DIRECTIONS, p_burn, t_burn)
        current_queue, next_queue = next_queue, deque()


def visualize(grid, cmap, norm, step):
    plt.clf()
    plt.imshow(grid, cmap=cmap, norm=norm)
    plt.title(f'Time Step {step}')
    plt.axis('off')
    plt.pause(0.1)
    

def update_fire(grid, current_queue, next_queue, directions, p_burn, t_burn):
    while current_queue:
        i, j = current_queue.popleft()
        process_cell(grid, i, j, next_queue)
        ignite_neighbors(grid, i, j, directions, p_burn, t_burn, next_queue)


def process_cell(grid, i, j, next_queue):
    if grid[i, j] > STATE_FADING:
        grid[i, j] -= 1
        next_queue.append((i, j))
    else:
        grid[i, j] = STATE_BURNED

    
def ignite_neighbors(grid, i, j, directions, p_burn, t_burn, next_queue):
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if is_within_bounds(grid, ni, nj):
            try_to_ignite(grid, ni, nj, p_burn, t_burn, next_queue)


def is_within_bounds(grid, i, j):
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def try_to_ignite(grid, i, j, p_burn, t_burn, next_queue):
    if grid[i, j] == STATE_UNBURNED and random.random() < p_burn:
        grid[i, j] = t_burn
        next_queue.append((i, j))



def show_plot():
    plt.show()



if __name__ == "__main__":
    main()
