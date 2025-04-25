import time

from grid import Grid
from island import Island
from reader import load_forbidden_cells
from visualizer import Visualizer


def main():
    grid_size = 30
    forbidden_cells = load_forbidden_cells("./PW#4/grid.csv") 

    wifi_count = int(input(f"Enter the number of Wi-Fi routers (default 8): ").strip() or "8")
    wifi_power = int(input(f"Enter the Wi-Fi power (default 10): ").strip() or "10")
    wall_penalty = int(input(f"Enter the wall penalty (default 7): ").strip() or "7")
    population_size = int(input(f"Enter the population size (default 50): ").strip() or "50")
    mutation_rate = float(input(f"Enter the mutation rate (default 0.1): ").strip() or "0.1")
    migration_rate = int(input(f"Enter the migration rate (default 10): ").strip() or "10")
    elitism_rate = float(input(f"Enter the elitism rate (default 0.1): ").strip() or "0.1")
    islands_count = int(input(f"Enter the number of islands (default 12): ").strip() or "12")
    max_generations = int(input(f"Enter the maximum number of generations (default 100): ").strip() or "100")

    start_time = time.time()

    grid = Grid(grid_size, forbidden_cells, wifi_power, wall_penalty)

    island_model = Island(grid, wifi_count,
                          population_size, mutation_rate,
                          migration_rate, elitism_rate)
    best_individual = island_model.run(islands_count, max_generations)

    print("Best individual's fitness:", best_individual.coverage)
    print("Best individual's wifi positions:", best_individual.wifi_positions)

    end_time = time.time()
    result_time = end_time - start_time
    print(f"Time: {result_time:.2f}")

    visualizer = Visualizer(grid_size, forbidden_cells, best_individual.wifi_positions)
    visualizer.visualize(best_individual.signal_grid)



if __name__ == "__main__":
    main()
