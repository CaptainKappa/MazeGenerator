import math
import pygame
from random import randint
from collections import deque

WINDOW_WIDTH = 401
WINDOW_HEIGHT = 401
BLOCK_SIZE = 20
COLUMNS = math.floor(WINDOW_WIDTH / BLOCK_SIZE)
ROWS = math.floor(WINDOW_HEIGHT / BLOCK_SIZE)

grid = []
neighbours = []
stack = deque()


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.borders = [True, True, True, True]
        self.visited = False
        self.lead = False


    def drawCell(self, win):
        if self.visited:
            pygame.draw.rect(win, (50, 168, 82), [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
            if self.lead:
                pygame.draw.rect(win, (168, 50, 140), [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

        # TOP LINE
        if self.borders[0]:
            pygame.draw.line(win, (0, 0, 0), [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE],
                             [self.x * BLOCK_SIZE + BLOCK_SIZE, self.y * BLOCK_SIZE])
        # RIGHT LINE
        if self.borders[1]:
            pygame.draw.line(win, (0, 0, 0), [self.x * BLOCK_SIZE + BLOCK_SIZE, self.y * BLOCK_SIZE],
                             [self.x * BLOCK_SIZE + BLOCK_SIZE, self.y * BLOCK_SIZE + BLOCK_SIZE])
        # BOTTOM LINE
        if self.borders[2]:
            pygame.draw.line(win, (0, 0, 0), [self.x * BLOCK_SIZE + BLOCK_SIZE, self.y * BLOCK_SIZE + BLOCK_SIZE],
                             [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE + BLOCK_SIZE])
        # LEFT LINE
        if self.borders[3]:
            pygame.draw.line(win, (0, 0, 0), [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE + BLOCK_SIZE],
                             [self.x * BLOCK_SIZE, self.y * BLOCK_SIZE])


    def checkNeighbours(self):
        neighbours = []

        cellTop = getCell(getIndex(self.x, self.y - 1))
        cellRight = getCell(getIndex(self.x + 1, self.y))
        cellBottom = getCell(getIndex(self.x, self.y + 1))
        cellLeft = getCell(getIndex(self.x - 1, self.y))

        if cellTop is not None and not cellTop.visited:
            neighbours.append(cellTop)
        if cellRight is not None and not cellRight.visited:
            neighbours.append(cellRight)
        if cellBottom is not None and not cellBottom.visited:
            neighbours.append(cellBottom)
        if cellLeft is not None and not cellLeft.visited:
            neighbours.append(cellLeft)

        return neighbours


    def removeWalls(self, neighbour):
        diffX = self.x - neighbour.x
        diffY = self.y - neighbour.y

        if diffX == -1:
            self.borders[1] = False
            neighbour.borders[3] = False
        if diffX == 1:
            self.borders[3] = False
            neighbour.borders[1] = False
        if diffY == -1:
            self.borders[2] = False
            neighbour.borders[0] = False
        if diffY == 1:
            self.borders[0] = False
            neighbour.borders[2] = False

# END CLASS CELL

def getIndex(x, y):
    index = None
    if x < 0 or x > COLUMNS - 1 or y < 0 or y > ROWS - 1:
        index = -1
        return -1

    index = x + y * COLUMNS
    return index


def getCell(index):
    cell = None

    if not index == -1:
        cell = grid[index]

    return cell


def drawDisplay(win, grid):
    for i in range(len(grid)):
        grid[i].drawCell(win)
    pygame.display.update()


def main():
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # initialize grid with cells
    for y in range(ROWS):
        for x in range(COLUMNS):
            grid.append(Cell(x, y))

    # 1st step
    current = grid[0]
    current.visited = True
    stack.append(current)

    running = True
    while running:
        clock.tick(100)
        # 2nd step
        if len(stack) > 0:
            # 2.1
            current = stack.pop()
            current.lead = True

            drawDisplay(win, grid)
            current.lead = False

            # 2.2
            neighbours = current.checkNeighbours()
            if len(neighbours) > 0:
                # 2.2.1
                stack.append(current)
                # 2.2.2
                chosenNeighbour = neighbours[randint(0, len(neighbours) - 1)]
                # 2.2.3
                current.removeWalls(chosenNeighbour)
                # 2.2.4
                chosenNeighbour.visited = True
                stack.append(chosenNeighbour)
        else:
            # stack == 0 -> all cells visited
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
    quit()


main()
