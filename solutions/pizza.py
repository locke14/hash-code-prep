#!/usr/bin/python3

from cfg import DEBUG


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


class Pizza:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.content = self.input_file.content
        self.slices = []

    def num_slices(self):
        return len(self.slices)

    def add_slice(self, r1, c1, r2, c2):
        s = Slice(self, r1, c1, r2, c2)
        self.slices.append(s)

        if DEBUG:
            print("Slice: " + str(self.num_slices()))
            print(s.content)
            print("Number of cells: " + str(s.num_cells))
            print("Number of tomato cells (T): " + str(s.num_cells_tomato))
            print("Number of mushroom cells (M): " + str(s.num_cells_mushroom))
            print("*"*10)

    def write_output(self):
        self.output_file.write(self.slices)
