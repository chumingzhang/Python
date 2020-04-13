import sys
import copy
import pygame
import pygame.gfxdraw
import random
import time
import math

from pygame.locals import *
from Map import map1
from collections import namedtuple

Evil = namedtuple('Evil', ['x', 'y'])
Pac = namedtuple('Pac', ['x', 'y'])

WIDTH = len(map1)                               # 地图宽度
HEIGHT = len(map1[0])                           # 地图高度
BLOCK_SIZE = 20                                 # 单位块大小
GAP = 5                                         # 地图四周空隙
BG_COLOR = (40, 40, 60)                         # 背景颜色
PAC_COLOR = (255, 255, 0)                       # 豆子颜色
BLOCK_COLOR = (100, 100, 100)                   # 墙颜色
MAN_COLOR = (148, 0, 211)                       # 人颜色
ENEMY_COLOR = (200, 30, 30)                     # 恶魔颜色
INFO_COLOR = (255, 50, 50)                      # 信息颜色
PAC_RADIU = 4                                   # 豆子半径
EX = int((BLOCK_SIZE - PAC_RADIU) / 2)          # 画豆子的额外计算距离
DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # 恶魔随机移动方向

def moveUp(pac, curMap):
    new_pac = pac
    nx = pac.x - 1
    ny = pac.y
    if curMap[nx][ny] != 1:
        curMap[nx][ny] = 3
        curMap[pac.x][pac.y] = 2
        new_pac = pac._replace(x = nx)
    return new_pac

def moveDown(pac, curMap):
    new_pac = pac
    nx = pac.x + 1
    ny = pac.y
    if curMap[nx][ny] != 1:
        curMap[nx][ny] = 3
        curMap[pac.x][pac.y] = 2
        new_pac = pac._replace(x = nx)
    return new_pac

def moveLeft(pac, curMap):
    new_pac = pac
    nx = pac.x
    ny = pac.y - 1
    if curMap[nx][ny] != 1:
        curMap[nx][ny] = 3
        curMap[pac.x][pac.y] = 2
        new_pac = pac._replace(y = ny)
    return new_pac

def moveRight(pac, curMap):
    new_pac = pac
    nx = pac.x
    ny = pac.y + 1
    if curMap[nx][ny] != 1:
        curMap[nx][ny] = 3
        curMap[pac.x][pac.y] = 2
        new_pac = pac._replace(y=ny)
    return new_pac

def restart():
    curMap = copy.deepcopy(map1)
    return curMap

def randomCreateEvils():
    evils = []
    for i in range(4):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        evil = Evil(x, y)
        evils.append(evil)

    return evils

def evilCatch(evils, pac):
    for evil in evils:
        if abs(evil.x - pac.x) + abs(evil.y - pac.y) > 8:
            while True:
                dx, dy = random.choice(DIRECTION)
                if 0 <= evil.x + dx and evil.x + dx < WIDTH and 0 <= evil.y + dy and evil.y + dy < HEIGHT:
                    break
            if dx == 0:
                new_evil = evil._replace(y = evil.y + dy)
            else:
                new_evil = evil._replace(x = evil.x + dx)
        else:
            if evil.x < pac.x :
                new_evil = evil._replace(x = evil.x + 1)
            elif evil.x > pac.x :
                new_evil = evil._replace(x = evil.x - 1)
            elif evil.y < pac.y :
                new_evil = evil._replace(y = evil.y + 1)
            elif evil.y > pac.y :
                new_evil = evil._replace(y = evil.y - 1)

        evils.remove(evil)
        evils.append(new_evil)

def judgeWin(curMap):
    for line in curMap:
        if 0 in line:
            return False
    return True

def judgeLose(evils, pac):
    for evil in evils:
        if evil.x == pac.x and evil.y == pac.y:
            return True

    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((HEIGHT * BLOCK_SIZE + GAP * 2, WIDTH *BLOCK_SIZE + GAP * 2), 0, 32)
    pygame.display.set_caption('PacMan')

    # print(WIDTH, HEIGHT)

    font1 = pygame.font.SysFont('SimHei', 20)           # 人和恶魔
    font2 = pygame.font.SysFont('SimHei', 24)           # 显示结局
    win = False
    lose = False
    curMap = restart()
    evils = randomCreateEvils()
    pac = Pac(1, 1)
    # for evil in evils:
    #     print(evil)

    # 用来控制移动速度不能太快
    last_pac_move_time = time.time()                    # 上一次人移动时间
    last_evil_move_time = time.time()                    # 上一次恶魔移动时间

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if win or lose:
                    if event.key == K_SPACE:
                        win = False
                        lose = False
                        curMap = restart()
                        evils = randomCreateEvils()
                        pac = Pac(1, 1)

        if event.type == KEYDOWN:
            if not win and not lose:
                if time.time() - last_pac_move_time > 0.1:
                    if event.key == K_UP:
                        pac = moveUp(pac, curMap)
                    elif event.key == K_DOWN:
                        pac = moveDown(pac, curMap)
                    elif event.key == K_LEFT:
                        pac = moveLeft(pac, curMap)
                    elif event.key == K_RIGHT:
                        pac = moveRight(pac, curMap)
                    win = judgeWin(curMap)
                    last_pac_move_time = time.time()

        if not win and not lose:
            if time.time() - last_evil_move_time > 0.5:
                evilCatch(evils, pac)
                last_evil_move_time = time.time()

        draw_map(screen, curMap, font1)
        draw_evil(screen, evils, font1)
        lose = judgeLose(evils, pac)
        if lose:
            draw_lose(screen, font2)
        if win:
            draw_win(screen, font2)

        pygame.display.update()


# 画出地图
def draw_map(screen, curMap, font):
    # 填充背景色
    screen.fill(BG_COLOR)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            w = GAP + j * BLOCK_SIZE
            h = GAP + i * BLOCK_SIZE
            if curMap[i][j] == 0:
                # pygame.draw.circle(screen, PAC_COLOR, (w + EX, h + EX), PAC_RADIU, 0)
                
                # 抗锯齿的圆
                pygame.gfxdraw.aacircle(screen, w + EX, h + EX, PAC_RADIU, PAC_COLOR)
                pygame.gfxdraw.filled_circle(screen, w + EX, h + EX, PAC_RADIU, PAC_COLOR)
            elif curMap[i][j] == 1:
                pygame.draw.rect(screen, BLOCK_COLOR, (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)
            elif curMap[i][j] == 3:
                pygame.gfxdraw.aacircle(screen, w + 10, h + 10, 8, MAN_COLOR)
                pygame.gfxdraw.filled_circle(screen, w + 10, h + 10, 8, MAN_COLOR)

def draw_evil(screen, evils, font):
    for evil in evils:
        w = GAP + evil.y * BLOCK_SIZE
        h = GAP + evil.x * BLOCK_SIZE
        pygame.gfxdraw.aacircle(screen, w + 10, h + 10, 8, ENEMY_COLOR)
        pygame.gfxdraw.filled_circle(screen, w + 10, h + 10, 8, ENEMY_COLOR)

def draw_win(screen, font):
    # print("win")
    screen.fill((255, 255, 255))
    text = font.render("You Win！ Press 'Space' to restart", True, INFO_COLOR)
    screen.blit(text, (10, BLOCK_SIZE * WIDTH // 2))

def draw_lose(screen, font):
    # print("lose")
    screen.fill((255, 255, 255))
    text = font.render("You Lose！ Press 'Space' to restart", True, INFO_COLOR)
    screen.blit(text, (10, BLOCK_SIZE * WIDTH // 2))

if __name__ == '__main__':
    main()