#!/usr/bin/python3

import numpy as np
from utils import log


class InputFile:
    def __init__(self, file_path):
        self._rows = []
        self.num_rows = 0
        self.num_cols = 0
        self.num_ingredients_min = 0
        self.num_cells_per_slice_max = 0

        self._file = open(file_path, 'r')
        self._parse()

    def __del__(self):
        self._file.close()

    def _parse(self):
        content = self._file.readlines()
        line0 = content[0]
        self.num_rows = int(line0[0])
        self.num_cols = int(line0[2])
        self.num_ingredients_min = int(line0[4])
        self.num_cells_per_slice_max = int(line0[6])

        rows = []
        for line in content[1:]:
            row = []
            row.extend(line.rstrip('\n'))
            rows.append(row)

        self.content = np.array(rows)

        log("Number of rows (R): " + str(self.num_rows))
        log("Number of columns (C): " + str(self.num_cols))
        log("Minimum number of each ingredient cells in each slice (L): " + str(self.num_ingredients_min))
        log("Maximum total number of cells of a slice (H): " + str(self.num_cells_per_slice_max))

    def print(self):
        for line in self._file:
            print(line)


class OutputFile:
    def __init__(self, file_path):
        self._file = open(file_path, 'w')
        self.slices = []

    def __del__(self):
        self._file.close()

    def write(self, slices):
        lines = [str(len(slices)) + "\n"]
        for s in slices:
            lines.append(str(s.r1) + " "
                         + str(s.c1) + " "
                         + str(s.r2) + " "
                         + str(s.c2) + "\n")

        self._file.writelines(lines)
