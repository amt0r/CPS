import matplotlib.pyplot as plt
import numpy as np
from fun import *
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint


def main():
    state0_1 = [1.0, 1.0, 1.0]
    state0_2 = [1.0, 1.0, 1.001]
    time = np.arange(0.0, 49.0, 0.01)

    states_1 = odeint(f, state0_1, time)
    states_2 = odeint(f, state0_2, time)

    x1_end, y1_end, z1_end = states_1[-1]
    x2_end, y2_end, z2_end = states_2[-1]

    fig = plt.figure()

    ax1 = fig.add_subplot(231, projection='3d')
    plot_trajectory(ax1, states_1, 'blue', "Початковий стан: [1.0, 1.0, 1.0]")

    ax2 = fig.add_subplot(232, projection='3d')
    plot_trajectory(ax2, states_2, 'red', "Початковий стан: [1.0, 1.0, 1.001]")

    ax_end_points = fig.add_subplot(233, projection='3d')
    plot_endpoints(ax_end_points, (x1_end, y1_end, z1_end), (x2_end, y2_end, z2_end))

    ax_both_trajectory = fig.add_subplot(223, projection='3d')
    plot_trajectory(ax_both_trajectory, states_1, 'blue')
    plot_trajectory(ax_both_trajectory, states_2, 'red', "Порівняння обох траєкторій")

    ax_animation = fig.add_subplot(224, projection='3d')
    update = create_lorenz_animation_subplot(ax_animation, states_1, states_2, time)
    
    ani = FuncAnimation(fig, update, frames=len(time), interval=10, blit=True)

    toggle_full_screen()

    plt.show()

if __name__ == "__main__":
    main()
