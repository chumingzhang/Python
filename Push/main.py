import sys
import copy
import pygame

from pygame.locals import *
from map import *
from collections import namedtuple

Player = namedtuple('Player', ['x', 'y'])
Box = namedtuple('Box', ['x', 'y'])

WIDTH = 12
HEIGHT = 12
BLOCK_SIZE = 30
MAPS = [map1, map2, map3, map4, map5]


BG_COLOR = (40, 40, 60)                         # 背景颜色
HOLE_COLOR = (20, 20, 20)                       # 洞颜色
WALL_COLOR = (80, 80, 120)                      # 墙颜色
PLAYER_COLOR = (148, 0, 211)                    # 人颜色
BOX_COLOR = (200, 200, 0)                       # 箱子颜色
FLOOR_COLOR = (50, 50, 160)                     # 地面颜色
INFO_COLOR = (255, 50, 50)                      # 信息颜色

def repaintCurMap(x, y, curMap, level):
    if MAPS[level][x][y] == 2 or MAPS[level][x][y] == 3 or MAPS[level][x][y] == 4:
        curMap[x][y] = 2
    elif MAPS[level][x][y] == 5:
        curMap[x][y] = 5

def move_up(player, curMap, level):
    new_player = player
    nx = player.x - 1
    ny = player.y
    if curMap[nx][ny] == 2:
        curMap[nx][ny] = 3
        new_player = player._replace(x = nx)
        repaintCurMap(player.x, player.y, curMap, level)
    elif curMap[nx][ny] == 4 and (curMap[nx - 1][ny] == 2 or curMap[nx - 1][ny] == 5):
        curMap[nx][ny] = 3
        curMap[nx - 1][ny] = 4
        new_player = player._replace(x = nx)
        repaintCurMap(player.x, player.y, curMap, level)
    elif curMap[nx][ny] == 5:
        curMap[nx][ny] = 3
        new_player = player._replace(x = nx)
        repaintCurMap(player.x, player.y, curMap, level)
        
    return new_player

def move_down(player, curMap, level):
    new_player = player
    nx = player.x + 1
    ny = player.y
    if curMap[nx][ny] == 2:
        curMap[nx][ny] = 3
        new_player = player._replace(x = nx)
        repaintCurMap(player.x, player.y, curMap, level)
    elif curMap[nx][ny] == 4 and (curMap[nx + 1][ny] == 2 or curMap[nx + 1][ny] == 5):
        curMap[nx][ny] = 3
        curMap[nx + 1][ny] = 4
        new_player = player._replace(x = nx)
        repaintCurMap(player.x, player.y, curMap, level)
    elif curMap[nx][ny] == 5:
        curMap[nx][ny] = 3
        new_player = player._replace(x = nx)
        repaintCurMap(player.x, player.y, curMap, level)
        
    return new_player

def move_left(player, curMap, level):
    new_player = player
    nx = player.x
    ny = player.y - 1
    if curMap[nx][ny] == 2:
        curMap[nx][ny] = 3
        new_player = player._replace(y = ny)
        repaintCurMap(player.x, player.y, curMap, level)
    elif curMap[nx][ny] == 4 and (curMap[nx][ny - 1] == 2 or curMap[nx][ny - 1] == 5):
        curMap[nx][ny] = 3
        curMap[nx][ny - 1] = 4
        new_player = player._replace(y = ny)
        repaintCurMap(player.x, player.y, curMap, level)
    elif curMap[nx][ny] == 5:
        curMap[nx][ny] = 3
        new_player = player._replace(y = ny)
        repaintCurMap(player.x, player.y, curMap, level)
        
    return new_player

def move_right(player, curMap, level):
    new_player = player
    nx = player.x
    ny = player.y + 1
    if curMap[nx][ny] == 2:
        curMap[nx][ny] = 3
        new_player = player._replace(y = ny)
        repaintCurMap(player.x, player.y, curMap, level)
    elif curMap[nx][ny] == 4 and (curMap[nx][ny + 1] == 2 or curMap[nx][ny + 1] == 5):
        curMap[nx][ny] = 3
        curMap[nx][ny + 1] = 4
        new_player = player._replace(y = ny)
        repaintCurMap(player.x, player.y, curMap, level)
    elif curMap[nx][ny] == 5:
        curMap[nx][ny] = 3
        new_player = player._replace(y = ny)
        repaintCurMap(player.x, player.y, curMap, level)

    return new_player

def judge_win(curMap, level):
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if MAPS[level][i][j] == 5 and curMap[i][j] != 4:
                return False

    return True

def restart(level):
    curMap = None
    curMap = copy.deepcopy(MAPS[level])
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if curMap[i][j] == 3:
                x = i
                y = j
                break
    player = Player(x, y)

    return player, curMap

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE), 0, 32)
    pygame.display.set_caption('Push')

    font1 = pygame.font.SysFont('SimHei', 20)           # 显示规则
    font2 = pygame.font.SysFont('SimHei', 24)           # 显示赢了

    curLevel = 0
    player, curMap = restart(curLevel)
    # print(player)
    win = False         # 当前关
    totalWin = False    # 全通关

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if not win:
                    if event.key == K_UP:
                        player = move_up(player, curMap, curLevel)
                    elif event.key == K_DOWN:
                        player = move_down(player, curMap, curLevel)
                    elif event.key == K_LEFT:
                        player = move_left(player, curMap, curLevel)
                    elif event.key == K_RIGHT:
                        player = move_right(player, curMap, curLevel)
                    elif event.key == K_r:
                        totalWin = False
                        player, curMap = restart(curLevel)

                    # for i in range(WIDTH):
                    #     for j in range(HEIGHT):
                    #         print(curMap[i][j], end = " ")
                    #     print("\n")

                    win = judge_win(curMap, curLevel)
                    if win:
                        win = False
                        curLevel = ((curLevel + 1) % len(MAPS))
                        player, curMap = restart(curLevel)
                        if curLevel == 0:
                            totalWin = True
                            draw_win(screen, font2)

        if not totalWin:
            draw_map(screen, curMap, font1)
        pygame.display.update()

# 0-墙外； 1-墙； 2-墙内； 3-人物； 4-箱子； 5-目的地
def draw_map(screen, curMap, font):
    screen.fill(BG_COLOR)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            w = j * BLOCK_SIZE
            h = i * BLOCK_SIZE
            if curMap[i][j] == 1:
                pygame.draw.rect(screen, WALL_COLOR, (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)
            elif curMap[i][j] == 2:
                pygame.draw.rect(screen, FLOOR_COLOR, (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)
            elif curMap[i][j] == 3:
                pygame.draw.rect(screen, PLAYER_COLOR, (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)
            elif curMap[i][j] == 4:
                pygame.draw.rect(screen, BOX_COLOR, (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)
            elif curMap[i][j] == 5:
                pygame.draw.rect(screen, HOLE_COLOR, (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)
    text = font.render("Press 'R' to restart", True, INFO_COLOR)
    screen.blit(text, (10, 10))

def draw_win(screen, font):
    # print("win")
    screen.fill((255, 255, 255))
    text = font.render("You Win！ Press 'R' to restart", True, INFO_COLOR)
    screen.blit(text, (0, BLOCK_SIZE * WIDTH // 2))


if __name__ == '__main__':
    main()