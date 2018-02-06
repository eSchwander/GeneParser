import numpy

class GeneStats:
    def __init__(self, name):
        self.name = name
        self.values = {"BEG": [], "MID": [], "END": []}
        self.means = {"BEG": 0, "MID": 0, "END": 0}

    def find_means(self):
        for k in self.values:
            self.means[k] = numpy.mean(self.values[k])
