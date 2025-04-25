from concurrent.futures import ProcessPoolExecutor
from typing import List

from grid import *
from individual import *


def evolve_island_wrapper(args):
    island_obj, island_idx, population, generations = args
    return island_obj.evolve_island(island_idx, population, generations)


class Island:
    def __init__(self, grid: Grid, wifi_count: int,
                 population_size: int, mutation_rate: float, migration_rate: int, elitism_rate: float):
        self.grid = grid
        self.grid_size = grid.size
        self.wifi_count = wifi_count
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.migration_rate = migration_rate
        self.elitism_count = max(1, int(population_size * elitism_rate))

    def initialize_population(self) -> List[Individual]:
        return [Individual.initialize_random(self.grid_size, self.wifi_count, list(self.grid.forbidden))
                for _ in range(self.population_size)]

    def evaluate_population(self, population: List[Individual]) -> None:
        for individual in population:
            individual.evaluate_coverage(self.grid)

    def select_parents(self, population: List[Individual]) -> List[Individual]:
        return sorted(population, key=lambda ind: ind.coverage, reverse=True)[:self.population_size // 2]

    def create_offspring(self, parents: List[Individual]) -> List[Individual]:
        offspring = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                child = parents[i].crossover(parents[i + 1])
                child.mutate(self.grid_size, list(self.grid.forbidden), self.mutation_rate)
                offspring.append(child)
        return offspring

    def select_next_generation(self, population: List[Individual], offspring: List[Individual]) -> List[Individual]:
        combined = population + offspring
        combined.sort(key=lambda ind: ind.coverage, reverse=True)
        elites = combined[:self.elitism_count]
        return elites + combined[self.elitism_count:self.population_size]
    
    def should_stop(self, generation: int, max_generations: int) -> bool:
        return generation >= max_generations

    def get_best_individual(self, population: List[Individual]) -> Individual:
        return max(population, key=lambda ind: ind.coverage)

    def evolve_island(self, island_idx: int, population: List[Individual],
                      max_generations: int) -> Individual:
        generation = 0
        best_individual = None
        best_coverage = 0
        
        # Оцінка придатності
        self.evaluate_population(population)

        while not self.should_stop(generation, max_generations):
            # Вибір батьків
            parents = self.select_parents(population)
            # Створення нащадків
            offspring = self.create_offspring(parents)
            # Оцінка придатності нової популяції
            self.evaluate_population(offspring)
            # Вибір для наступної популяції
            population = self.select_next_generation(population, offspring)

            current_best = self.get_best_individual(population)
            print(f"Island {island_idx} - Generation {generation} - Best covarage {current_best.coverage}")
            
            if current_best.coverage > best_coverage:
                best_coverage = current_best.coverage
                best_individual = current_best.copy()
                
            generation += 1
        # Вивід результатів
        return best_individual

    def run(self, islands_count: int = 4, max_generations: int = 50) -> Individual:
        # Ініціалізація популяції
        island_populations = [self.initialize_population() for _ in range(islands_count)]
        args = [(self, i, island_populations[i], max_generations) for i in range(islands_count)]

        with ProcessPoolExecutor(max_workers=islands_count) as executor:
            results = list(executor.map(evolve_island_wrapper, args))

        return max(results, key=lambda ind: ind.coverage)
