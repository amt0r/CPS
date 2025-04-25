import unittest

from grid import Grid
from individual import Individual
from island import Island


class TestIsland(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(size=5, forbidden=[])
        self.wifi_count = 3
        self.population_size = 10
        self.mutation_rate = 0.1
        self.migration_rate = 2
        self.elitism_rate = 0.2

        self.island = Island(self.grid, self.wifi_count, self.population_size,
                             self.mutation_rate, self.migration_rate, self.elitism_rate)
        self.population = self.island.initialize_population()
        self.island.evaluate_population(self.population)

    def test_coverage_evaluation(self):
        for ind in self.population:
            self.assertIsNotNone(ind.coverage)
            self.assertGreaterEqual(ind.coverage, 0)

    def test_parent_selection(self):
        parents = self.island.select_parents(self.population)
        self.assertEqual(len(parents), self.population_size // 2)
        self.assertTrue(all(isinstance(p, Individual) for p in parents))

    def test_offspring_creation(self):
        parents = self.island.select_parents(self.population)
        offspring = self.island.create_offspring(parents)
        self.assertTrue(len(offspring) <= len(parents) // 2)
        self.assertTrue(all(isinstance(child, Individual) for child in offspring))

    def test_offspring_evaluation(self):
        parents = self.island.select_parents(self.population)
        offspring = self.island.create_offspring(parents)
        self.island.evaluate_population(offspring)
        for child in offspring:
            self.assertIsNotNone(child.coverage)
            self.assertGreaterEqual(child.coverage, 0)

    def test_next_generation_selection(self):
        parents = self.island.select_parents(self.population)
        offspring = self.island.create_offspring(parents)
        self.island.evaluate_population(offspring)
        next_gen = self.island.select_next_generation(self.population, offspring)
        self.assertEqual(len(next_gen), self.population_size)
        self.assertTrue(all(isinstance(ind, Individual) for ind in next_gen))

    def test_result_output(self):
        best = self.island.evolve_island(island_idx=0, population=self.population, max_generations=3)
        self.assertIsInstance(best, Individual)
        self.assertIsNotNone(best.coverage)
        self.assertGreaterEqual(best.coverage, 0)


if __name__ == '__main__':
    unittest.main()
