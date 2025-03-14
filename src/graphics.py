import sys
import pygame

import pygame_menu.themes
from pygame.locals import *

from game import Game

SQUARE_SIZE = 80
SCREEN_SIZE = (640, 640)

PIECE_SIZE = (56, 56)
PIECE_OFFSET = 12
PROBABILITY_OFFSET = 4

CIRCLE_RADIUS = 16
CIRCLE_OFFSET = 40

PLAY_AGAIN_TEXT_POSITION = (80, 160)

FONT_COLOR = (0, 0, 127)

colors = (
    ((238, 213, 183), (160, 82, 45), (236, 51, 10)),
    ((245, 255, 250), (189, 252, 201), (126, 51, 10))
)

skins_list = [
    ("Wooden", 0),
    ("Minty", 1)

]


class UI:
    def __init__(self, game: Game):
        pygame.init()
        pygame.font.init()
        self.menu = None
        self.game: Game = game
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.skinIndex = 0
        self.spritesList = dict()
        self.menuBackground = pygame.image.load("images/menu/borgar.png")
        self.font = pygame.font.SysFont('Comic Sans MS', 10)
        self.endFont = pygame.font.SysFont('Comic Sans MS', 64)
        self.light = (255, 255, 255)
        self.dark = (0, 0, 0)
        self.possibleMoveColor = (127, 127, 127)

    def __draw_board(self):
        for row in range(8):
            for column in range(8):
                # Determines the background colors
                color = self.dark if (row+column) % 2 else self.light
                pygame.draw.rect(
                    self.screen,
                    color,
                    (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def __drawPieces(self):
        for piece in self.game.board.pieces:
            path = "images/" + piece.color + "/" + piece.type + ".gif"
            for tile in piece.coordinates.keys():
                image = pygame.image.load(path)
                imageResized = pygame.transform.scale(image, PIECE_SIZE)
                self.screen.blit(imageResized, (tile[0] * SQUARE_SIZE + PIECE_OFFSET, (7 - tile[1]) * SQUARE_SIZE + PIECE_OFFSET))
                probText = self.font.render(str(piece.coordinates[tile])[0:7], True, (31, 31, 31))
                self.screen.blit(probText, (tile[0] * SQUARE_SIZE + PROBABILITY_OFFSET, (7 - tile[1]) * SQUARE_SIZE))
                idText = self.font.render(str(piece.pieceId), True, (31, 31, 31))
                self.screen.blit(idText, (tile[0] * SQUARE_SIZE + PROBABILITY_OFFSET, (7 - tile[1]) * SQUARE_SIZE + 32))

    def __drawLegalMoves(self):
        pygame.draw.circle(self.screen, (0, 0, 0), (self.game.selectedTileFrom[0] * SQUARE_SIZE + CIRCLE_OFFSET, (7 - self.game.selectedTileFrom[1]) * SQUARE_SIZE + CIRCLE_OFFSET), CIRCLE_RADIUS)
        for move in self.game.board.getMoves(self.game.selectedTileFrom):
            x = move[0] * SQUARE_SIZE
            y = (7 - move[1]) * SQUARE_SIZE
            if move == self.game.selectedTileTo:
                pygame.draw.rect(self.screen, self.possibleMoveColor, (x + 0.6 * CIRCLE_OFFSET, y + 0.6 * CIRCLE_OFFSET, 2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS))
                continue
            pygame.draw.circle(self.screen, self.possibleMoveColor, (x + CIRCLE_OFFSET, y + CIRCLE_OFFSET), CIRCLE_RADIUS)

    def start_menu(self):
        pygame.display.set_caption("Menu")
        customTheme = pygame_menu.themes.THEME_DARK
        customTheme.background_color = pygame_menu.baseimage.BaseImage("images/menu/borgar.png")
        customTheme.title_background_color = (0, 0, 0)
        customTheme.widget_background_color = (238, 174, 238)
        customTheme.widget_font_color = (50, 50, 50)

        self.menu = pygame_menu.Menu("", SCREEN_SIZE[0], SCREEN_SIZE[1], theme=customTheme)

        self.menu.add.button("Play", self.startMainloop)

        def changeSkin(name, index):
            self.skinIndex = index

        selId = "axsfghnya:3"
        self.menu.add.selector("Skin: ", skins_list, default=0,
                               selector_id=selId,
                               onchange=changeSkin)

        self.menu.mainloop(self.screen)

    def startMainloop(self):
        pygame.display.set_caption("White to move")
        self.light, self.dark, self.possibleMoveColor = colors[self.skinIndex][0], colors[self.skinIndex][1], colors[self.skinIndex][2]
        while True:
            if not self.game.board.hasKing("white"):
                self.handleGameOver("black")
            if not self.game.board.hasKing("black"):
                self.handleGameOver("white")
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    clickedTile = (x // SQUARE_SIZE, 7 - y // SQUARE_SIZE)
                    self.game.tileClicked(clickedTile)
                    pygame.display.set_caption("White to move" if self.game.whiteToMove else "Black to move")

            self.__draw_board()
            self.__drawPieces()
            if self.game.selectedTileFrom is not None:
                self.__drawLegalMoves()

            self.clock.tick(30)
            pygame.display.flip()

    def handleGameOver(self, winner):
        infoText = self.endFont.render(winner + " has won!", False, FONT_COLOR)
        self.screen.blit(infoText, (PLAY_AGAIN_TEXT_POSITION[0] + 40, PLAY_AGAIN_TEXT_POSITION[1]))
        infoText = self.endFont.render("press space", False, FONT_COLOR)
        self.screen.blit(infoText, (PLAY_AGAIN_TEXT_POSITION[0] + 70, PLAY_AGAIN_TEXT_POSITION[1] + 80))
        infoText = self.endFont.render("for rematch", False, FONT_COLOR)
        self.screen.blit(infoText, (PLAY_AGAIN_TEXT_POSITION[0] + 60, PLAY_AGAIN_TEXT_POSITION[1] + 160))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    print("Thanks for playing")
                    sys.exit(0)
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.__init__(Game())
                        self.start_menu()
