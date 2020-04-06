import sys
import time
import pygame
from pygame.locals import *
import blocks

SIZE = 30                                # 每个小方格大小
BLOCK_HEIGHT = 20                        # 游戏区高度
BLOCK_WIDTH = 10                         # 游戏区宽度
BORDER_WIDTH = 4                         # 游戏区边框宽度
BORDER_COLOR = (40, 40, 200)             # 游戏区边框颜色
SCREEN_WIDTH = SIZE * (BLOCK_WIDTH + 5)  # 游戏屏幕的宽(偏移量为状态栏)
SCREEN_HEIGHT = SIZE * BLOCK_HEIGHT      # 游戏屏幕的高
BG_COLOR = (40, 40, 60)                  # 背景色
BLOCK_COLOR = (20, 128, 200)             # 方块颜色
BLACK = (0, 0, 0)
RED = (200, 30, 30)                      # GAME OVER 的字体颜色


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    font1 = pygame.font.SysFont('SimHei', 24)            # 状态信息，黑体24
    font2 = pygame.font.Font(None, 72)                   # GAME OVER 的字体
    font3 = pygame.font.SysFont('SimHei', 20)            # 按键操作说明信息  
    font_pos_x = BLOCK_WIDTH * SIZE + BORDER_WIDTH + 10  # 右侧信息显示区域字体位置的X坐标
    gameover_size = font2.size('GAME OVER')
    font1_height = int(font1.size('Score')[1])            # 字体高度

    cur_block = None                # 当前下落方块
    next_block = None               # 下一个要落下的方块（而不是当前方块旋转的下一个图形）
    cur_pos_x, cur_pos_y = 0, 0     # 正在下落的方块的位置

    game_area = None                # 整个游戏区域 0->有方块
    game_over = True
    start = False                   # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    score = 0                       # 得分
    oriSpeed = 0.8                  # 原始速度
    speed =  oriSpeed               # 自然下落速度(两次刷新的时间间隔),调整游戏难度
    pause = False                   # 暂停

    # 两次自然下落的时间差为方块碰撞后仍然可以左右移动的时间
    last_drop_time = None           # 上次自然下落时间
    # 如果没有时间间隔则按住不放时会迅速结束游戏
    last_press_time = None          # 上次按键时间

    def _dock():
        # nonlocal修饰后为main函数内的变量（即上面定义的变量）
        nonlocal cur_block, next_block, cur_pos_x, cur_pos_y, game_area, game_over, score, speed
        for _i in range(cur_block.start_pos.Y, cur_block.end_pos.Y + 1):
            for _j in range(cur_block.start_pos.X, cur_block.end_pos.X + 1):
                if cur_block.template[_i][_j] == 'O':
                    game_area[cur_pos_y + _i][cur_pos_x + _j] = '0'

        # 判断是否游戏结束
        if cur_pos_y + cur_block.start_pos.Y <= 0:
            game_over = True
        else:
            # 计算消除
            remove_idxs = []
            # 遍历当前block高度所占的行
            for _i in range(cur_block.start_pos.Y, cur_block.end_pos.Y + 1):
                # 一行都为0时需要移除
                if all(_x == '0' for _x in game_area[cur_pos_y + _i]):
                    # 记录要被移除的行数
                    remove_idxs.append(cur_pos_y + _i)

            if remove_idxs:
                # 计算得分
                remove_count = len(remove_idxs)
                if remove_count == 1:
                    score += 100
                elif remove_count == 2:
                    score += 300
                elif remove_count == 3:
                    score += 700
                elif remove_count == 4:
                    score += 1500
                # 根据得分改变速度
                if(speed > 0.3):
                    speed = oriSpeed - 0.1 * (score // 2000)
                # 消除
                _i = _j = remove_idxs[-1]
                while _i >= 0:
                    # _j为没有被消除的第一行
                    while _j in remove_idxs:
                        _j -= 1
                    # 如果_j < 0，表示已经超出屏幕外，屏幕内的都被清除了，直接清空_i行
                    if _j < 0:
                        game_area[_i] = ['.'] * BLOCK_WIDTH
                    # 否则_i行改成未被清除的行
                    else:
                        game_area[_i] = game_area[_j]
                    # 注意_j也要-1找到下一行(上一行)
                    _i -= 1
                    _j -= 1

            cur_block = next_block
            next_block = blocks.get_block()
            # 初始化正在掉落的方块在屏幕中的单位位置（x在中间，y为负数在屏幕外）
            cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos.X - 1) // 2, -1 - cur_block.end_pos.Y

    # 判断是否可以旋转
    def _judge(pos_x, pos_y, block):
        nonlocal game_area
        for _i in range(block.start_pos.Y, block.end_pos.Y + 1):
            # 行高超出屏幕
            if pos_y + block.end_pos.Y >= BLOCK_HEIGHT:
                return False
            # 与已有单位接触
            for _j in range(block.start_pos.X, block.end_pos.X + 1):
                if pos_y + _i >= 0 and block.template[_i][_j] != '.' and game_area[pos_y + _i][pos_x + _j] != '.':
                    return False
        return True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 回车键开始游戏
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        score = 0
                        last_drop_time = time.time()
                        last_press_time = time.time()
                        # 整个游戏区域全部置为'.'
                        game_area = [['.'] * BLOCK_WIDTH for _ in range(BLOCK_HEIGHT)]
                        cur_block = blocks.get_block()
                        next_block = blocks.get_block()
                        cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos.X - 1) // 2, -1 - cur_block.end_pos.Y
                # 空格键暂停
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                # 上键旋转图形
                elif event.key == K_UP:
                    # 旋转
                    # .0.
                    # .00
                    # ..0
                    # 这个在最右边靠边的情况下不能旋转
                    # 在形状设计的时候做了很多的空白，这样只需要规定整个形状包括空白部分全部在游戏区域内时才可以旋转
                    if 0 <= cur_pos_x <= BLOCK_WIDTH - len(cur_block.template[0]):
                        _next_block = blocks.get_next_block(cur_block)
                        # 判断旋转后图形是否超出屏幕高度或者与已有单位块重叠
                        if _judge(cur_pos_x, cur_pos_y, _next_block):
                            cur_block = _next_block

        # 左右下三个移动键放外面判断是为了实现按着不动时能实现连续移动
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not game_over and not pause:
                    if time.time() - last_press_time > 0.1:
                        last_press_time = time.time()
                        # 不能移出左边框
                        if cur_pos_x > - cur_block.start_pos.X:
                            if _judge(cur_pos_x - 1, cur_pos_y, cur_block):
                                cur_pos_x -= 1
            if event.key == pygame.K_RIGHT:
                if not game_over and not pause:
                    if time.time() - last_press_time > 0.1:
                        last_press_time = time.time()
                        # 不能移出右边框
                        if cur_pos_x + cur_block.end_pos.X + 1 < BLOCK_WIDTH:
                            if _judge(cur_pos_x + 1, cur_pos_y, cur_block):
                                cur_pos_x += 1
            if event.key == pygame.K_DOWN:
                if not game_over and not pause:
                    # 间隔设置小一点则移动快一点
                    if time.time() - last_press_time > 0.05:
                        last_press_time = time.time()
                        # 如果当前块已撞（停止运动），则下一块
                        if not _judge(cur_pos_x, cur_pos_y + 1, cur_block):
                            _dock()
                        else:
                            last_drop_time = time.time()
                            cur_pos_y += 1

        _draw_background(screen)
        _draw_game_area(screen, game_area)
        _draw_gridlines(screen)
        # 右侧状态信息
        _draw_info(screen, font1, font_pos_x, font1_height, score)
        # 按键操作说明信息
        if start == False:
            _draw_key_info(screen, font3, font_pos_x, font1_height)
        # 画显示信息中的下一个方块
        _draw_block(screen, next_block, font_pos_x, 30 + (font1_height + 6) * 5, 0, 0)

        if not game_over:
            cur_drop_time = time.time()
            # 用两次自然下落的时间差来判断当前方块是否碰撞，因为方块落到底的瞬间是可以进行左右移动
            if cur_drop_time - last_drop_time > speed:
                if not pause:
                    if not _judge(cur_pos_x, cur_pos_y + 1, cur_block):
                        _dock()
                    else:
                        last_drop_time = cur_drop_time
                        cur_pos_y += 1
        else:
            if start:
                print_text(screen, font2,
                           (SCREEN_WIDTH - gameover_size[0]) // 2, (SCREEN_HEIGHT - gameover_size[1]) // 2,
                            'GAME OVER', RED)

        # 画当前下落方块
        _draw_block(screen, cur_block, 0, 0, cur_pos_x, cur_pos_y)

        pygame.display.flip()


# 画背景
def _draw_background(screen):
    # 填充背景色
    screen.fill(BG_COLOR)
    # 画游戏区域分隔线
    pygame.draw.line(screen, BORDER_COLOR,
                     (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, 0),
                     (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, SCREEN_HEIGHT), BORDER_WIDTH)


# 画已经落下的方块
def _draw_game_area(screen, game_area):
    if game_area:
        for i, row in enumerate(game_area):
            for j, cell in enumerate(row):
                if cell != '.':
                    pygame.draw.rect(screen, BLOCK_COLOR, (j * SIZE, i * SIZE, SIZE, SIZE), 0)


# 画网格线
def _draw_gridlines(screen):
    # 画网格线 竖线
    for x in range(BLOCK_WIDTH):
        pygame.draw.line(screen, BLACK, (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
    # 画网格线 横线
    for y in range(BLOCK_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, y * SIZE), (BLOCK_WIDTH * SIZE, y * SIZE), 1)


# 画单个方块
def _draw_block(screen, block, offset_x, offset_y, pos_x, pos_y):
    if block:
        for i in range(block.start_pos.Y, block.end_pos.Y + 1):
            for j in range(block.start_pos.X, block.end_pos.X + 1):
                if block.template[i][j] != '.':
                    pygame.draw.rect(screen, BLOCK_COLOR,
                                     (offset_x + (pos_x + j) * SIZE, offset_y + (pos_y + i) * SIZE, SIZE, SIZE), 0)


# 画得分等信息
def _draw_info(screen, font, pos_x, font_height, score):
    print_text(screen, font, pos_x, 10, f'Score: ')
    print_text(screen, font, pos_x, 10 + font_height + 6, f'{score}')
    print_text(screen, font, pos_x, 20 + (font_height + 6) * 2, f'Speed: ')
    print_text(screen, font, pos_x, 20 + (font_height + 6) * 3, f'{score // 10000}')
    print_text(screen, font, pos_x, 30 + (font_height + 6) * 4, f'Next: ')


def _draw_key_info(screen, font, pos_x, font_height):
    print_text(screen, font, 10, font_height * 8, f"Press 'Enter' to restart")
    print_text(screen, font, 10, font_height * 10, f"Press 'Space' to pause/start")
    print_text(screen, font, 10, font_height * 12, f"Press '↑' to rotate")


if __name__ == '__main__':
    main()
