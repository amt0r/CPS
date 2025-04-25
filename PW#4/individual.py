import random
from typing import List, Tuple


class Individual:
    def __init__(self, wifi_positions: List[Tuple[int, int]]):
        self.wifi_positions = wifi_positions
        self.signal_grid = None
        self.coverage = 0.0 

    @staticmethod
    def initialize_random(grid_size: int, wifi_count: int, forbidden: List[Tuple[int, int]]) -> "Individual":
        positions = set()
        while len(positions) < wifi_count:
            pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
            if pos not in forbidden:
                positions.add(pos)
        return Individual(list(positions))

    def evaluate_coverage(self, grid) -> float:
        signal_grid = grid.calculate_coverage(self.wifi_positions)
        total_signal = sum(sum(row) for row in signal_grid)
        self.signal_grid = signal_grid
        self.coverage = total_signal
        return self.coverage

    def mutate(self, grid_size: int, forbidden: List[Tuple[int, int]], mutation_rate: float = 0.1):
        for i in range(len(self.wifi_positions)):
            if random.random() < mutation_rate:
                new_pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
                while new_pos in forbidden:
                    new_pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
                self.wifi_positions[i] = new_pos

    def crossover(self, other: "Individual") -> "Individual":
        point = random.randint(1, len(self.wifi_positions) - 1)
        child_genes = self.wifi_positions[:point] + other.wifi_positions[point:]
        seen = set()
        unique_genes = []
        for pos in child_genes:
            if pos not in seen:
                unique_genes.append(pos)
                seen.add(pos)
            if len(unique_genes) == len(self.wifi_positions):
                break
        return Individual(unique_genes)

    def copy(self) -> "Individual":
        clone = Individual(self.wifi_positions[:])
        clone.coverage = self.coverage
        clone.signal_grid = self.signal_grid
        return clone
