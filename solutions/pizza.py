#!/usr/bin/python3

from cfg import log


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
        if self.c1 >= other.c2 or self.c2 <= other.c1:
            return False
        if self.r1 >= other.r2 or self.r2 <= other.r1:
            return False
        return True


class Pizza:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.content = self.input_file.content
        self.slices = []

    def num_slices(self):
        return len(self.slices)

    def overlaps(self, new_slice):
        for s in self.slices:
            if s.overlaps(new_slice):
                return True
        return False

    def slice(self, r1, c1, r2, c2):
        s = Slice(self, r1, c1, r2, c2)

        log("*************************************")
        log("Slice: " + str(self.num_slices()))
        log(s.content)
        log("Number of cells: " + str(s.num_cells))
        log("Number of tomato cells (T): " + str(s.num_cells_tomato))
        log("Number of mushroom cells (M): " + str(s.num_cells_mushroom))

        if s.num_cells_tomato < self.input_file.num_ingredients_min:
            log("Too few tomato cells :(")
            return False

        if s.num_cells_mushroom < self.input_file.num_ingredients_min:
            log("Too few mushroom cells :(")
            return False

        if s.num_cells > self.input_file.num_cells_max:
            log("Too many cells :(")
            return False

        if self.overlaps(s):
            log("Overlaps with existing cells :(")
            return False

        log("Valid pizza slice :)")

        self.slices.append(s)
        return True

    def write_output(self):
        self.output_file.write(self.slices)
