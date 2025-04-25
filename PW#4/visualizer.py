import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, grid_size: int, forbidden_cells: list, wifi_positions: list):
        self.grid_size = grid_size
        self.forbidden_cells = forbidden_cells
        self.wifi_positions = wifi_positions

    def plot_grid(self, coverage=None):
        grid = np.zeros((self.grid_size, self.grid_size))

        for cell in self.forbidden_cells:
            grid[cell[0], cell[1]] = 2

        for wifi in self.wifi_positions:
            grid[wifi[0], wifi[1]] = 1

        plt.imshow(grid, cmap='binary')
        
        if coverage is not None:
            plt.imshow(coverage, cmap='coolwarm', alpha=0.5)
        
        plt.title("Wi-Fi Coverage")
        plt.show()

    def visualize(self, coverage=None):
        self.plot_grid(coverage)
