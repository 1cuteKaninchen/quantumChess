from quantumPiece import QuantumPiece
import random


def inRange(coordinate):
    if coordinate[0] < 0 or coordinate[0] > 7 or coordinate[1] < 0 or coordinate[1] > 7:
        return False
    return True


class PieceContainer:
    
    def __init__(self):
        self.pieces: list[QuantumPiece] = list()
    
    def getPiece(self, coordinate):
        for piece in self.pieces:
            if coordinate in piece.coordinates.keys():
                return piece
        return None

    def movePiece(self, coordinateFrom, coordinateTo):
        # only in cases in which a piece has only one move
        piece = self.getPiece(coordinateFrom)
        probability = piece.coordinates.pop(coordinateFrom)

        # handles captures
        self.capturePiece(coordinateTo)

        piece.coordinates[coordinateTo] = probability

    def movePiece(self, coordinateFrom, coordinateTo1, coordinateTo2):
        piece = self.getPiece(coordinateFrom)
        probability = piece.coordinates.pop(coordinateFrom)

        # handles captures
        for partMove in (coordinateTo1, coordinateTo2):
            self.capturePiece(partMove)

        # handles castling
        if piece.type == "King":
            for partMove in (coordinateTo1, coordinateTo2):
                if abs(coordinateFrom[0] - partMove[0]) == 2:
                    if partMove[0] == 2:
                        rook = self.getPiece((0, coordinateFrom[1]))
                        rook.coordinates[(0, coordinateFrom[1])] = 0.5
                        rook.coordinates[(3, coordinateFrom[1])] = 0.5
                        rook.hasMoved = True
                    if partMove[0] == 6:
                        rook = self.getPiece((7, coordinateFrom[1]))
                        rook.coordinates[(7, coordinateFrom[1])] = 0.5
                        rook.coordinates[(5, coordinateFrom[1])] = 0.5
                        rook.hasMoved = True

        # handles en passant todo

        piece.coordinates[coordinateTo1] = probability / 2
        piece.coordinates[coordinateTo2] = probability / 2
        piece.hasMoved = True

    def capturePiece(self, coordinate):
        capturedPiece = self.getPiece(coordinate)
        if capturedPiece is not None:
            if random.random() < capturedPiece.coordinates[coordinate]:
                capturedPiece.die()
            else:
                capturedPiece.coordinates.pop(coordinate)
                capturedPiece.adjustProbabilities()

    def addMovesInLine(self, coordinate, piece, xDirection, yDirection):
        moves = []
        checkTile = (coordinate[0] + xDirection, coordinate[1] + yDirection)
        while inRange(checkTile):
            if not self.getPiece(checkTile).color == piece.color:
                moves.append(checkTile)
                checkTile = (checkTile[0] + xDirection, checkTile[1] + yDirection)
            else:
                break
        return moves

    def getMoves(self, coordinate):
        piece = self.getPiece(coordinate)
        coordinates = []
        match piece.type:
            case "King":
                # collects all theoretically possible moves
                for x in (-1, 0, 1):
                    for y in (-1, 0, 1):
                        coordinates.append((coordinate[0] + x, coordinate[1] + y))
                coordinates.pop(coordinate)

                # removes all moves out of bound
                for x in coordinates:
                    if not inRange(x):
                        coordinates.remove(x)
                    # removes all moves to tiles inhibited by ur own pieces
                    else:
                        for checkPiece in self.pieces:
                            if x in checkPiece.coordinates.keys() and piece.color == checkPiece.color:
                                coordinates.remove(x)

                if not piece.hasMoved:
                    if not self.getPiece((0, coordinate[1])).hasMoved and self.getPiece((1, coordinate[1])) is None:
                        if self.getPiece((2, coordinate[1])) is None and self.getPiece((3, coordinate[1])) is None:
                            coordinates.append((2, coordinate[1]))
                    if not self.getPiece((7, coordinate[1])).hasMoved and self.getPiece((5, coordinate[1])) is None:
                        if self.getPiece((6, coordinate[1])) is None:
                            coordinates.append((6, coordinate[1]))

            case "Queen":
                for xDirection in (-1, 0, 1):
                    for yDirection in (-1, 0, 1):
                        if xDirection == yDirection == 0:
                            continue
                        coordinates.extend(self.addMovesInLine(coordinate, piece, xDirection, yDirection))

            case "Bishop":
                for xDirection in (-1, 1):
                    for yDirection in (-1, 1):
                        coordinates.extend(self.addMovesInLine(coordinate, piece, xDirection, yDirection))

            case "Rook":
                for xDirection, yDirection in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    coordinates.extend(self.addMovesInLine(coordinate, piece, xDirection, yDirection))

            case "Knight":
                for x in (-1, 1):
                    for y in (-1, 1):
                        for checkTile in ((2 * x, y), (x, 2 * y)):
                            if inRange(checkTile) and not self.getPiece(checkTile).color == piece.color:
                                coordinates.append(checkTile)

            case "Pawn":
                pass

        return coordinates
