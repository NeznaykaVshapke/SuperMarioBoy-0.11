#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pygame_menu
from pygame import *
from player import *
from blocks import *
from prize import *
from mine import *

WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
round_count = 1;

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)
runnning = True
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("SuperGamePythonchiik")
level1 = [
        "----------------------------------",
        "-                                -",
        "-                                -",
        "-                       --       -",
        "-            --                  -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                   ----     --- -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                            --- -",
        "-                                -",
        "-      ---                       -",
        "-                                -",
        "-                                -",
        "-   -------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]
level2 = [
        "----------------------------------",
        "-                                -",
        "-                                -",
        "-                         -      -",
        "-            --                  -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                   ----     --- -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-          ---               --- -",
        "-                                -",
        "-                                -",
        "-      ---                       -",
        "-                                -",
        "---                 ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]
level3 = [
        "----------------------------------",
        "-                                -",
        "---------------------   -------- -",
        "-                                -",
        "-                                -",
        "-                    ---         -",
        "--                               -",
        "-                                -",
        "-                 ------     --- -",
        "-                                -",
        "--                               -",
        "-      ---                       -",
        "-                                -",
        "-                                -",
        "-              ----              -",
        "-                                -",
        "-                                -",
        "                          ----   -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "----------------------------------"]
level_array = [level1, level2, level3]

pygame.display.update()
file = open("tablerecords.txt", "w")
file.write("hello world")
level1_prizes = [[252, 418], [430, 98], [787, 65]]
level2_prizes = [[60, 513], [437, 96], [830, 66]]
level3_prizes = [[550, 417], [720, 224], [280, 322]]
level1_mines = [[170, 500], [650, 213], [970, 215]]
level2_mines = [[280, 435], [395, 342], [680, 500]]
level3_mines = [[870, 500], [650, 213], [970, 215]]
prizes_array = [level1_prizes, level2_prizes, level3_prizes]
mines_array = [level1_mines, level2_mines, level3_mines]
def start_the_game():
    level = level_array[round_count - 1]
    level_prizes = prizes_array[round_count - 1]
    level_mines = mines_array[round_count - 1]
    runnning = True
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    hero = Player(55, 55)
    left = right = False  # по умолчанию - стоим
    up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    prizes = []
    mines = []
    flag = False
    flag_mine = False
    mn_empty = False
    mn_empty1 = False
    mn_empty2 = False
    pr_empty = False
    pr_empty1 = False
    pr_empty2 = False
    entities.add(hero)



    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    pr = Prize(level_prizes[0][0], level_prizes[0][1])
    entities.add(pr)
    prizes.append(pr)

    pr1 = Prize(level_prizes[1][0], level_prizes[1][1])
    entities.add(pr1)
    prizes.append(pr1)

    pr2 = Prize(level_prizes[2][0], level_prizes[2][1])
    entities.add(pr2)
    prizes.append(pr2)

    mn = Mine(level_mines[0][0], level_mines[0][1])
    entities.add(mn)
    mines.append(mn)

    mn1 = Mine(level_mines[1][0], level_mines[1][1])
    entities.add(mn1)
    mines.append(mn1)

    mn2 = Mine(level_mines[2][0], level_mines[2][1])
    entities.add(mn2)
    mines.append(mn2)

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while runnning:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_ESCAPE:
                runnning = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        count = hero.count
        mn_count = hero.count_mine

        camera.update(hero)


        hero.update(left, right, up, platforms, prizes, mines)
        f1 = pygame.font.Font(None, 56)
        f2 = pygame.font.Font(None, 36)
        pr_del = hero.index_pr
        mn_del = hero.index_mn
        if hero.count_mine != mn_count and not mn_empty and mn_del == mines.index(mn):
            mines.remove(mn)
            pr.kill()
            mn_empty = True
            mn_del = 5
            hero.kill()
            flag_mine = True
        if hero.count_mine != mn_count and not mn_empty1 and mn_del == mines.index(mn1):
                mines.remove(mn1)
                pr.kill()
                mn_empty1 = True
                mn_del = 5
                hero.kill()
                flag_mine = True
        if hero.count_mine != mn_count and not mn_empty2 and mn_del == mines.index(mn2):
            mines.remove(mn2)
            pr.kill()
            mn_empty2 = True
            mn_del = 5
            hero.kill()
            flag_mine = True

        if hero.count != count and not pr_empty and pr_del == prizes.index(pr):
            prizes.remove(pr)
            pr.kill()
            pr_empty = True
            pr_del = 5
        if hero.count != count and not pr_empty1 and pr_del == prizes.index(pr1):
            prizes.remove(pr1)
            pr1.kill()
            pr_empty1 = True
        if hero.count != count and not pr_empty2 and pr_del == prizes.index(pr2):
            prizes.remove(pr2)
            pr2.kill()
            pr_empty2 = True
            pr_del = 5
        text3 = f1.render('Чтобы перейти в главное меню', 1, (180, 0, 0), (10,100,0))
        text31 = f1.render('нажмите Escape', 1, (180, 0, 0), (10,100,0))
        text1 = f2.render('Бонусов:' + str(hero.count), 1, (180, 0, 0))
        if flag_mine:
            text4 = f1.render('Вы наткнулись на мину и погибли:(', 10, (180, 0, 0), (100,10,0))
            screen.blit(text4, (65, 300))
            screen.blit(text3, (50, 100))
            screen.blit(text31, (50, 140))
        if hero.count == 2:
            hero.kill()
            file.write(str(hero.count))
            text2 = f1.render('Вы прошли уровень ' + str(1), 1, (180, 0, 0), (10,10,100))
            screen.blit(text2, (50, 300))
            screen.blit(text3, (50, 100))
            for e in pygame.event.get():
                if e.type == KEYUP and e.key == K_ESCAPE:
                    runnning = False

        screen.blit(text1, (40, 40))
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def set_difficulty(value, difficulty):
    print(difficulty)
    global round_count
    round_count = difficulty
menu = pygame_menu.Menu('MarioBoy', 400, 300)
#menu.add.text_input('Name :')
menu.add.selector('Difficulty :', [('Easy', 1), ('Hard', 2), ('Dead', 3)], onchange = set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)


