import random
import unittest
from collections import deque
from unittest.mock import patch

import numpy as np
from main import *


class TestSimulation(unittest.TestCase):
    
    @patch('builtins.input', side_effect=['100', '0.3', '3', '100'])
    def test_get_parameters(self, mock_input):
        grid_size, p_burn, t_burn, steps = get_parameters()
        
        self.assertEqual(grid_size, 100)
        self.assertEqual(p_burn, 0.3)
        self.assertEqual(t_burn, 3)
        self.assertEqual(steps, 100)

    def test_initialize_grid(self):
        grid_size = 5
        
        grid = initialize_grid(grid_size)
        
        self.assertEqual(grid.shape, (grid_size, grid_size))
        self.assertTrue(np.all(grid == STATE_UNBURNED))

    def test_initialize_queue(self):
        current_queue, next_queue = initialize_queue()
        
        self.assertEqual(len(current_queue), 0)
        self.assertEqual(len(next_queue), 0)

    def test_ignite_center(self):
        grid_size = 5
        center = grid_size // 2
        grid = initialize_grid(grid_size)
        current_queue, _ = initialize_queue()
        
        ignite_center(grid, current_queue, 3)
        
        self.assertEqual(grid[center, center], 3)

    @patch('random.random', return_value=0.1)
    def test_try_to_ignite_burn(self, mock_random):
        grid_size = 5
        grid = initialize_grid(grid_size)
        next_queue = deque()
        
        try_to_ignite(grid, 2, 2, 0.3, 3, next_queue)
        
        self.assertEqual(grid[2, 2], 3)
        self.assertEqual(len(next_queue), 1)
        
    @patch('random.random', return_value=0.5)
    def test_try_to_ignite_unburn(self, mock_random):
        grid_size = 5
        grid = initialize_grid(grid_size)
        next_queue = deque()
        
        try_to_ignite(grid, 2, 2, 0.3, 3, next_queue)
        
        self.assertEqual(grid[2, 2], STATE_UNBURNED)
        self.assertEqual(len(next_queue), 0)

    def test_is_within_bounds(self):
        grid_size = 5
        grid = initialize_grid(grid_size)
        
        self.assertTrue(is_within_bounds(grid, 2, 2))
        self.assertFalse(is_within_bounds(grid, 5, 5))
        self.assertFalse(is_within_bounds(grid, -1, 0))

    def test_process_cell(self):
        grid_size = 5
        grid = initialize_grid(grid_size)
        next_queue = deque()
        grid[2, 2] = 3
        
        process_cell(grid, 2, 2, next_queue)
        
        self.assertEqual(grid[2, 2], 2)
        self.assertEqual(len(next_queue), 1)

    def test_run_simulation(self):
        grid_size = 5
        grid = initialize_grid(grid_size)
        current_queue, next_queue = initialize_queue()
        ignite_center(grid, current_queue, 3)
        p_burn = 0.3
        t_burn = 3
        steps = 10
        cmap, norm = create_colormap(t_burn)
        
        run_simulation(steps, grid, current_queue, next_queue, p_burn, t_burn, cmap, norm)
        
        self.assertTrue(np.any(grid != STATE_UNBURNED))

if __name__ == '__main__':
    unittest.main()
