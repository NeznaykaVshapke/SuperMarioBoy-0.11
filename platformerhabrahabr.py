#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import pygame_menu
from pygame import *
from player import *
from blocks import *
from prize import *
from mine import *

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
round_count = 0;

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

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)
runnning = True
pygame.init()  # Инициация PyGame, обязательная строчка
screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
level1 = [
        "----------------------------------",
        "-                                -",
        "-                       --       -",
        "-                                -",
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
        "-                                -",
        "-      ---                       -",
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
        "-                       --       -",
        "-                                -",
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
        "-                                -",
        "-      ---                       -",
        "-                                -",
        "-----------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]
level3 = [
        "----------------------------------",
        "-                                -",
        "-------------------------------- -",
        "-                                -",
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
        "-                                -",
        "-      ---                       -",
        "-                                -",
        "-----------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]
level_array = [level1, level2, level3]

round_count = False
pygame.display.update()
def start_the_game():
    level = level_array[round_count - 1]
    runnning = True
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    prizes = []
    mines = []
    pr_empty = False
    flag = False
    flag_mine = False
    mn_empty = False
    pr_empty1 = False
    entities.add(hero)



    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    pr = Prize(100,600)
    entities.add(pr)
    prizes.append(pr)

    pr1 = Prize(150, 650)
    entities.add(pr1)
    prizes.append(pr1)

    mn = Mine(500, 670)
    entities.add(mn)
    mines.append(mn)

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while runnning:  # Основной цикл программы
        #print(round_count)
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
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

        #count_pr = count_pr_upper(count_pr)
        count = hero.count
        mn_count = hero.count_mine

        camera.update(hero)  # центризируем камеру относительно персонажа


        hero.update(left, right, up, platforms, prizes, mines)  # передвижение
        f1 = pygame.font.Font(None, 56)
        f2 = pygame.font.Font(None, 36)
        pr_del = hero.index_pr
        if hero.count_mine != mn_count:
            mn.kill()
            xTekst = hero.xvel
            yTekst = hero.yvel
            hero.kill()
            #hero.rect.x = 0;
            #hero.rect.y = 0;
            flag_mine = True
        if hero.count != count and not pr_empty and pr_del == prizes.index(pr):
            prizes.remove(pr)
            # if not pr_empty:
            #p = prizes.index(pr)
            #prizes(pr)
            # pr_empty[p] = True
            pr.kill()
            pr_empty = True
            pr_del = 5
        if hero.count != count and not pr_empty1 and pr_del == prizes.index(pr1):
            prizes.remove(pr1)
            # if not pr_empty:
            #p = prizes.index(pr)
            #prizes(pr)
            # pr_empty[p] = True
            pr1.kill()
            pr_empty1 = True
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
            #hero.rect.x = 0;
            #hero.rect.y = 0;
            text2 = f1.render('Вы прошли уровень ' + str(1), 1, (180, 0, 0), (10,10,100))
            #text3 = f1.render('Чтобы перейти в главное меню нажмите Escape, чтобы пройти уровень заново нажмите Enter' + str(1), 1, (180, 0, 0))
            screen.blit(text2, (50, 300))
            screen.blit(text3, (50, 100))
            for e in pygame.event.get():
                if e.type == KEYUP and e.key == K_ESCAPE:
                    runnning = False

        screen.blit(text1, (40, 40))
        # entities.draw(screen) # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран

def set_difficulty(value, difficulty):
    print(difficulty)
    global round_count
    round_count = difficulty
menu = pygame_menu.Menu('Welcome', 400, 300)
menu.add.text_input('Name :')
menu.add.selector('Difficulty :', [('Easy', 1), ('Hard', 2), ('Dead', 3)], onchange = set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
def count_pr_upper(count):
    count += 1
    return count

def change_perem():
    pass

