from collections import deque
from typing import List, Tuple


class Grid:
    def __init__(self, size: int, forbidden: List[Tuple[int, int]], wifi_power: int = 10, wall_penalty: int = 2):
        self.size = size
        self.forbidden = set(forbidden)
        self.wifi_power = wifi_power
        self.wall_penalty = wall_penalty

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def calculate_coverage(self, wifi_positions: List[Tuple[int, int]]) -> List[List[int]]:
        signal_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for wy, wx in wifi_positions:
            queue = deque()
            queue.append((wx, wy, self.wifi_power))

            while queue:
                y, x, power = queue.popleft()

                if not self.is_inside(y, x) or power <= 0:
                    continue

                if power <= signal_grid[x][y]:
                    continue

                signal_grid[x][y] = power

                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    if not self.is_inside(ny, nx):
                        continue

                    penalty = self.wall_penalty if (nx, ny) in self.forbidden else 0
                    new_power = power - 1 - penalty

                    if new_power > signal_grid[nx][ny]:
                        queue.append((ny, nx, new_power))

        return signal_grid
