import sys
import pygame
from pygame.locals import * # QUIT
from board import *
from const import *
from engine import *
from algorithm import *

def main():
    """
    main函数
    """
    board = Board()
    engine = Engine(board)
    algorithm = Algorithm(board)
    # 初始化pygame
    pygame.init()
    # 初始化时钟对象
    fpsClock = pygame.time.Clock()

    # 创建一个窗口
    SCREEN_SIZE = (const.BOARD_WIDTH * const.BOX, const.BOARD_HEIGHT * const.BOX)
    # 设置窗口的状态
    # 参数1 分辨率 必须为元组
    # 参数2 标志位 如果不用什么特性，就指定0 可以指定为FULLSCREEN
    # 参数3 色深
    # 返回一个pygame.Surface对象，代表了在桌面上出现的那个窗口
    playSurface = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    
    # 设置窗口标题
    pygame.display.set_caption("贪吃蛇")
     # 设置重要的参数
    board.set_head([0,0])  # 蛇头的位置
    board.set_tailArr([]) # 蛇尾的数组
    # 初始化食物的位置
    foodPos = board.initFoodPos()
    board.set_food(foodPos)
    # 开始的方向
    direction = 'right'

    # 游戏主循环
    while True:
        for event in pygame.event.get():
            # 接收到退出事件后退出程序
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            '''elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == K_RIGHT or event.key == ord('d'):
                    direction = 'right'
                if event.key == K_LEFT or event.key == ord('a'):
                    direction = 'left'
                if event.key == K_UP or event.key == ord('w'):
                    direction = 'up'
                if event.key == K_DOWN or event.key == ord('s'):
                    direction = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))'''

        # 根据食物位置 蛇头位置 蛇身的状态决定移动的方向
        direction = algorithm.findDirection()
        if direction == "none":
            engine.gameOver(playSurface)

        # 根据方向移动蛇头的坐标
        cur_state = board.move_with_tail(direction)

         # 绘制pygame显示层
        playSurface.fill(const.BLACK_COLOR)
        # 绘制食物
        # rect() 绘制矩形
        # 参数1 surface pygame.Surface对象 在桌面上出现的那个窗口
        # 参数2 color 表示颜色 pygame.Color对象
        # 参数3 Rect 表示要绘制的矩形 (startX, startY, Xlen, Ylen)
        pygame.draw.rect(playSurface, const.RED_COLOR, Rect(board.food[0] * const.BOX, board.food[1] * const.BOX, const.BOX, const.BOX))
        # 绘制蛇头
        pygame.draw.rect(playSurface, const.WHITE_COLOR, Rect(board.head[0] * const.BOX, board.head[1] * const.BOX, const.BOX, const.BOX))
        
        # 绘制蛇尾数组
        for position in board.tailArr:
            pygame.draw.rect(playSurface, const.GRAY_COLOR, Rect(position[0] * const.BOX, position[1] * const.BOX, const.BOX, const.BOX))

        # 刷新pygame显示层
        pygame.display.flip()

        # 判断是否死亡
        if cur_state == const.STATE_GAMEOVER:
            engine.gameOver(playSurface)

        # 控制游戏速度
        fpsClock.tick(5)

def test_move_possible():
    # T H N N N N N
    # T T N N N N N
    # N N N N N N N
    # N N N N N N N
    # N N N N F N N
    board = Board()
    board.set_food([4,4])
    board.set_head([1,0])
    board.set_tailArr([[0,0],[0,1],[1,1]])
    # 测试往空白位置移动
    ret = board.is_move_possible([1,0], "right")
    print(ret) # 期望值为True
    # 测试往边界移动
    ret = board.is_move_possible([1,0], "up")
    print(ret) # 期望值为False
    # 测试往蛇尾移动(非最后一格)
    ret = board.is_move_possible([1,0], "left")
    print(ret) # 期望值为False
    # 测试往蛇尾移动(最后一格)
    ret = board.is_move_possible([1,0], "down")
    print(ret) # 期望值为True

def test_board_reset():
    # T N H N N N N
    # T T T N N N N
    # N N N N N N N
    # N N N F N N N
    # N N N N N N N
    board = Board()
    board.set_food([3,3])
    board.set_head([2,0])
    board.set_tailArr([[2,1],[1,1],[0,1],[0,0]])
    board.board_reset()
    board.board_print()

def test_board_refresh():
    # N H N N N N N
    # N N F N N N N
    # N N N N N N N
    # N N N N N N N
    # N N N N N N N
    board = Board()
    board.set_food([2,1]) # 食物的位置
    board.set_head([1,0])  # 蛇头的位置
    board.set_tailArr([]) # 蛇尾的数组
    board.board_reset()
    board.board_refresh()
    board.board_print()
    # T N H N N N N
    # T T T N N N N
    # N N N N N N N
    # N N N F N N N
    # N N N N N N N
    board.set_food([3,3]) # 食物的位置
    board.set_head([2,0])  # 蛇头的位置
    board.set_tailArr([[2,1],[1,1],[0,1],[0,0]]) # 蛇尾的数组
    board.board_reset()
    board.board_refresh()
    board.board_print()




if __name__ == "__main__":
    main()

