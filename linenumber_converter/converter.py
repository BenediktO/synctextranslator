import difflib

class LineNumberConverter:
    def __init__(self, dataA, dataB, interpolate = True):
        if type(dataA) != list:
            with open(dataA) as f:
                self.dataA = f.readlines()
        else:
            self.dataA = dataA

        if type(dataB) != list:
            with open(dataB) as f:
                self.dataB = f.readlines()
        else:
            self.dataB = dataB

        self.interpolate = interpolate

        self.differ = difflib.SequenceMatcher()
        self.differ.set_seqs(self.dataA, self.dataB)

        self.linesA = []
        self.linesB = []


        for block in self.differ.get_matching_blocks():
            a, b, size = block.a, block.b, block.size
            for i in range(max(size, 1)):
                self.linesA.append(a + i)
                self.linesB.append(b + i)

        self.translater = {line_a: line_b for line_a, line_b in zip(self.linesA, self.linesB)}
        self.translater_inv = {line_b: line_a for line_a, line_b in zip(self.linesA, self.linesB)}

        if self.interpolate:
            self.translater = self.interpolate_dict(self.translater)
            self.translater_inv = self.interpolate_dict(self.translater_inv)

    def get_next_values(self, array, value):
        for a in array:
            if a > value:
                max_ = a
                break
        for a in array[::-1]:
            if a < value:
                min_ = a
                break
        return min_, max_

    def interpolate_dict(self, dict):
        keys = sorted(list(dict.keys()))
        min_ = min(keys)
        max_ = max(keys)
        for i in range(min_, max_ + 1):
            if not i in keys:
                next_min, next_max = self.get_next_values(keys, i)
                dict[i] = i / (next_max - next_min)
        return dict

    def convert(self, line):
        return self.translater.get(line, None)

    def convert_inv(self, line):
        return self.translater_inv.get(line, None)
