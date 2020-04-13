import sys
import random
import pygame

from pygame.locals import *

SIZE = 4                                            # 游戏区域 4 * 4
BLOCK_SIZE = 110                                    # 单位块大小
GAP = 10                                            # 块之间的间隙
GAME_SIZE = BLOCK_SIZE * SIZE + (SIZE + 1) * GAP    # 游戏区域宽和高
PANEL_SIZE = (GAME_SIZE, GAME_SIZE + 110)           # 整个界面的（宽， 高）
BG_COLOR = (60, 60, 80)                             # 背景色
EMPTY_BLOCK_COLOR = (40, 40, 60)                    # 空块的颜色
INFO_COLOR = (200, 30, 30)                          # 状态信息颜色
NUM_COLOR = (0, 0, 0)                               # 方块上的数字颜色
DIRECTION = [[-1, 0], [0, -1], [1, 0], [0, 1]]      # 相邻的四个方向
SCORE = 0                                           # 得分

BLOCK_COLOR = {                                     # 每种块对应的颜色
    0:(0, 0, 0),
    2:(255,255,255),
    4:(255,255,128),
    8:(255,255,0),
    16:(255,220,128),
    32:(255,220,0),
    64:(255,190,0),
    128:(255,160,0),
    256:(255,130,0),
    512:(255,100,0),
    1024:(255,70,0),
    2048:(255,40,0),
    4096:(255,10,0),
}

def mergeUp(matrix):
    global SCORE
    for i in range(1, 4):
        for j in range(4):
            if matrix[i][j] != 0:
                l = i
                for k in range(i - 1, -1, -1):
                    if matrix[k][j] == 0:
                        matrix[k][j] = matrix[l][j]
                        matrix[l][j] = 0
                        l -= 1
                    elif matrix[k][j] == matrix[l][j]:
                        matrix[k][j] = 2 * matrix[k][j]
                        SCORE += matrix[k][j]
                        matrix[l][j] = 0
                    else:
                        break

def mergeDown(matrix):
    global SCORE
    for i in range(2, -1, -1):
        for j in range(4):
            if matrix[i][j] != 0:
                l = i
                for k in range(i + 1, 4):
                    if matrix[k][j] == 0:
                        matrix[k][j] = matrix[l][j]
                        matrix[l][j] = 0
                        l += 1
                    elif matrix[k][j] == matrix[l][j]:
                        matrix[k][j] = 2 * matrix[k][j]
                        SCORE += matrix[k][j]
                        matrix[l][j] = 0
                    else:
                        break

def mergeLeft(matrix):
    global SCORE
    for i in range(0, 4):
        for j in range(1, 4):
            if matrix[i][j] != 0:
                l = j
                for k in range(j - 1, -1, -1):
                    if matrix[i][k] == 0:
                        matrix[i][k] = matrix[i][l]
                        matrix[i][l] = 0
                        l -= 1
                    elif matrix[i][k] == matrix[i][l]:
                        matrix[i][k] = 2 * matrix[i][l]
                        SCORE += matrix[i][k]
                        matrix[i][l] = 0
                    else:
                        break

def mergeRight(matrix):
    global SCORE
    for i in range(0, 4):
        for j in range(2, -1, -1):
            if matrix[i][j] != 0:
                l = j
                for k in range(j + 1, 4):
                    if matrix[i][k] == 0:
                        matrix[i][k] = matrix[i][l]
                        matrix[i][l] = 0
                        l += 1
                    elif matrix[i][k] == matrix[i][l]:
                        matrix[i][k] = 2 * matrix[i][l]
                        SCORE += matrix[i][k]
                        matrix[i][l] = 0
                    else:
                        break

def randomCreate(matrix):
    hasZero = False
    for i in range(4):
        if 0 in matrix[i]:
            hasZero = True
            break
    
    if hasZero:
        while True:
            i = random.choice(range(4))
            j = random.choice(range(4))
            if matrix[i][j] == 0:
                matrix[i][j] = random.choice([2, 2, 2, 4])
                break

def judgeLose(matrix):
    for i in range(4):
        if 0 in matrix[i]:
            return False

    for i in range(4):
        for j in range(4):
            for (dx, dy) in DIRECTION:
                nx = i + dx
                ny = j + dy
                if(nx >= 0 and nx < 4 and ny >= 0 and ny < 4 and matrix[nx][ny] == matrix[i][j]):
                    return False
    
    # print("gameover!")
    return True

def newGame():
    global SCORE
    SCORE = 0
    matrix = [                                      # 初始化块二维list
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    # 先随机生成两个块
    randomCreate(matrix)
    randomCreate(matrix)
    return matrix

def main():
    pygame.init()
    screen = pygame.display.set_mode(PANEL_SIZE, 0, 32)
    pygame.display.set_caption('2048')

    font1 = pygame.font.SysFont(None, 60)           # 写在块上的数字
    font2 = pygame.font.SysFont('SimHei', 72)
    matrix = None
    matrix = newGame()
    gameover = False                                # 判断游戏是否结束
    # for i in BLOCK_COLOR:
    #     print(BLOCK_COLOR[i])
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if gameover == True:
                        gameover = False
                        matrix = newGame()
                elif gameover == False:
                    if event.key == K_UP:
                        mergeUp(matrix)
                    elif event.key == K_DOWN:
                        mergeDown(matrix)
                    elif event.key == K_LEFT:
                        mergeLeft(matrix)
                    elif event.key == K_RIGHT:
                        mergeRight(matrix)
                    # 随机产生新的2或4(概率不同)
                    gameover = judgeLose(matrix) 
                    if not gameover:
                        randomCreate(matrix)

        draw_background(screen)
        draw_info(screen, font2)
        if gameover:
            draw_gameover(screen, font1)
        else:
            draw_block(screen, matrix, font1)

        pygame.display.update()

# 画背景
def draw_background(screen):
    # 填充背景色
    screen.fill(BG_COLOR)
    for i in range(4):
        for j in range(4):
            w = GAP + j * (BLOCK_SIZE + GAP)
            h = GAP + BLOCK_SIZE + i * (BLOCK_SIZE + GAP)
            pygame.draw.rect(screen, EMPTY_BLOCK_COLOR, (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)

# 画状态信息
def draw_info(screen, font):
    text = font.render("Score:" + str(SCORE), True, INFO_COLOR)
    screen.blit(text, (GAP, GAP))

# 画块
def draw_block(screen, matrix, font):
    for i in range(4):
        for j in range(4):
            # print(matrix[i][j])
            if matrix[i][j] != 0:
                w = GAP + j * (BLOCK_SIZE + GAP)
                h = GAP + BLOCK_SIZE + i * (BLOCK_SIZE + GAP)
                if matrix[i][j] <= 4096:
                    pygame.draw.rect(screen, BLOCK_COLOR[matrix[i][j]], (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)
                else:
                    pygame.draw.rect(screen, INFO_COLOR, (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)
                fw, fh = font.size(str(int(matrix[i][j])))
                text = font.render(str(int(matrix[i][j])), True, NUM_COLOR)
                screen.blit(text, (w + (int)((BLOCK_SIZE - fw) / 2), h + (int)((BLOCK_SIZE - fh) / 2)))

# 画游戏结束画面
def draw_gameover(screen, font):
    for i in range(4):
        for j in range(4):
            w = GAP + j * (BLOCK_SIZE + GAP)
            h = GAP + BLOCK_SIZE + i * (BLOCK_SIZE + GAP)
            pygame.draw.rect(screen, (255, 255, 255), (w, h, BLOCK_SIZE, BLOCK_SIZE), 0)

    fw, fh = font.size("Press 'SPACE' to restart")
    text = font.render("Press 'SPACE' to restart", True, (255, 0, 0))
    screen.blit(text, (10, int(BLOCK_SIZE * 3)))

if __name__ == "__main__":
    main()