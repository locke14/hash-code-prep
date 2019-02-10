#!/usr/bin/python3

from input_file import InputFile
from output_file import OutputFile


class PizzaSlicer:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def slice_pizza(self):
        pass

    def write_output(self):
        self.output_file.num_slices = 3
        self.output_file.add_slice(0, 0, 2, 1)
        self.output_file.add_slice(0, 2, 2, 2)
        self.output_file.add_slice(0, 3, 2, 4)
        self.output_file.write()


def run():
    a_in = InputFile('./../datasets/a_example.in')
    a_out = OutputFile('./../datasets/a_example.out')

    solver = PizzaSlicer(a_in, a_out)
    solver.slice_pizza()
    solver.write_output()


if __name__ == "__main__":
    run()
