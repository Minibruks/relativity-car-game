import pygame
import random
import math

pygame.init()
gamedisplay = pygame.display.set_mode((800, 600))
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Don't Crash")
clock = pygame.time.Clock()

explode_sound = pygame.mixer.Sound("crash.wav")
launch_sound = pygame.mixer.Sound("launch.wav")
ring_sound = pygame.mixer.Sound("ring.wav")
# Меняем музыку на Девида Боуи, чтобы как у Илона Маска
pygame.mixer.music.load("spaceoddity.mp3")
roadimg = pygame.image.load("kosmos-zvezdy.jpg")
mycarimg = pygame.image.load("yellow_car.png")
mycarimg_orig = pygame.image.load("yellow_car.png")  # Запоминаем оригинальную картинку
mycarimg_size = mycarimg.get_rect().size  # Запоминаем начальные размеры картинки

explodeimg = pygame.image.load("explode.png")
busimg = pygame.image.load("bus.png")
busimg_orig = pygame.image.load("bus.png")  # Запоминаем оригинальную картинку
busimg_size = busimg.get_rect().size  # Запоминаем начальные размеры картинки
bluecarimg = pygame.image.load("blue_car.png")
bluecarimg_orig = pygame.image.load("blue_car.png")  # Запоминаем оригинальную картинку
bluecarimg_size = bluecarimg.get_rect().size  # Запоминаем начальные размеры картинки
policecarimg = pygame.image.load("police_car.png")
policecarimg_orig = pygame.image.load("police_car.png")  # Запоминаем оригинальную картинку
policecarimg_size = policecarimg.get_rect().size  # Запоминаем начальные размеры картинки
redcarimg = pygame.image.load("red_car.png")
redcarimg_orig = pygame.image.load("red_car.png")  # Запоминаем оригинальную картинку
redcarimg_size = redcarimg.get_rect().size  # Запоминаем начальные размеры картинки
introimg = pygame.image.load("intro.jpg")
rocketimg = pygame.image.load("rocket.png")
rocketimg_orig = pygame.image.load("rocket.png")  # Запоминаем оригинальную картинку
rocketimg_size = rocketimg.get_rect().size  # Запоминаем начальные размеры картинки
rocketicon = pygame.image.load("rocketicon.png")
missileimg = pygame.image.load("missile.png")
missileimg_orig = pygame.image.load("missile.png")  # Запоминаем оригинальную картинку
missileimg_size = missileimg.get_rect().size  # Запоминаем начальные размеры картинки

# константы
speed_c = 30  # скорость света
crash_flag = 1  # 1 - конец игры после столкновения, 0 - не обращать внимания на столкновения

# **********color**********
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
brightred = (255, 0, 0)
green = (0, 200, 0)
brightgreen = (0, 255, 0)
blue = (0, 0, 200)
brightblue = (0, 0, 255)
yellow = (200, 200, 0)
brightyellow = (255, 255, 0)
purple = (200, 0, 200)
brightpurple = (255, 0, 255)


# **********functions********
def quitgame():
    pygame.quit()
    quit()


def road1(x, y):
    gamedisplay.blit(roadimg, (x, y))


def road2(x, y):
    gamedisplay.blit(roadimg, (x, y))


def road3(x, y):
    gamedisplay.blit(roadimg, (x, y))


def Label(msg, x, y, size, color):
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(msg, True, color)
    gamedisplay.blit(text, (x, y))


def Button(msg, x, y, width, height, i_color, a_color, command=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(gamedisplay, a_color, (x, y, width, height))
        if click[0] == 1 and command != None:
            command()
    else:
        pygame.draw.rect(gamedisplay, i_color, (x, y, width, height))
    buttontext = pygame.font.SysFont("comicsansms", 20)
    buttonmsg = buttontext.render(msg, True, black)
    buttonmsgrect = buttonmsg.get_rect()
    buttonmsgrect.center = ((x + width / 2), (y + height / 2))
    gamedisplay.blit(buttonmsg, buttonmsgrect)


def explode(x, y):
    x -= 50
    y -= 50
    gamedisplay.blit(explodeimg, (x, y))
    pygame.mixer.Sound.play(explode_sound)


def crash(x, y):
    if not crash_flag:
        return 0
    pygame.mixer.music.stop()
    explode(x, y)
    Label("Вы врезались!", 100, 200, 100, yellow)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        Button("Заново", 200, 400, 100, 50, green, brightgreen, gameloop)
        Button("Выход", 500, 400, 100, 50, red, brightred, quitgame)
        Button("меню", 20, 500, 100, 50, purple, brightpurple, intro)

        pygame.display.update()
        clock.tick(15)


def scorelabel(score):
    Label("Моя cкорость: " + str(score) + "км/ч Скорость света " + str(speed_c) + "км/ч", 5, 5, 30, blue)


def unpause():
    pygame.mixer.music.unpause()
    global paused
    paused = False


def pause():
    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        Label("Пауза", 250, 150, 100, blue)
        Button("Продолжить", 200, 400, 100, 50, brightgreen, green, unpause)
        Button("Выход", 500, 400, 100, 50, red, quitgame, brightred)
        Button("Заново", 680, 500, 100, 50, yellow, brightyellow, gameloop)
        Button("Меню", 20, 500, 100, purple, 50, brightpurple, intro)
        pygame.display.update()
        clock.tick(15)


# вычисляем коэф. искажения размеров через преобразования лоренца
def k_lorenz(speed_obj):
    if math.fabs(speed_obj) / speed_c >= 1:  # подстрахуемся от превышения скорости света, если такое случиться
        # вернем очень маленькое число
        return 0.0000001
    return math.sqrt(1 - speed_obj ** 2 / speed_c ** 2)


def rocket(x, y, speed):
    global rocketimg
    rocketimg = pygame.transform.scale(rocketimg_orig, (rocketimg_size[0], int(rocketimg_size[1] * k_lorenz(
        speed))))  # изменяем размеры картинки по оси У в зависимости от относительной скорости автомобилей
    gamedisplay.blit(rocketimg, (x, y))


def missile(x, y, speed):
    global missileimg
    missileimg = pygame.transform.scale(missileimg_orig, (missileimg_size[0], int(missileimg_size[1] * k_lorenz(
        speed))))  # изменяем размеры картинки по оси У в зависимости от относительной скорости автомобилей
    gamedisplay.blit(missileimg, (x, y))


def missilelabel(shots):
    gamedisplay.blit(rocketicon, (600, 470))
    Label("X " + str(shots), 730, 500, 30, purple)


# ************cars*************
# функции ресования машинок переделываем с изменением размеров с учетом скорости
def mycar(x, y):
    gamedisplay.blit(mycarimg, (x, y))


def bus(x, y, speed):
    global busimg
    busimg = pygame.transform.scale(busimg_orig, (busimg_size[0], int(busimg_size[1] * k_lorenz(
        speed))))  # изменяем размеры картинки по оси У в зависимости от относительной скорости автомобилей
    gamedisplay.blit(busimg, (x, y))


def bluecar(x, y, speed):
    global bluecarimg
    bluecarimg = pygame.transform.scale(bluecarimg_orig, (bluecarimg_size[0], int(bluecarimg_size[1] * k_lorenz(
        speed))))  # изменяем размеры картинки по оси У в зависимости от относительной скорости автомобилей
    gamedisplay.blit(bluecarimg, (x, y))


def policecar(x, y, speed):
    global policecarimg
    policecarimg = pygame.transform.scale(policecarimg_orig, (policecarimg_size[0], int(policecarimg_size[1] * k_lorenz(
        speed))))  # изменяем размеры картинки по оси У в зависимости от относительной скорости автомобилей
    gamedisplay.blit(policecarimg, (x, y))


def redcar(x, y, speed):
    global redcarimg
    redcarimg = pygame.transform.scale(redcarimg_orig, (redcarimg_size[0], int(redcarimg_size[1] * k_lorenz(
        speed))))  # изменяем размеры картинки по оси У в зависимости от относительной скорости автомобилей
    gamedisplay.blit(redcarimg, (x, y))


# *********Main_game***********
def intro():
    gamedisplay.blit(introimg, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        Label("Проектная работа", 150, 80, 50, blue)
        Label("Смирнова Павла", 170, 210, 50, red)
        # Label("Нажмите p для паузы", 300, 470, 27, purple)
        Label("Нажмите ПРОБЕЛ для выстрела", 270, 510, 27, purple)
        Button("Поехали", 200, 400, 100, 50, green, brightgreen, gameloop)
        Button("Выход", 500, 400, 100, 50, blue, brightblue, quitgame)
        pygame.display.update()


def gameloop():
    pygame.mixer.music.play(-1)
    global paused
    speed = 0.5
    drive = 1  # 1 едем вперед -1 едем назад
    score = 0
    shots = 0
    change_x = 0
    myx = 370
    myy = 460  # добавим переменную для У координат нашей машинки, чтобы удобнее было менять если нужно

    road1y = -225
    road2y = -225 - 825
    road3y = -225 - 825 - 825
    road_speed = 1

    busx = random.randrange(100, 700 - 72)
    busy = -210
    bus_speed = -2

    bluecarx = random.randrange(100, 700 - 67)
    bluecary = -160
    bluecar_speed = 0

    policecarx = random.randrange(100, 700 - 83)
    policecary = -170
    policecar_speed = -4

    redcarx = random.randrange(100, 700 - 69)
    redcary = -170
    redcar_speed = -6

    rocketx = random.randrange(100, 700 - 75)
    rockety = -50
    rocket_speed = 3

    missilex = -500
    missiley = 600
    missile_speed = -7

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_x = -5
                if event.key == pygame.K_RIGHT:
                    change_x = 5
                # добавим возможность менять скорость по нажатию на кнопки ВВЕРХ или ВНИЗ, но не более чем скрость света
                if event.key == pygame.K_UP:
                    if speed + 1 < speed_c:
                        speed += 0.5
                        drive = 1
                    else:
                        speed = speed_c - 1
                        drive = -1
                if event.key == pygame.K_DOWN:
                    if speed > 1:
                        speed -= 0.5
                        drive = -1
                    else:
                        speed = 0.5
                        drive = 1
                if event.key == pygame.K_p:
                    paused = True
                    pause()
                if event.key == pygame.K_SPACE:
                    if shots > 0:
                        pygame.mixer.Sound.play(launch_sound)
                        shots -= 1
                        missilex = myx + 10
                        missiley = myy
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    change_x = 0

        # ********Road********
        if road1y > 600:
            road1y = -825
        if road2y > 600:
            road2y = -825
        if road3y > 600:
            road3y = -825
        road1y += road_speed + speed
        road2y += road_speed + speed
        road3y += road_speed + speed
        road1(0, road1y)
        road2(0, road2y)
        road3(0, road3y)
        # *********************

        scorelabel(int(speed))
        missilelabel(shots)

        myx += change_x
        mycar(myx, myy)

        # добавляем в вызов функции для автобуса еще один параметр - скорость относительно нашего автомобиля
        bus(busx, busy, bus_speed + speed)
        busy += bus_speed + speed
        if busy > 600:
            busy = -2000
            busx = random.randrange(100, 700 - 72)
            score += 1
        while (
                bluecarx < busx < bluecarx + 67 or bluecarx < busx + 72 < bluecarx + 67 or bluecarx < busx + 36 < bluecarx + 67) or (
                policecarx < busx < policecarx + 83 or policecarx < busx + 72 < policecarx + 83 or policecarx < busx + 36 < policecarx + 83) or (
                redcarx < busx < redcarx + 69 or redcarx < busx + 72 < redcarx + 69 or redcarx < busx + 36 < redcarx + 69):
            busx = random.randrange(100, 700 - 72)

        # добавляем в вызов функции для синей машинки еще один параметр - скорость относительно нашего автомобиля
        bluecar(bluecarx, bluecary, bluecar_speed + speed)
        bluecary += bluecar_speed + speed
        if bluecary > 600:
            bluecary = -1000
            bluecarx = random.randrange(100, 700 - 67)
            score += 1
        while (
                busx < bluecarx < busx + 72 or busx < bluecarx + 67 < busx + 72 or busx < bluecarx + 33.5 < busx + 72) or (
                policecarx < bluecarx < policecarx + 83 or policecarx < bluecarx + 67 < policecarx + 83 or policecarx < bluecarx + 33.5 < policecarx + 83) or (
                redcarx < bluecarx < redcarx + 69 or redcarx < bluecarx + 67 < redcarx + 69 or redcarx < bluecarx + 33.5 < redcarx + 69):
            bluecarx = random.randrange(100, 700 - 67)

        # добавляем в вызов функции для полицейской машины еще один параметр - скорость относительно нашего автомобиля
        policecar(policecarx, policecary, policecar_speed + speed)
        policecary += policecar_speed + speed
        if policecary > 600:
            policecary = -3000
            policecarx = random.randrange(100, 700 - 83)
            score += 1
        while (
                busx < policecarx < busx + 72 or busx < policecarx + 83 < busx + 72 or busx < policecarx + 83 / 2 < busx + 72) or (
                bluecarx < policecarx < bluecarx + 67 or bluecarx < policecarx + 83 < bluecarx + 67 or bluecarx < policecarx + 83 / 2 < bluecarx + 67) or (
                redcarx < policecarx < redcarx + 69 or redcarx < policecarx + 83 < redcarx + 69 or redcarx < policecarx + 83 / 2 < redcarx + 69):
            policecarx = random.randrange(100, 700 - 83)

        # добавляем в вызов функции для красной машинки еще один параметр - скорость относительно нашего автомобиля
        redcar(redcarx, redcary, redcar_speed + speed)
        redcary += redcar_speed + speed
        if redcary > 600:
            redcary = -2000
            redcarx = random.randrange(100, 700 - 69)
            score += 1
        while (
                busx < redcarx < busx + 72 or busx < redcarx + 69 < busx + 72 or busx < redcarx + 69 / 2 < busx + 72) or (
                bluecarx < redcarx < bluecarx + 67 or bluecarx < redcarx + 69 < bluecarx + 67 or bluecarx < redcarx + 69 / 2 < bluecarx + 67) or (
                policecarx < redcarx < policecarx + 83 or policecarx < redcarx + 69 < policecarx + 83 or policecarx < redcarx + 69 / 2 < policecarx + 83):
            redcarx = random.randrange(100, 700 - 69)

        # **************rocket_and_missile*************
        # добавляем в вызов функции для ракеты еще один параметр - скорость относительно нашего автомобиля
        rocket(rocketx, rockety, rocket_speed + speed)
        rockety += rocket_speed
        if rockety > 600:
            rockety = -1000
            rocketx = random.randrange(100, 700 - 75)
        if rockety + 50 > myy:
            if rocketx < myx < rocketx + 75 or rocketx < myx + 62 < rocketx + 75 or rocketx < myx + 31 < rocketx + 75:
                rockety = -1000
                rocketx = random.randrange(100, 700 - 75)
                shots += 1
                pygame.mixer.Sound.play(ring_sound)

        # добавляем в вызов функции для ракеты еще один параметр - скорость относительно нашего автомобиля
        missile(missilex, missiley, missile_speed + speed)
        missiley += missile_speed
        if missiley + 130 < 0:
            missiley = 600
            missilex = -500
        if busy + 210 > missiley:
            if busx + 10 < missilex < busx + 72 - 10 or busx + 10 < missilex + 44 < busx + 72 - 10 or busx + 10 < missilex + 22 < busx + 72 - 10:
                explode(missilex + 22, missiley)
                missilex = -500
                missiley = 600
                busx = -1000
                busy = 1000
        if bluecary + 150 - 30 > missiley:
            if bluecarx + 15 < missilex < bluecarx + 67 - 15 or bluecarx + 15 < missilex + 44 < bluecarx + 67 - 15 or bluecarx + 15 < missilex + 22 < bluecarx + 67 - 15:
                explode(missilex + 22, missiley)
                missilex = -500
                missiley = 600
                bluecarx = -2000
                bluecary = 1000
        if policecary + 165 - 20 > missiley:
            if policecarx + 20 < missilex < policecarx + 83 - 20 or policecarx + 20 < missilex + 44 < policecarx + 83 - 20 or policecarx + 20 < missilex + 22 < policecarx + 83 - 20:
                explode(missilex + 22, missiley)
                missilex = -500
                missiley = 600
                policecarx = -3000
                policecary = 1000
                score += 1
        if redcary + 130 > missiley:
            if redcarx + 5 < missilex < redcarx + 69 - 5 or redcarx + 5 < missilex + 44 < redcarx + 69 - 5 or redcarx + 5 < missilex + 22 < redcarx + 69 - 5:
                explode(missilex + 22, missiley)
                missilex = -500
                missiley = 600
                redcarx = -4000
                redcary = 1000

        # ************crashes*************
        if myx < 100 or myx + 62 > 700:
            crash(myx + 31, myy)
        if busy + 210 > myy:
            if busx + 10 < myx < busx + 72 - 10 or busx + 10 < myx + 62 < busx + 72 - 10 or busx + 10 < myx + 31 < busx + 72 - 10:
                crash(myx + 31, myy)
        if bluecary + 150 - 30 > myy:
            if bluecarx + 15 < myx < bluecarx + 67 - 15 or bluecarx + 15 < myx + 62 < bluecarx + 67 - 15 or bluecarx + 15 < myx + 31 < bluecarx + 67 - 15:
                crash(myx + 31, myy)
        if policecary + 165 - 20 > myy:
            if policecarx + 20 < myx < policecarx + 83 - 20 or policecarx + 20 < myx + 62 < policecarx + 83 - 20 or policecarx + 20 < myx + 31 < policecarx + 83 - 20:
                crash(myx + 31, myy)
        if redcary + 130 > myy:
            if redcarx + 5 < myx < redcarx + 69 - 5 or redcarx + 5 < myx + 62 < redcarx + 69 - 5 or redcarx + 5 < myx + 31 < redcarx + 69 - 5:
                crash(myx + 31, myy)

        if speed < speed_c - 0.05:
            speed += 0.005 * drive  # добавляем признак направления движения drive

        pygame.display.update()
        clock.tick(60)


intro()
gameloop()
quitgame()
