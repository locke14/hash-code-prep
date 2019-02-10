#!/usr/bin/python3


class OutputFile:
    def __init__(self, file_path):
        self._file = open(file_path, 'w')
        self.num_slices = 0
        self.slices = []

    def __del__(self):
        self._file.close()

    @property
    def num_slices(self):
        return self._num_slices

    @num_slices.setter
    def num_slices(self, value):
        self._num_slices = value

    def add_slice(self, r1, c1, r2, c2):
        self.slices.append(str(r1) + " "
                           + str(c1) + " "
                           + str(r2) + " "
                           + str(c2) + "\n")

    def write(self):
        lines = [str(self.num_slices) + "\n"]
        lines.extend(self.slices)
        self._file.writelines(lines)

