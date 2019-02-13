#!/usr/bin/python3


from file_io import InputFile, OutputFile
from pizza import Pizza, Slice
from constraint import *
from cfg import *
from utils import log
import operator


class PizzaSlicer:
    def __init__(self, dataset):
        input_file = InputFile(DATASETS_PATH + dataset + INPUT_FORMAT)
        output_file = OutputFile(DATASETS_PATH + dataset + OUTPUT_FORMAT)
        self.pizza = Pizza(input_file, output_file)

    def get_valid_slices(self):
        log(f"Finding all valid slices...")

        p = Problem()
        p.addVariable("r1", range(0, self.pizza.num_rows))
        p.addVariable("c1", range(0, self.pizza.num_cols))
        p.addVariable("r2", range(0, self.pizza.num_rows))
        p.addVariable("c2", range(0, self.pizza.num_cols))

        p.addConstraint(self.pizza.is_valid_slice, ["r1", "c1", "r2", "c2"])
        valid_slices = p.getSolutions()
        log(f"Found {len(valid_slices)} total valid slices")

        return [Slice(self.pizza, s['r1'], s['c1'], s['r2'], s['c2']) for s in valid_slices]

    def get_valid_cuts(self, valid_slices, num_slices):
        log(f"Finding valid cuts with {num_slices} slices...")

        p = Problem()
        slice_vars = [f"slice_{i}" for i in range(num_slices)]

        for var in slice_vars:
            p.addVariable(var, valid_slices)

        for i in range(num_slices):
            for j in range(num_slices):
                if i != j:
                    p.addConstraint(FunctionConstraint(self.pizza.is_valid_cut), [slice_vars[i], slice_vars[j]])

        valid_cuts_iter = p.getSolutionIter()
        valid_cuts = list(next(valid_cuts_iter) for _ in range(N))
        valid_cuts = [tuple(c.values()) for c in valid_cuts]

        log(f"Took first {N} valid cuts with {num_slices} slices")
        # log(f"Found {len(valid_cuts)} valid cuts with {num_slices} slices")

        return {cut: self.pizza.cut(cut) for cut in valid_cuts}

    def slice_pizza(self):
        valid_slices = self.get_valid_slices()

        num_slices_min = self.pizza.num_slices_min
        num_slices_max = 10  # self.pizza.num_slices_max

        valid_cuts_all = {}
        for i in range(num_slices_min, num_slices_max + 1):
            valid_cuts = self.get_valid_cuts(valid_slices, i)
            if len(valid_cuts) == 0:
                break
            valid_cuts_all = {**valid_cuts, **valid_cuts_all}

        best_cut = max(valid_cuts_all.items(), key=operator.itemgetter(1))[0]
        log("Best cut with total number of cells: " + str(self.pizza.cut(best_cut)))
        self.pizza.write_output()


def run():
    solver = PizzaSlicer(DATASET_B)
    solver.slice_pizza()


if __name__ == "__main__":
    run()
