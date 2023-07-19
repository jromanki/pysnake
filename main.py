'''--- pySnake - A Simple Snake Clone Made in Pygame by jromanki --- https://github.com/jromanki ---'''


import pygame, sys, random
pygame.font.init()

WIDTH, HEIGHT = 400, 400
FONT = pygame.font.SysFont('comicsans', 50)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pySnake")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (20, 20, 20)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

SQARE_SIZE = 18
LINE_WIDTH = 2
GAMESPEEDMOD = 6    # The higher the slower the game speeds up


def createGrid(grid):
    for x in range(0, (WIDTH//(SQARE_SIZE+LINE_WIDTH))):
        row = []
        for y in range(0, (HEIGHT//(SQARE_SIZE+LINE_WIDTH))):
            row.append([y, 'dead'])
        grid.append(row)
    return grid


def handleMovement(grid, direction, head, width, height):
    grid[head[0]][head[1]][1] = 'dead'
    
    if direction == 'R':
        head[0] += 1
        if head[0] > width:
            head[0] = 0
    if direction == 'L':
        head[0] -= 1
        if head[0] < 0:
            head[0] = width
    if direction == 'D':
        head[1] += 1
        if head[1] > height:
            head[1] = 0
    if direction == 'U':
        head[1] -= 1
        if head[1] < 0:
            head[1] = height
    return grid, head


def makeTail(grid, head, tail, tailLength):
    
    if len(tail) <= tailLength:
        tail.append(head.copy())
    else:
        grid[tail[0][0]][tail[0][1]][1] = 'dead'
        tail.pop(0)
        tail.append(head.copy())
    return grid, tail


def handleColisions(head, tail):
    for i, segment in enumerate(tail):
        if i == len(tail) - 1:
            continue
        if segment[0] == head[0] and segment[1] == head[1]:
            return True


def handleFood(grid, tail, food, tailLength, width, height, gameSpeed):
    if len(food) < 1:
        food = [random.randint(0, width), random.randint(0, height)]
    for i, segment in enumerate(tail):
        if segment == food:
            tailLength += 1
            if tailLength % GAMESPEEDMOD == GAMESPEEDMOD - 1:
                gameSpeed += 1
            food = []
    return food, tailLength, gameSpeed


def drawGrid(grid, head, tail, food, tailLength, run):
    WIN.fill(GREY)

    grid[head[0]][head[1]][1] = 'head'

    for i in tail:
        grid[i[0]][i[1]][1] = 'tail'
    
    if len(food) != 0:
        grid[food[0]][food[1]][1] = 'food'

    for x, row in enumerate(grid):
        for y, column in enumerate(row):
            square = pygame.Rect(x*(SQARE_SIZE+LINE_WIDTH), column[0]*(SQARE_SIZE+LINE_WIDTH), SQARE_SIZE, SQARE_SIZE)
            if row[y][1] == 'head':
                pygame.draw.rect(WIN, RED, square)
            elif row[y][1] == 'tail':
                pygame.draw.rect(WIN, RED, square)
            elif row[y][1] == 'food':
                pygame.draw.rect(WIN, GREEN, square)
            else:
                pygame.draw.rect(WIN, BLACK, square)
            
    scoreText = FONT.render(str(tailLength), 1, WHITE)
    WIN.blit(scoreText, ((WIDTH - scoreText.get_width())/2, 50))

    if run == False:
        gameOver = FONT.render('Game Over!', 1, WHITE)
        WIN.blit(gameOver, ((WIDTH - gameOver.get_width())/2, (HEIGHT - gameOver.get_height())/2))

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    grid = []       # A list containing all possible positions
    tail = []       # A list consisting of head's previous positions (Empty at the begining)
    food = []       # The position of the food
    tailLength = 0
    direction, prevDir,  = '', ''

    grid = createGrid(grid)

    width = len(grid) - 1
    height = len(grid[0]) - 1
    head = [width//2, height//2]  # Player's starting position, head of the snake
    
    gameSpeed = 7 # Initial game speed

    while run:
        clock.tick(gameSpeed) # The game increases in difficulty by increasing FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                # The prevDir variable prevents backing off the snake (This would mean colision with the tail)
                if event.key == pygame.K_UP and prevDir != 'D':
                    direction = 'U'
                if event.key == pygame.K_DOWN and prevDir != 'U':
                    direction = 'D'
                if event.key == pygame.K_LEFT and prevDir != 'R':
                    direction = 'L'
                if event.key == pygame.K_RIGHT and prevDir != 'L':
                    direction = 'R'

        prevDir = direction
        grid, head = handleMovement(grid, direction, head, width, height)
        grid, tail = makeTail(grid, head, tail, tailLength)

        food, tailLength, gameSpeed = handleFood(grid, tail, food, tailLength, width, height, gameSpeed)

        if handleColisions(head, tail) == True:
            run = False

        drawGrid(grid, head, tail, food, tailLength, run)
    
    pygame.time.delay(1000)
    main()


if __name__ == "__main__":
    main()