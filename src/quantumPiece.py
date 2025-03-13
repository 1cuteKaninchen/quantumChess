from abc import ABC


class QuantumPiece(ABC):

    def __init__(self, color):
        self.color = color
        self.coordinates = dict()

    def adjustProbabilities(self):
        valuesTotal = 0
        for value in self.coordinates.values():
            valuesTotal += value
        for key in self.coordinates.keys():
            self.coordinates[key] = self.coordinates[key] * (1 / valuesTotal)
