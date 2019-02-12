#!/usr/bin/python3

import itertools as it
from math import floor, ceil


class Slice:
    def __init__(self, pizza, r1, c1, r2, c2):
        self.r1 = min(r1, r2)
        self.r2 = max(r1, r2)
        self.c1 = min(c1, c2)
        self.c2 = max(c1, c2)

        self.content = pizza.content[r1:r2+1, c1:c2+1]

    @property
    def num_rows(self):
        return self.r2 - self.r1 + 1

    @property
    def num_cols(self):
        return self.c2 - self.c1 + 1

    @property
    def num_cells_mushroom(self):
        return sum(self.content.ravel() == 'M')

    @property
    def num_cells_tomato(self):
        return sum(self.content.ravel() == 'T')

    @property
    def num_cells(self):
        return self.num_rows * self.num_cols

    def overlaps(self, other):
        if self.c1 > other.c2 or self.c2 < other.c1:
            return False
        if self.r1 > other.r2 or self.r2 < other.r1:
            return False
        return True


class Pizza:
    def __init__(self, input_file, output_file):
        self.num_rows = input_file.num_rows
        self.num_cols = input_file.num_cols
        self.num_ingredients_min = input_file.num_ingredients_min
        self.num_cells_per_slice_max = input_file.num_cells_per_slice_max
        self.content = input_file.content
        self.slices = []

        self.output_file = output_file

    @property
    def num_cells(self):
        return self.num_rows * self.num_cols

    @property
    def num_slices_min(self):
        return floor(self.num_cells / self.num_cells_per_slice_max)

    @property
    def num_slices_max(self):
        return ceil(self.num_cells / (2 * self.num_ingredients_min))

    @property
    def num_cells_in_slices(self):
        n = 0
        for s in self.slices:
            n += s.num_cells
        return n

    def overlaps(self, new_slice):
        for s in self.slices:
            if s.overlaps(new_slice):
                return True
        return False

    def is_valid_slice(self, r1, c1, r2, c2):
        s = Slice(self, r1, c1, r2, c2)

        if s.num_cells_tomato < self.num_ingredients_min:
            return False

        if s.num_cells_mushroom < self.num_ingredients_min:
            return False

        if s.num_cells > self.num_cells_per_slice_max:
            return False

        return True

    @staticmethod
    def is_valid_cut(*slices):
        p = it.permutations(slices, 2)
        for s1, s2 in p:
            if s1.overlaps(s2):
                return False
        return True

    def cut(self, slices):
        self.slices = slices
        return self.num_cells_in_slices

    def write_output(self):
        self.output_file.write(self.slices)
