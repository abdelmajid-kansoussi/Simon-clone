import pygame, sys, time, random
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600

FPS = 30
BUTTONSIZE = 200
GAP = 10

FLASHDELAY = 100
TIMEOUT = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
BRIGHTRED = (255, 0, 0)
GREEN = (0, 155 , 0)
BRIGHTGREEN = (0, 255, 0)
BLUE = (0, 0, 155)
BRIGHTBLUE = (0, 0, 255)
YELLOW = (155, 155, 0)
BRIGHTYELLOW = (255, 255, 0)

XMARGIN = (WINDOWWIDTH - 2 * BUTTONSIZE) / 2
YMARGIN = (WINDOWHEIGHT - 2 * BUTTONSIZE) / 2

def main():
    global DISPLAYSURF, REDRECT, BLUERECT, GREENRECT, YELLOWRECT, CLOCK, BEEP1, BEEP2, BEEP3, BEEP4
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Simon clone")
    CLOCK = pygame.time.Clock()

    BEEP1 = pygame.mixer.Sound("beep1.ogg")
    BEEP2 = pygame.mixer.Sound("beep2.ogg")
    BEEP3 = pygame.mixer.Sound("beep3.ogg")
    BEEP4 = pygame.mixer.Sound("beep4.ogg")

    REDRECT = pygame.Rect(XMARGIN - GAP, YMARGIN - GAP, BUTTONSIZE, BUTTONSIZE)
    YELLOWRECT = pygame.Rect(XMARGIN + BUTTONSIZE + GAP, YMARGIN - GAP, BUTTONSIZE, BUTTONSIZE)
    GREENRECT = pygame.Rect(XMARGIN - GAP, YMARGIN + BUTTONSIZE + GAP, BUTTONSIZE, BUTTONSIZE)
    BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + GAP, YMARGIN + BUTTONSIZE + GAP, BUTTONSIZE, BUTTONSIZE)

    FONT = pygame.font.Font("freesansbold.ttf", 20)

    pattern = []
    currentStep = 0
    waitingForInput = False
    score = 0
    lastTimeClick = 0

    while True:
        SCORESURF = FONT.render("score: " + str(score), False, WHITE)
        SCORERECT = SCORESURF.get_rect()
        SCORERECT.topleft = (WINDOWWIDTH - 100, 25)

        clickedButton = None
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(SCORESURF, SCORERECT)
        drawButtons()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                clickedButton = getClickedButton(event.pos[0], event.pos[1])
            
        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((BLUE, RED, YELLOW, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True

        else:
            if clickedButton and pattern[currentStep] == clickedButton:
                flashButtonAnimation(clickedButton)
                lastTimeClick  = time.time()
                currentStep += 1
                if currentStep == len(pattern):
                    currentStep = 0
                    score += 1
                    waitingForInput = False

            elif (clickedButton and pattern[currentStep] != clickedButton) or (time.time() - lastTimeClick > TIMEOUT and currentStep != 0):
                gameOverAnimation()
                currentStep = 0
                pattern = []
                score = 0
                waitingForInput = False
                pygame.time.wait(1000)

        pygame.display.update()
        CLOCK.tick(FPS)


def drawButtons():
        pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
        pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
        pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)
        pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)


def getClickedButton(left, top):
    if REDRECT.collidepoint(left, top):
        return RED
    if BLUERECT.collidepoint(left, top):
        return BLUE
    if GREENRECT.collidepoint(left, top):
        return GREEN
    if YELLOWRECT.collidepoint(left, top):
        return YELLOW


def flashButtonAnimation(color, animationSpeed = 50):
    if color == RED:
        rect = REDRECT
        flashColor = BRIGHTRED
        sound = BEEP1
    if color == GREEN:
        rect = GREENRECT
        flashColor = BRIGHTGREEN
        sound = BEEP2
    if color == BLUE:
        rect = BLUERECT
        flashColor = BRIGHTBLUE
        sound = BEEP3
    if color == YELLOW:
        rect = YELLOWRECT
        flashColor = BRIGHTYELLOW
        sound = BEEP4

    sound.play()

    originalSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor

    for start , end , step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rect.topleft)
            pygame.display.update()
            CLOCK.tick(FPS)

    DISPLAYSURF.blit(originalSurf, (0, 0))

def gameOverAnimation(color = WHITE, animationSpeed = 50):
    originalSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = color

    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()

    for i in range(3):
        for start , end , step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, step * animationSpeed):
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(originalSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                CLOCK.tick(FPS)


main()