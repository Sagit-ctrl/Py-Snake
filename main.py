import pygame, sys, random
from pygame.locals import *

# Tạo sẵn các màu sắc
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
SILVER = (215, 215, 215)
YELLOW = (255, 255, 0)
EMPTY = (0, 0, 0, 0)
# Thông số cơ bản
WIDTH = 25
HEIGHT = 25
BLANK = 5
NUM_X = 20
NUM_Y = 20
WINDOWWIDTHADD = NUM_X*WIDTH + (NUM_X + 1)*BLANK + 200
WINDOWWIDTH = NUM_X*WIDTH + (NUM_X + 1)*BLANK
WINDOWHEIGHT = NUM_Y*HEIGHT + (NUM_Y + 1)*BLANK

pygame.init()
FPS = 6
fpsClock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WINDOWWIDTHADD, WINDOWHEIGHT), SRCALPHA, pygame.RESIZABLE)
pygame.display.set_caption('Snake Man')

class Board():

    def __init__(self):
        pass

    def draw(self):
        SCREEN.fill(WHITE)

        for i in range(NUM_X):
            for j in range(NUM_Y):
                color = SILVER
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                pygame.draw.rect(SCREEN, color, (x, y, WIDTH, HEIGHT))

    def update(self):
        pass

class Snake():

    def __init__(self):
        # self.location = [[int(NUM_X/2), int(NUM_Y/2)], [int(NUM_X/2), int(NUM_Y/2)+1]]
        self.location = [[int(NUM_X / 2), int(NUM_Y / 2)]]
        self.old_location = []
        self.head = []
        self.old_head = []
        self.length = 0
        self.surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), SRCALPHA)

    def draw(self):
        checkHead = True
        SCREEN.blit(self.surface, (0, 0))
        self.surface.fill(EMPTY)
        for i in self.location:
            x = BLANK * (i[0] + 1) + WIDTH * i[0]
            y = BLANK * (i[1] + 1) + HEIGHT * i[1]
            if checkHead == False:
                pygame.draw.rect(self.surface, BLACK, (x, y, WIDTH, HEIGHT))
            else:
                pygame.draw.rect(self.surface, RED, (x, y, WIDTH, HEIGHT))
            checkHead = False

    def update(self, check, point):
        direction = check

        self.old_location = self.location.copy()
        self.old_head = self.location[0].copy()
        self.head = [0, 0]
        self.location.clear()

        if direction == 1:
            self.head[0] = self.old_head[0]
            if self.old_head[1] == 0:
                self.head[1] = NUM_Y - 1
            else:
                self.head[1] = self.old_head[1] - 1
        elif direction == 2:
            if self.old_head[0] == NUM_X - 1:
                self.head[0] = 0
            else:
                self.head[0] = self.old_head[0] + 1
            self.head[1] = self.old_head[1]
        elif direction == 3:
            self.head[0] = self.old_head[0]
            if self.old_head[1] == NUM_Y - 1:
                self.head[1] = 0
            else:
                self.head[1] = self.old_head[1] + 1
        elif direction == 4:
            if self.old_head[0] == 0:
                self.head[0] = NUM_X - 1
            else:
                self.head[0] = self.old_head[0] - 1
            self.head[1] = self.old_head[1]

        self.location.append(self.head)
        if self.head[0] == point[0] and self.head[1] == point[1]:
            pass
        else:
            self.old_location.pop(-1)
        for i in self.old_location:
            self.location.append(i)

        self.length = len(self.location)
        self.old_location.clear()
        self.old_head.clear()
        # print(self.location)

    def output(self):
        return self.location

    def length(self):
        self.length = len(self.location)
        return self.length

class Point():

    def __init__(self):
        self.x = random.randrange(0, NUM_X, 1)
        self.y = random.randrange(0, NUM_Y, 1)
        self.position = [0, 0]
        self.point = 0

    def draw(self, length):
        direc_x = BLANK * (self.x + 1) + WIDTH * self.x
        direc_y = BLANK * (self.y + 1) + HEIGHT * self.y
        self.point += 1
        if length % 5 == 0:
            if self.point % 2 == 0:
                pygame.draw.rect(SCREEN, GREEN, (direc_x, direc_y, WIDTH, HEIGHT))
            else:
                pygame.draw.rect(SCREEN, YELLOW, (direc_x, direc_y, WIDTH, HEIGHT))
        else:
            pygame.draw.rect(SCREEN, BLUE, (direc_x, direc_y, WIDTH, HEIGHT))

    def update(self, SnakeLocation):
        checkSnake = list(SnakeLocation)
        checkPoint = True

        if checkSnake[0][0] == self.x and checkSnake[0][1] == self.y:
            self.x = random.randrange(0, NUM_X, 1)
            self.y = random.randrange(0, NUM_Y, 1)
            self.position = [self.x, self.y]
        else:
            while checkPoint:
                for i in range(len(checkSnake)):
                    if checkSnake[i][0] == self.x and checkSnake[i][1] == self.y:
                        checkPoint = True
                    else:
                        checkPoint = False
                if checkPoint == True:
                    self.x = random.randrange(0, NUM_X, 1)
                    self.y = random.randrange(0, NUM_Y, 1)
                    self.position = [self.x, self.y]
    def output(self):
        return self.position

class Score():

    def __init__(self):
        self.score = 0
        self.addScore = True

    def draw(self):
        font = pygame.font.SysFont('consolas', 40)
        scoreSurface = font.render(str(self.score), True, (0, 0, 0))
        textSize = scoreSurface.get_size()
        cor_y = WINDOWWIDTH + (200 - textSize[0])/2
        SCREEN.blit(scoreSurface, (cor_y, 100))

    def update(self, location):
        if location.count(location[0]) == 2:
            self.addScore = False

        x = len(location)
        self.score = x + int((x - 1) / 5) * 4

    def output(self):
        return self.addScore

    def score(self):
        return self.score

font1 = pygame.font.Font(None, 32)
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = SILVER
        self.text = text
        self.txt_surface = font1.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = YELLOW if self.active else SILVER
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_SPACE:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        # Re-render the text.
        self.txt_surface = font1.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def output(self):
        return self.text

def rank(player, listRank):
    Rank = []
    listScore = []
    listRank = list(listRank)
    listRank.append(player)
    for i in range(len(listRank)):
        listScore.append(listRank[i][1])

    listScore.sort(reverse=True)
    for i in range(len(listScore)):
        for j in range(len(listRank)):
            if listRank[j][1] == listScore[i]:
                Rank.append(listRank[j])
    listRank = list(Rank[:5])
    return listRank

def name():
    input_box1 = InputBox(int((WINDOWWIDTHADD - 200) / 2), 300, 140, 32)
    done = False

    font = pygame.font.SysFont('consolas', 40)
    quesSuface = font.render("What is your name ?", True, RED)
    quesSize = quesSuface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    done = True
            input_box1.handle_event(event)
        input_box1.update()
        input_box1.draw(SCREEN)

        SCREEN.blit(quesSuface, (int((WINDOWWIDTHADD - quesSize[0]) / 2), 200))
        if done == True:
            return input_box1.output()

        pygame.display.update()
        fpsClock.tick(FPS)

def gameStart(name):
    i = 0

    font = pygame.font.SysFont('consolas', 100)
    headingSuface = font.render('SNAKE MAN', True, RED)
    headingSize = headingSuface.get_size()

    font = pygame.font.SysFont('consolas', 40)
    nameSuface = font.render("Hello " + str(name), True, BLUE)
    nameSize = nameSuface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return

        if i == 0:
            color = BLACK
        elif i == 1:
            color = YELLOW
        elif i == 2:
            color = BLUE
        else:
            color = GREEN
        i += 1
        if i == 4:
            i = 0

        font = pygame.font.SysFont('consolas', 30)
        commentSuface = font.render('Click "space" to continue', True, color)
        commentSize = commentSuface.get_size()

        SCREEN.fill(WHITE)
        SCREEN.blit(headingSuface, (int((WINDOWWIDTHADD - headingSize[0]) / 2), 100))
        SCREEN.blit(nameSuface, (int((WINDOWWIDTHADD - nameSize[0]) / 2), 200))
        SCREEN.blit(commentSuface, (int((WINDOWWIDTHADD - commentSize[0]) / 2), 400))

        pygame.display.update()
        fpsClock.tick(FPS)

def gamePlay(board, snake, point, score):
    check = 2
    checkDirec = False
    snake.__init__()
    board.__init__()
    score.__init__()
    point.__init__()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if checkDirec == True:
                    if event.key == K_RIGHT:
                        check = 2
                        checkDirec = False
                    elif event.key == K_LEFT:
                        check = 4
                        checkDirec = False
                if checkDirec == False:
                    if event.key == K_UP:
                        check = 1
                        checkDirec = True
                    elif event.key == K_DOWN:
                        check = 3
                        checkDirec = True

        SCREEN.fill(WHITE)

        board.draw()
        point.update(snake.output())
        point.draw(snake.length)
        snake.update(check, point.output())
        snake.draw()
        score.update(snake.output())
        score.draw()

        if snake.length > 2:
            if score.output() == False:
                return

        FPS = 6 + snake.length/10
        pygame.display.update()
        fpsClock.tick(FPS)

def gameEnd(listRank):
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('CONGRATULATION', True, RED)
    headingSize = headingSuface.get_size()

    font = pygame.font.SysFont('consolas', 40)
    rankSuface = font.render('Rank', True, BLACK)
    rankSize = rankSuface.get_size()

    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to replay', True, BLACK)
    commentSize = commentSuface.get_size()

    BACK = pygame.image.load("image/back3.png")
    backSize = BACK.get_size()
    SCREEN.blit(BACK, (int((WINDOWWIDTHADD-backSize[0])/2), int((WINDOWHEIGHT-backSize[1])/2)))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return

        checkFirst = True
        for i in range(len(listRank)):
            name = listRank[i][0]
            score = listRank[i][1]
            font = pygame.font.SysFont('consolas', 40)
            if checkFirst == True:
                color = RED
            else:
                color = BLACK
            checkFirst = False
            nameSurface = font.render(name, True, color)
            scoreSurface = font.render(str(score), True, color)
            nameSize = nameSurface.get_size()
            scoreSize = scoreSurface.get_size()

            cor_name =  (WINDOWWIDTHADD/4 - nameSize[0]) / 2 + WINDOWWIDTHADD/4
            cor_score = (WINDOWWIDTHADD/4 - scoreSize[0]) / 2 + WINDOWWIDTHADD/2
            cor_y = 200 + nameSize[1]*1.5*i

            SCREEN.blit(nameSurface, (cor_name, cor_y))
            SCREEN.blit(scoreSurface, (cor_score, cor_y))

        SCREEN.blit(headingSuface, (int((WINDOWWIDTHADD - headingSize[0]) / 2), 75))
        SCREEN.blit(rankSuface, (int((WINDOWWIDTHADD - rankSize[0]) / 2), 150))
        SCREEN.blit(commentSuface, (int((WINDOWWIDTHADD - commentSize[0]) / 2), 500))

        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    board = Board()
    snake = Snake()
    point = Point()
    score = Score()
    listRank = [["A", 0], ["B", 0], ["C", 0], ["D", 0], ["E", 0]]

    while True:
        name1 = name()
        gameStart(name1)
        gamePlay(board, snake, point, score)
        Rank = rank([name1, score.score], listRank)
        listRank = Rank.copy()
        print(listRank)
        gameEnd(listRank)
        SCREEN.fill(BLACK)

if __name__ == '__main__':
    main()
