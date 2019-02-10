#!/usr/bin/python3


class InputFile:
    def __init__(self, file_path):
        self._rows = []
        self.num_rows = 0
        self.num_cols = 0
        self.num_ingredients_min = 0
        self.num_cells_max = 0

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
        self.num_cells_max = int(line0[6])
        self.rows = [line.rstrip('\n') for line in content[1:]]

        print("Number of rows (R): " + str(self.num_rows))
        print("Number of columns (C): " + str(self.num_cols))
        print("Minimum number of each ingredient cells in each slice (L): " + str(self.num_ingredients_min))
        print("Maximum total number of cells of a slice (H): " + str(self.num_cells_max))

    @property
    def num_rows(self):
        return self._num_rows

    @num_rows.setter
    def num_rows(self, value):
        self._num_rows = value

    @property
    def num_cols(self):
        return self._num_cols

    @num_cols.setter
    def num_cols(self, value):
        self._num_cols = value

    @property
    def num_ingredients_min(self):
        return self._num_ingredients_min

    @num_ingredients_min.setter
    def num_ingredients_min(self, value):
        self._num_ingredients_min = value

    @property
    def num_cells_max(self):
        return self._num_cells_max

    @num_cells_max.setter
    def num_cells_max(self, value):
        self._num_cells_max = value

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    def print(self):
        for line in self._file:
            print(line)
