import time
import sys
import pygame
from pygame.locals import *
from const import * #使用常量
# 游戏引擎类
class Engine:


    # 构造器 传入棋盘对象
    def __init__(self, board):
        self.board = board

    # 定义gameOver函数
    def gameOver(self, playSurface):
        gameOverFont = pygame.font.Font('arial.ttf',72)
        gameOverSurf = gameOverFont.render('Game Over', True, const.GRAY_COLOR)
        gameOverRect = gameOverSurf.get_rect()
        gameOverRect.midtop = (320, 10)
        playSurface.blit(gameOverSurf, gameOverRect)
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()
