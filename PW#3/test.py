import unittest

import matplotlib.pyplot as plt
import numpy as np
from fun import *


class TestLorenzFunctions(unittest.TestCase):

    def test_f_output(self):
        state = np.random.uniform(-10, 10, size=3)
        t = np.random.uniform(0.1, 10)
        expected_dx = sigma * (state[1] - state[0])
        expected_dy = state[0] * (rho - state[2]) - state[1]
        expected_dz = state[0] * state[1] - beta * state[2]

        dx, dy, dz = f(state, t)

        self.assertAlmostEqual(dx, expected_dx, places=6)
        self.assertAlmostEqual(dy, expected_dy, places=6)
        self.assertAlmostEqual(dz, expected_dz, places=6)



    def test_set_limits(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        set_limits(ax)
        
        self.assertEqual(ax.get_xlim(), (-20.0, 20.0))
        self.assertEqual(ax.get_ylim(), (-20.0, 30.0))
        self.assertEqual(ax.get_zlim(), (0.0, 40.0))

    def test_plot_trajectory(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        states = np.random.rand(100, 3)
        
        plot_trajectory(ax, states, 'blue', 'Test Title')
        
        self.assertEqual(ax.get_title(), 'Test Title')

    def test_plot_endpoints(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        end1 = np.random.rand(100, 3)
        end2 = np.random.rand(100, 3)
        
        plot_endpoints(ax, end1, end2)
        
        self.assertEqual(ax.get_title(), 'Кінцеві точки траєкторій')

    def test_create_lorenz_animation_subplot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        states_1 = np.random.rand(100, 3)
        states_2 = np.random.rand(100, 3)
        time = np.linspace(0, 10, 500)
        
        update = create_lorenz_animation_subplot(ax, states_1, states_2, time)
        result = update(10)
        
        self.assertEqual(len(result), 4)


if __name__ == '__main__':
    unittest.main()
