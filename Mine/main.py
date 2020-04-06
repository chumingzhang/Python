import sys
import time
import pygame

from tkinter import * 

from enum import Enum
from pygame.locals import *
from mineblock import *

# 游戏屏幕的宽
SCREEN_WIDTH = BLOCK_WIDTH * SIZE
# 游戏屏幕的高
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE

class GameStatus(Enum):
    readied = 1,
    started = 2,
    over = 3,
    win = 4

# 绘制信息
def print_text(screen, font, x, y, text, fcolor):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

# 根据选择的游戏难度改变埋雷数
def choice1():
    change_MINE_COUNT(30)

def choice2():
    change_MINE_COUNT(60)

def choice3():
    change_MINE_COUNT(99)

# 选择游戏难度
def choose_degree():
    root = Tk()
    ch1 = Checkbutton(root, text = 'Easy',  command = choice1)
    ch1.pack(anchor = NW)
    ch2 = Checkbutton(root, text = 'Median',  command = choice2)
    ch2.pack(anchor = NW)
    ch3 = Checkbutton(root, text = 'Hard',  command = choice3)
    ch3.pack(anchor = NW)
    
    mainloop()

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('扫雷')

    font1 = pygame.font.Font('Mine/a.TTF', SIZE * 2)  # 得分的字体
    fwidth, fheight = font1.size('999')
    red = (200, 40, 40)

    # 加载资源图片，因为资源文件大小不一，所以做了统一的缩放处理
    img0 = pygame.image.load('Mine/images/0.bmp').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('Mine/images/1.bmp').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('Mine/images/2.bmp').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('Mine/images/3.bmp').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('Mine/images/4.bmp').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('Mine/images/5.bmp').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('Mine/images/6.bmp').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('Mine/images/7.bmp').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('Mine/images/8.bmp').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_blank = pygame.image.load('Mine/images/blank.bmp').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    img_flag = pygame.image.load('Mine/images/flag.bmp').convert()
    img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))
    img_ask = pygame.image.load('Mine/images/ask.bmp').convert()
    img_ask = pygame.transform.smoothscale(img_ask, (SIZE, SIZE))
    img_mine = pygame.image.load('Mine/images/mine.bmp').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    img_blood = pygame.image.load('Mine/images/blood.bmp').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    img_error = pygame.image.load('Mine/images/error.bmp').convert()
    img_error = pygame.transform.smoothscale(img_error, (SIZE, SIZE))
    face_size = int(SIZE * 1.25)
    img_face_fail = pygame.image.load('Mine/images/face_fail.bmp').convert()
    img_face_fail = pygame.transform.smoothscale(img_face_fail, (face_size, face_size))
    img_face_normal = pygame.image.load('Mine/images/face_normal.bmp').convert()
    img_face_normal = pygame.transform.smoothscale(img_face_normal, (face_size, face_size))
    img_face_success = pygame.image.load('Mine/images/face_success.bmp').convert()
    img_face_success = pygame.transform.smoothscale(img_face_success, (face_size, face_size))
    face_pos_x = (SCREEN_WIDTH - face_size) // 2
    face_pos_y = (SIZE * 2 - face_size) // 2

    img_dict = {
        0: img0,
        1: img1,
        2: img2,
        3: img3,
        4: img4,
        5: img5,
        6: img6,
        7: img7,
        8: img8
    }

    bgcolor = (225, 225, 225)   # 背景色

    block = MineBlock()
    game_status = GameStatus.readied
    start_time = None   # 开始时间
    elapsed_time = 0    # 耗时

    while True:
        # 填充背景色
        screen.fill(bgcolor)

        for event in pygame.event.get():
            # 退出事件
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # 按下鼠标事件
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2     # -2为显示状态栏的偏移量
#                print(x, y)
                b1, b2, b3 = pygame.mouse.get_pressed()
                if game_status == GameStatus.started:
                    # 鼠标左右键同时按下，如果已经标记了所有雷，则打开周围一圈
                    # 如果还未标记完所有雷，则有一个周围一圈被同时按下的效果
                    if b1 and b3:
                        mine = block.getmine(x, y)
                        # 同时按下鼠标左右键只对已打开的块有效
                        if mine.status == BlockStatus.opened:
                            block.double_mouse_button_down(x, y)

            # 鼠标抬起事件                
            elif event.type == MOUSEBUTTONUP:
                # 点击到表情位置, 重开游戏
                if face_pos_x <= mouse_x <= face_pos_x + face_size \
                        and face_pos_y <= mouse_y <= face_pos_y + face_size:
                    game_status = GameStatus.readied
                    # 重置block，只是为了显示，还没有确定难度（雷数）
                    block = MineBlock()
                    continue
                
                if y >= 0: # 防止点到状态栏除导致getmine(x, y)越界
                    if game_status == GameStatus.readied:
                        game_status = GameStatus.started
                        choose_degree()
                        # 真正重置block
                        block = MineBlock()
                        start_time = time.time()
                        elapsed_time = 0
                        

                    if game_status == GameStatus.started:
                        mine = block.getmine(x, y)
                        if b1 and not b3:       # 按鼠标左键
                            if mine.status == BlockStatus.normal:
                                if not block.open_mine(x, y):
                                    game_status = GameStatus.over
                        elif not b1 and b3:     # 按鼠标右键，标记状态循环
                            if mine.status == BlockStatus.normal:
                                mine.status = BlockStatus.flag
                            elif mine.status == BlockStatus.flag:
                                mine.status = BlockStatus.ask
                            elif mine.status == BlockStatus.ask:
                                mine.status = BlockStatus.normal
                        elif b1 and b3:
                            if mine.status == BlockStatus.double:
                                block.double_mouse_button_up(x, y)

        # 已开个数      
        opened_count = 0
        # 画图，顺便计数
        for row in block.block:
            for mine in row:
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if mine.status == BlockStatus.opened:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                    opened_count += 1
                elif mine.status == BlockStatus.double:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                elif mine.status == BlockStatus.bomb:
                    screen.blit(img_blood, pos)
                elif mine.status == BlockStatus.flag:
                    screen.blit(img_flag, pos)
                elif mine.status == BlockStatus.ask:
                    screen.blit(img_ask, pos)
                elif mine.status == BlockStatus.hint:
                    screen.blit(img0, pos)
                elif game_status == GameStatus.over and mine.value:
                    screen.blit(img_mine, pos)
                elif mine.value == 0 and mine.status == BlockStatus.flag:
                    screen.blit(img_error, pos)
                elif mine.status == BlockStatus.normal:
                    screen.blit(img_blank, pos)

        # 绘制剩余雷数
        print_text(screen, font1, 30, (SIZE * 2 - fheight) // 2 - 2, '%02d' % (get_MINE_COUNT() - flag_count), red)
        # 绘制用时
        if game_status == GameStatus.started:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, font1, SCREEN_WIDTH - fwidth - 30, (SIZE * 2 - fheight) // 2 - 2, '%03d' % elapsed_time, red)

        if opened_count == BLOCK_WIDTH * BLOCK_HEIGHT - get_MINE_COUNT():
            game_status = GameStatus.win

        # 显示不同表情
        if game_status == GameStatus.over:
            screen.blit(img_face_fail, (face_pos_x, face_pos_y))
        elif game_status == GameStatus.win:
            screen.blit(img_face_success, (face_pos_x, face_pos_y))
        else:
            screen.blit(img_face_normal, (face_pos_x, face_pos_y))

        pygame.display.update()

if __name__ == '__main__':
    main()