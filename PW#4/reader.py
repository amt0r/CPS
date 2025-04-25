import csv
from typing import List, Tuple


def load_forbidden_cells(csv_file: str) -> List[Tuple[int, int]]:
    forbidden_cells = []
    
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for y, row in enumerate(reader):
            for x, value in enumerate(row):
                if value == '1':
                    forbidden_cells.append((y, x))
    
    return forbidden_cells
