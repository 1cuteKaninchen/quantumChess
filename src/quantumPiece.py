class QuantumPiece():

    def __init__(self, color, pieceType):
        self.color = color
        self.coordinates = dict()
        self.hasMoved = False
        self.type = pieceType

    def adjustProbabilities(self):
        valuesTotal = 0
        for value in self.coordinates.values():
            valuesTotal += value
        for key in self.coordinates.keys():
            self.coordinates[key] = self.coordinates[key] * (1 / valuesTotal)

    def die(self):
        self.coordinates = None
