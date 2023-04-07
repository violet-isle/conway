import pygame
from random import randint
from copy import deepcopy

RES = WIDTH, HEIGHT = 1200, 675
TILE = 25
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 4

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
paused = True

next_field = [[0 for i in range(W)] for j in range(H)]
current_field = [[0 for i in range(W)] for j in range(H)]

def check_cell(current_field, x, y):
    count = 0
    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            if current_field[j][i]:
                count += 1
    if current_field[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        else: 
            return 0
    else:
        if count == 3:
            return 1
        else: 
            return 0

def draw():
    for i in range(1, W-1):
        for j in range(1, H-1):
            if current_field[j][i]:
                pygame.draw.rect(surface, pygame.Color('white'), (i * TILE + 2, j * TILE + 2, TILE - 2, TILE -2))
            else:
                if not textRect0.colliderect(pygame.Rect(i * TILE + 2, j * TILE + 2, TILE - 2, TILE -2)) and not textRect1.colliderect(pygame.Rect(i * TILE + 2, j * TILE + 2, TILE - 2, TILE -2)):
                    pygame.draw.rect(surface, pygame.Color('black'), (i * TILE + 2, j * TILE + 2, TILE - 2, TILE -2))
                
    pygame.display.flip()


surface.fill(pygame.Color('black'))
[pygame.draw.line(surface, pygame.Color('dimgray'), (x, 0), (x, HEIGHT)) for x in range (0, WIDTH, TILE)]
[pygame.draw.line(surface, pygame.Color('dimgray'), (0, y), (WIDTH, y)) for y in range (0, HEIGHT, TILE)]

font = pygame.font.Font('freesansbold.ttf', 28)
text0 = font.render('   Paused   ', True, pygame.Color('black'), pygame.Color('gray'))
text1 = font.render('Unpaused', True, pygame.Color('black'), pygame.Color('gray'))
textRect0 = text0.get_rect()
textRect0.center = (4 * TILE, 2 * TILE)
textRect1 = text1.get_rect()
textRect1.center = (4 * TILE, 2 * TILE - 1)

pygame.display.flip()
while True:

    
    draw()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    surface.blit(text1, textRect1)
                    draw()
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or pygame.mouse.get_pressed(3) == (1, 0, 0):
                for i in range(1, W-1):
                    for j in range(1, H-1):
                        r = pygame.Rect(i * TILE + 2, j * TILE + 2, TILE - 2, TILE - 2)
                        if r.collidepoint(pygame.mouse.get_pos()):
                            if current_field[j][i]:
                                current_field[j][i] = 0
                                pygame.draw.rect(surface, pygame.Color('black'), (i * TILE + 2, j * TILE + 2, TILE - 2, TILE -2))
                            else:
                                current_field[j][i] = 1
                                pygame.draw.rect(surface, pygame.Color('white'), (i * TILE + 2, j * TILE + 2, TILE - 2, TILE -2))
                            draw()
    while not paused:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    surface.blit(text0, textRect0)
                    draw()
                    paused = True
        for i in range(1, W-1):
            for j in range(1, H-1):
                next_field[j][i] = check_cell(current_field, i, j)
        current_field = deepcopy(next_field)
        pygame.display.flip()
        clock.tick(FPS)
