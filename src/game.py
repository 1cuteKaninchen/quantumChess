from pieceContainer import PieceContainer


class Game:
    def __init__(self):
        self.board: PieceContainer = PieceContainer()
        self.selectedTileFrom = None
        self.selectedTileTo = None
        self.whiteToMove = True

    def tileClicked(self, tile: (int, int)):
        if self.selectedTileFrom is None:
            if self.getPiece(tile) is not None:
                if self.getPiece(tile).color == "white" and self.whiteToMove:
                    self.selectedTileFrom = tile
                if self.getPiece(tile).color == "black" and not self.whiteToMove:
                    self.selectedTileFrom = tile
            return

        if tile == self.selectedTileFrom:
            self.selectedTileFrom = None
            self.selectedTileTo = None
            return

        if tile not in self.getMoves(self.selectedTileFrom):
            return

        if tile == self.selectedTileTo:
            self.selectedTileTo = None
            return

        # now we know that we clicked on a tile we can move to
        if self.selectedTileTo is None:
            possibleMoves = 0
            for move in self.getMoves(self.selectedTileFrom):
                possibleMoves += 1
            if possibleMoves == 1:
                self.board.movePiece1(self.selectedTileFrom, tile)
                self.flipWhiteToMove()
                self.selectedTileFrom = None
                return

            self.selectedTileTo = tile

        else:
            self.board.movePiece2(self.selectedTileFrom, self.selectedTileTo, tile)
            self.flipWhiteToMove()
            self.selectedTileFrom = None
            self.selectedTileTo = None

    def getMoves(self, tile):
        return self.board.getMoves(tile)

    def getPiece(self, tile):
        return self.board.getPiece(tile)

    def flipWhiteToMove(self):
        if self.whiteToMove:
            self.whiteToMove = False
        else:
            self.whiteToMove = True
