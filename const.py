#coding:utf-8
import pygame
from pygame.locals import *

class _const:
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value

    # 计算两点之间的曼哈顿距离(L1距离)
def manhattan_distance(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])



# 在这里初始化常量后 即不可改变
const = _const()
const.BOX = 20 # 一个格子的大小
#const.BOARD_WIDTH = 7 # 盘面的宽度
#const.BOARD_HEIGHT = 5 # 盘面的高度
const.BOARD_WIDTH = 50 
const.BOARD_HEIGHT = 30

# 定义棋盘中食物 蛇头 蛇尾的常量值 用于board的记录
const.UNDEFINED = const.BOARD_WIDTH * const.BOARD_HEIGHT + 1 # 就是无限远的意思
const.FOOD = -1
const.SNAKE_HEAD = -2
const.SNAKE_TAIL = -3 

# 定义颜色变量
const.RED_COLOR = pygame.Color(255,0,0)
const.BLACK_COLOR = pygame.Color(0,0,0)
const.WHITE_COLOR = pygame.Color(255,255,255)
const.GRAY_COLOR = pygame.Color(150,150,150)

# 移动一步后的状态
const.STATE_GAMEOVER = 0 # 游戏结束
const.STATE_MOVE = 1     # 移动一格
const.STATE_EAT_FOOD = 2 # 吃食物

