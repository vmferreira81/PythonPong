import pygame
from pygame.locals import *
from sys import exit


def startValues():
    global speed_x
    global speed_y
    global x
    global y
    global player_lost
    global score
    global high_score
    speed_x = 150
    speed_y = 150
    x = SCREEN_SIZE[0]/2
    y = 0
    player_lost = False
    score = 0


def drawBackgound():
    pygame.draw.rect(screen, tuple(colorWhite), (0, 0, 640, 480))


def drawBar():
    mx, my = pygame.mouse.get_pos()
    if ((mx + bar.get_width()) > SCREEN_SIZE[0]):
        mx = SCREEN_SIZE[0] - bar.get_width()
    screen.blit(bar, (mx, SCREEN_SIZE[1] - bar.get_height()))


def drawBall(position):
    screen.blit(ball, position)


def ballHitRight():
    return (x > SCREEN_SIZE[0] - ball.get_width())


def ballHitLeft():
    return (x < 0)


def ballHitBottom():
    return y > SCREEN_SIZE[1] - ball.get_height()


def ballHitTop():
    return y < 0


def ballHitBar():
    barX, barY = pygame.mouse.get_pos()
    return ((y > SCREEN_SIZE[1] - ball.get_height() - bar.get_height()) and ((x > barX - ball.get_width()) and (x < barX + bar.get_width() + ball.get_width())))


def drawScores():
    scoretext = small_font.render("Score = "+str(score), 1, (0,0,0))
    screen.blit(scoretext, (5, 10))
    higscoretext = small_font.render("High Score = "+str(high_score), 1, (0,0,0))
    screen.blit(higscoretext, (5, 30))

pygame.init()
clock = pygame.time.Clock()

SCREEN_SIZE = (640, 480)
colorWhite = [255, 255, 255]
colorBlack = [0, 0, 0]

youlostmessage = "You lose"
font = pygame.font.SysFont("arial", 80);
text_surface = font.render(youlostmessage, True, (0, 0, 255))

small_font = pygame.font.SysFont("monospace", 16)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

contador_surface = font.render("Score: ", True, (0, 0, 255))

bar = pygame.Surface((80, 20))
ball = pygame.Surface((20,20)).convert_alpha()
ball.fill(colorWhite)
pygame.draw.circle(ball, colorBlack, (10,10), 10)

restart_file = "restart.png"
restart_button = pygame.image.load(restart_file).convert_alpha()

startValues()
high_score = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and player_lost == True:
            if restart_rect.collidepoint(pygame.mouse.get_pos()):
                startValues()
    if  not player_lost:
        drawBackgound()
        drawBar()
        drawBall((x,y))
        drawScores()
        
    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0
    x += speed_x * time_passed_seconds 
    y += speed_y * time_passed_seconds
    
    if ballHitRight():
        speed_x = -speed_x
        x = SCREEN_SIZE[0] - ball.get_width()
    
    elif ballHitLeft():
        speed_x = -speed_x
        x = 0

    if ballHitBottom():
        screen.blit(text_surface, (SCREEN_SIZE[0]/2 - text_surface.get_width()/2, SCREEN_SIZE[1]/2 - text_surface.get_height()))
        player_lost = True   
        restart_rect = screen.blit(restart_button, (SCREEN_SIZE[0]/2 - restart_button.get_width()/2, SCREEN_SIZE[1]/2 + text_surface.get_height()/2 ))
        
    elif ballHitTop():
        speed_y = -speed_y
        y = 0
    
    if ballHitBar():
        speed_y = -speed_y
        y = SCREEN_SIZE[1] - ball.get_height() - bar.get_height()
        score += 1
        if score > high_score:
            high_score = score
        speed_x = speed_x + ( (speed_x*score+1)/80)
        speed_y = speed_y + ( (speed_y*score+1)/80)
    

    pygame.display.update()
