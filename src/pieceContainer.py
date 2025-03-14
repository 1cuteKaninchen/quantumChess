from quantumPiece import QuantumPiece
import random


def inRange(coordinate):
    if coordinate[0] < 0 or coordinate[0] > 7 or coordinate[1] < 0 or coordinate[1] > 7:
        return False
    return True


class PieceContainer:
    
    def __init__(self):
        self.pieces: list[QuantumPiece] = list()
        self.enPassant: (int, int) = ()
    
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

        # handles enPassant
        if piece.type == "pawn":
            self.handleEnPassant(coordinateFrom, coordinateTo)

        piece.coordinates[coordinateTo] = probability

    def movePiece(self, coordinateFrom, coordinateTo1, coordinateTo2):
        piece = self.getPiece(coordinateFrom)
        probability = piece.coordinates.pop(coordinateFrom)

        # handles captures
        for partMove in (coordinateTo1, coordinateTo2):
            self.capturePiece(partMove)

        # handles castling
        if piece.type == "king":
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

        # handles en passant
        if piece.type == "pawn":
            for partMove in (coordinateTo1, coordinateTo2):
                self.handleEnPassant(coordinateFrom, partMove)

        piece.coordinates[coordinateTo1] = probability / 2
        piece.coordinates[coordinateTo2] = probability / 2
        piece.hasMoved = True

    def handleEnPassant(self, coordinateFrom, move):
        if move == self.enPassant:
            if move[1] == 2:
                self.capturePiece((move[0], move[1] + 1))
            elif move[1] == 5:
                self.capturePiece((move[0], move[1] - 1))
        if abs(move[1] - coordinateFrom[1]) == 2:
            self.enPassant = (coordinateFrom[0], (coordinateFrom[1] + move[1]) / 2)

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
            case "king":
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

            case "queen":
                for xDirection in (-1, 0, 1):
                    for yDirection in (-1, 0, 1):
                        if xDirection == yDirection == 0:
                            continue
                        coordinates.extend(self.addMovesInLine(coordinate, piece, xDirection, yDirection))

            case "bishop":
                for xDirection in (-1, 1):
                    for yDirection in (-1, 1):
                        coordinates.extend(self.addMovesInLine(coordinate, piece, xDirection, yDirection))

            case "rook":
                for xDirection, yDirection in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    coordinates.extend(self.addMovesInLine(coordinate, piece, xDirection, yDirection))

            case "knight":
                for x in (-1, 1):
                    for y in (-1, 1):
                        for checkTile in ((2 * x, y), (x, 2 * y)):
                            if inRange(checkTile) and not self.getPiece(checkTile).color == piece.color:
                                coordinates.append(checkTile)

            case "pawn":
                if piece.color == "black":
                    direction = -1
                else:
                    direction = 1
                checkTile = (coordinate[0], coordinate[1] + direction)
                if inRange(checkTile) and self.getPiece(checkTile) is None:
                    coordinates.append(checkTile)
                    if not piece.hasMoved:
                        checkTile = (coordinate[0], coordinate[1] + direction * 2)
                        if inRange(checkTile) and self.getPiece(checkTile) is None:
                            coordinates.append(checkTile)
                for x in (-1, 1):
                    checkTile = (coordinate[0] + x, coordinate[1] + direction)
                    if inRange(checkTile):
                        if self.getPiece(checkTile) is not None and self.getPiece(checkTile).color != piece.color:
                            coordinates.append(checkTile)
                        elif checkTile == self.enPassant:
                            coordinates.append(checkTile)

        return coordinates
