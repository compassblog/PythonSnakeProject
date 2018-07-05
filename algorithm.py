from const import * #使用常量
from board import * # 导入棋盘类
import copy

# 人工智能算法类
class Algorithm:
    # 构造器 传入棋盘对象 构件一个实际棋盘和一个虚拟棋盘
    def __init__(self, board):
        self.board = board

    # 根据食物位置 蛇头位置 蛇身的状态决定移动的方向
    def findDirection(self):
        return "down"

        # 在各种方案都不行时，随便找一个可行的方向来走(1步),
    def any_possible_move(self):
        best_move = "none"
        self.board.board_reset()
        self.board.board_refresh()

        min = const.UNDEFINED
        dir = ["left", "up", "right", "down"]
        for i in range(4):
            # 判断这个点是否能往这个方向移动(去寻找食物)
            if self.board.is_move_possible(self.board.head, dir[i]):
                # 如果可以移动 则直接使用该方向了
                best_move = dir[i]
                break
    
        return best_move

    # 根据食物位置 蛇头位置 蛇身的状态决定移动的方向
    def findDirection(self):
        best_move = self.choose_shortest_safe_move()
        if best_move == "none":
        	best_move = self.any_possible_move()
    
        #return "down"
        return best_move # 真的来了啊

    
    # 从蛇头开始，根据board中元素值，
    # 从蛇头周围4个领域点中选择最短路径
    # 确保移动后蛇头与食物的欧氏距离比移动前的要小即可
    # 返回值为"left" "right" "up" "down" "none"之一
    def choose_shortest_safe_move(self, board = None):
        # 创建虚拟的棋盘 该棋盘可能来源于真实的棋盘 也可能来源于虚拟生成的棋盘
        if board:
            tmpboard = copy.deepcopy(board)
        else:
            tmpboard = copy.deepcopy(self.board)
        
        best_move = "none"
        dir = ["left", "up", "right", "down"]
        for i in range(4):
            # 判断这个点是否能往这个方向移动(去寻找食物)
            if tmpboard.is_move_possible(tmpboard.head, dir[i]):
                # 移动后的点
                next = tmpboard.move(tmpboard.head, dir[i])
                # 判断移动后的点与食物的距离是否比移动前的点与食物的距离要小
                if manhattan_distance(next, tmpboard.food) < manhattan_distance(tmpboard.head, tmpboard.food):
                    # 判断两个点之间是否有障碍(蛇尾)无法直接通过曼哈顿距离到达
                    if not tmpboard.is_obstacle_between(next, tmpboard.food):
                        best_move = dir[i]
                        break
        
        return best_move
    




