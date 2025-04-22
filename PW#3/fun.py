import matplotlib.pyplot as plt

rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0

def f(state, t):
    x, y, z = state
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z

def set_limits(ax):
    ax.set_xlim([-20, 20])
    ax.set_ylim([-20, 30])
    ax.set_zlim([0, 40])
    
def plot_trajectory(ax, states, color, title = ""):
    set_limits(ax)
    ax.plot(states[:, 0], states[:, 1], states[:, 2], color=color)
    ax.set_title(title)

def plot_endpoints(ax, end1, end2, title = "Кінцеві точки траєкторій"):
    set_limits(ax)
    ax.scatter(end1[0], end1[1], end1[2], color='blue', s=50)
    ax.scatter(end2[0], end2[1], end2[2], color='red', s=50)
    ax.set_title(title)

def create_lorenz_animation_subplot(ax_animation, states_1, states_2, time):
    set_limits(ax_animation)
    ax_animation.set_title("Анімація траєкторій Лоренца")

    line1, = ax_animation.plot([], [], [], lw=1, color='blue')
    point1, = ax_animation.plot([], [], [], 'o', color='blue')

    line2, = ax_animation.plot([], [], [], lw=1, color='red')
    point2, = ax_animation.plot([], [], [], 'o', color='red')

    def update(frame):
        line1.set_data(states_1[:frame, 0], states_1[:frame, 1])
        line1.set_3d_properties(states_1[:frame, 2])
        point1.set_data([states_1[frame, 0]], [states_1[frame, 1]])
        point1.set_3d_properties([states_1[frame, 2]])

        line2.set_data(states_2[:frame, 0], states_2[:frame, 1])
        line2.set_3d_properties(states_2[:frame, 2])
        point2.set_data([states_2[frame, 0]], [states_2[frame, 1]])
        point2.set_3d_properties([states_2[frame, 2]])

        return line1, point1, line2, point2

    return update

def toggle_full_screen():
    mng = plt.get_current_fig_manager()
    try:
        mng.full_screen_toggle()
    except AttributeError:
        pass