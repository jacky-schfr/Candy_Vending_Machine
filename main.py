import pygame
import random

pygame.init()

CANDY_COLORS = {
    "PEACH": (250, 150, 130),
    "BLUEBERRY": (123, 123, 230),
    "CHERRY": (255, 109, 150),
    "LEMON": (245, 245, 180)
}
SOUR_CANDY = (173, 255, 47)
GREY = (185, 175, 185)
DARK_GREY = (150, 120, 150)
PINK = (255, 128, 165)
WHITE = (255, 255, 255)

MACHINE = pygame.image.load("Images/automat.png")
BG = pygame.image.load("Images/bg.png")

random_key = ''

last_bonbon = (255, 255, 255)

text = ""

size = (700, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Candy Vending Machine')

display_click = False
run = True
clock = pygame.time.Clock()

first_bonbon_position = 450
radius = 45


def bonbon_distance(first_pos, list_pos):
    return first_pos - ((list_pos * 2) * (radius + 2))


def special_candy():
    if random.randint(0, 9) == 1:
        special = True
    else:
        special = False
    return special


def get_color():
    global random_key
    random_key = random.choice(list(CANDY_COLORS.keys()))
    return CANDY_COLORS.get(random_key)


class Candy:
    def __init__(self, sour, color, key, y):
        self.y = y
        self.inMachine = True
        self.key = key
        if sour:
            self.key = self.key + " XTRA SOUR"
            self.color = SOUR_CANDY
        else:
            self.color = color

    def bonbon_shape(self):
        return pygame.draw.circle(screen, self.color, (460, self.y), radius)


bonbon_1 = Candy(special_candy(), get_color(), random_key, 0)
bonbon_2 = Candy(special_candy(), get_color(), random_key, bonbon_distance(0, 1))
bonbon_3 = Candy(special_candy(), get_color(), random_key, bonbon_distance(0, 2))
bonbon_4 = Candy(special_candy(), get_color(), random_key, bonbon_distance(0, 3))

bonbons = [bonbon_1, bonbon_2, bonbon_3, bonbon_4]

while run:
    background = screen.blit(BG, (0, 0))
    screen.blit(MACHINE, (110, 100))
    pygame.draw.rect(screen, GREY, pygame.Rect(400, 120, 120, 400))
    bonbon_1.bonbon_shape()
    bonbon_2.bonbon_shape()
    bonbon_3.bonbon_shape()
    bonbon_4.bonbon_shape()
    output = pygame.draw.rect(screen, PINK, pygame.Rect(385, 620, 150, 40))
    button = pygame.draw.circle(screen, PINK, (220, 250), 70)
    pygame.draw.rect(screen, GREY, pygame.Rect(172, 350, 100, 30))
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(180, 360, 80, 10))
    screen.blit(pygame.font.Font(None, 50).render("PUSH", True, WHITE), (button.centerx - 50, button.centery - 10))
    screen.blit(pygame.font.Font(None, 70).render(text, True, last_bonbon), (100, 740))

    if bonbons:
        if bonbons[0].y <= output.centery and not bonbons[0].inMachine:
            bonbons[0].y += 5
            if bonbons[0].bonbon_shape().collidepoint(output.center):
                last_bonbon = bonbons[0].color
                text = bonbons[0].key
                del bonbons[0]
        for bonbon in bonbons:
            if bonbon.y <= bonbon_distance(first_bonbon_position, bonbons.index(bonbon)) and bonbon.inMachine:
                bonbon.y += 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and bonbons:
            bonbons[0].inMachine = False
            text = ""

    pygame.display.flip()

    clock.tick(60)

pygame.quit()