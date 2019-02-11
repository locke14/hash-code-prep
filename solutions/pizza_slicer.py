#!/usr/bin/python3


from file_io import InputFile, OutputFile
from pizza import Pizza
from cfg import *


class PizzaSlicer:
    def __init__(self, dataset):
        input_file = InputFile(DATASETS_PATH + dataset + INPUT_FORMAT)
        output_file = OutputFile(DATASETS_PATH + dataset + OUTPUT_FORMAT)
        self.pizza = Pizza(input_file, output_file)

    def slice_pizza(self):
        self.pizza.add_slice(0, 0, 2, 1)
        self.pizza.add_slice(0, 2, 2, 2)
        self.pizza.add_slice(0, 3, 2, 4)
        self.pizza.write_output()


def run():
    solver = PizzaSlicer(DATASET_A)
    solver.slice_pizza()


if __name__ == "__main__":
    run()
