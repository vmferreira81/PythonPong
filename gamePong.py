import pygame
from pygame.locals import *
from sys import exit


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SCREEN_SIZE = (640, 480)


class Bar(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect.y = SCREEN_SIZE[1] - height

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def update_pos(self):
        mx, my = pygame.mouse.get_pos()
        if ((mx + bar.get_width()) > SCREEN_SIZE[0]):
            mx = SCREEN_SIZE[0] - bar.get_width()
        self.rect.x = mx


class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, color, (10, 10), 10)

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def update_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


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
    pygame.draw.rect(screen, tuple(WHITE), (0, 0, 640, 480))


def ballHitRight():
    return (x > SCREEN_SIZE[0] - ball.get_width())


def ballHitLeft():
    return (x < 0)


def ballHitBottom():
    return y > SCREEN_SIZE[1] - ball.get_height()


def ballHitTop():
    return y < 0


def ballHitBar():
    return len(pygame.sprite.spritecollide(ball, sprites, False)) > 0


def drawScores():
    scoretext = small_font.render("Score = "+str(score), 1, (0,0,0))
    screen.blit(scoretext, (5, 10))
    higscoretext = small_font.render("High Score = "+str(high_score), 1, (0,0,0))
    screen.blit(higscoretext, (5, 30))

pygame.init()
clock = pygame.time.Clock()

youlostmessage = "You lose"
font = pygame.font.SysFont("arial", 80);
text_surface = font.render(youlostmessage, True, (0, 0, 255))

small_font = pygame.font.SysFont("monospace", 16)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

contador_surface = font.render("Score: ", True, (0, 0, 255))

restart_file = "restart.png"
restart_button = pygame.image.load(restart_file).convert_alpha()

startValues()
high_score = 0
bar = Bar(BLACK, 80, 20)
ball = Ball(BLACK, 20, 20)

sprites = pygame.sprite.Group()
sprites.add(bar)
sprites.draw(screen)

spriteBall = pygame.sprite.Group()
spriteBall.add(ball)
spriteBall.draw(screen)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and player_lost is True:
            if restart_rect.collidepoint(pygame.mouse.get_pos()):
                startValues()
    if not player_lost:
        drawBackgound()
        bar.update_pos()
        ball.update_pos(x, y)
        sprites.draw(screen)
        spriteBall.draw(screen)
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
