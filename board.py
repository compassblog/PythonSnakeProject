import copy

from const import * #使用常量
import math
import random
from itertools import product
import copy

# 棋盘类
class Board:

    # 蛇头蛇尾食物的数据 待初始化
    food = [0,1] # 食物的值
    head = [0,0] # 蛇头的值
    tailArr = [] # 蛇尾数组
    
    def __init__(self):
        # 清空棋盘
        self.board = [[const.UNDEFINED for i in range(const.BOARD_WIDTH)] for i in range(const.BOARD_HEIGHT)]
        
    # 根据位置获得对应的值
    def get_value(self, pos):
        return self.board[pos[1]][pos[0]]

    # 根据位置设置对应的值 (用于board_refresh计算)
    def set_value(self, pos, value):
        self.board[pos[1]][pos[0]] = value

    # 写入food值
    def set_food(self, food):
        self.food = copy.deepcopy(food)
        
    # 写入head
    def set_head(self, head):
        self.head = copy.deepcopy(head)
        
    # 写入tailArr
    def set_tailArr(self, tailArr):
        self.tailArr = copy.deepcopy(tailArr)


    # 初始化食物的位置
    # 返回值 列表 描述生成的食物的位置
    def initFoodPos(self):
        while True:
            x = math.floor(random.random() * const.BOARD_WIDTH)
            y = math.floor(random.random() * const.BOARD_HEIGHT)
            # 新生成的位置不能与蛇头相同
            if [x,y] == self.head:
                continue
            # 新生成的位置不能在蛇尾数组中
            if [x,y] in self.tailArr:
                continue
        
            return [x,y]

        # 根据坐标按照方向查找下一个格子
    def move(self, pos, direction):
        nextPos = copy.deepcopy(pos)
        if direction == "left":
            nextPos[0] -= 1
        elif direction == "right":
            nextPos[0] += 1
        elif direction == "up":
            nextPos[1] -= 1
        elif direction == "down":
            nextPos[1] += 1
        return nextPos

    # 蛇按照方向移动一格
    # 返回True表示正常移动 返回False表示不能移动
    def move_with_tail(self, direction):
        # 判断是否吃到食物
        food_eated = False
        if not self.is_move_possible(self.head, direction):
            return const.STATE_GAMEOVER
        nextPos = self.move(self.head, direction)
        if nextPos in self.tailArr:
            # 蛇尾最后一格例外 
            if not nextPos == self.tailArr[-1]:
                return const.STATE_GAMEOVER

        # 把蛇头插入蛇尾数组
        self.tailArr.insert(0, self.head)

        # 蛇头移动一格
        self.head = self.move(self.head, direction)
        if self.head == self.food:
            # 吃到食物 则重新生成食物的位置
            self.food = self.initFoodPos()
            food_eated = True
        else:
            # 没有吃到 则删除蛇尾的最后一部分
            self.tailArr.pop()

        if food_eated:
            return const.STATE_EAT_FOOD
        else:
            return const.STATE_MOVE

    # 假设蛇头是在位置pos上，检测方向dir是否在棋盘内
    def is_in_board(self, pos, direction):
        nextPos = self.move(pos, direction)
    
        # 越界的判断    
        if nextPos[1] < 0 or nextPos[1] >= const.BOARD_HEIGHT or nextPos[0] < 0 or nextPos[0] >= const.BOARD_WIDTH:
            return False

        return True

    # 假设蛇头是在位置pos上，检测是否可以向方向dir移动
    def is_move_possible(self, pos, direction):
        if not self.is_in_board(pos, direction):
            return False
    
        nextPos = self.move(pos, direction)

        # 碰蛇尾的判断
        if nextPos in self.tailArr:
            # 蛇尾最后一格例外 
            if not nextPos == self.tailArr[-1]:
                return False
        return True

    # 打印board 仅为调试用
    def board_print(self):
        # 注意board[1][2]表示第2行第1列
        for i in range(0, const.BOARD_HEIGHT):
            for j in range(0, const.BOARD_WIDTH):
                # 使用F表示食物 H表示蛇头 T表示蛇尾
                value = str(self.board[i][j])
                if self.board[i][j] == const.FOOD:
                    value = "F"
                elif self.board[i][j] == const.SNAKE_HEAD:
                    value = "H"
                elif self.board[i][j] == const.SNAKE_TAIL:
                    value = "T"
                print(value, end=' ')
                if self.board[i][j] <= 9:
                    print(end=' ')
            
            print() # 换行

        print() # 换行

    # 重置board 把board中除了food head tailArr之外的内容全部重置为UNDEFINED
    # 后面在board_refresh中都会变为到达食物的路径的长度
    def board_reset(self):
        # 设置棋盘中的值
        for i, j in product(range(0, const.BOARD_WIDTH), range(0, const.BOARD_HEIGHT)):
            # 食物
            if [i,j] == self.food:
                self.board[j][i] = const.FOOD
            # 蛇头
            elif [i,j] == self.head:
                self.board[j][i] = const.SNAKE_HEAD
            # 蛇身
            elif [i,j] in self.tailArr:
                self.board[j][i] = const.SNAKE_TAIL
            # 其他
            else:
                self.board[j][i] = const.UNDEFINED

    # 判断两个点之间是否有障碍(蛇尾)无法直接通过曼哈顿距离到达
    # 返回值为True(有障碍)或False(无障碍)
    def is_obstacle_between(self, startPos, endPos):
        # 两点重合 则肯定无障碍了
        if startPos == endPos:
            return False
    
        dir = ["left", "up", "right", "down"]
        for i in range(4):
            # 判断这个点是否能往这个方向移动(去寻找食物)
            if self.is_move_possible(startPos, dir[i]):
                # 移动后的点
                next = self.move(startPos, dir[i])
                # 如果移动后的点与目标点的距离比移动前的点与目标点的距离要小 则直接忽略
                if manhattan_distance(next, endPos) > manhattan_distance(startPos, endPos):
                    continue
                # 对移动后的点进行判断
                if next == endPos:
                    # 如果移动后的下一步就是目标 则直接返回False
                    return False
                else:
                    # 否则对移动后的点与目标点之间的障碍进一步的递归
                    ret = self.is_obstacle_between(next, endPos)
                    # 如果移动后没有障碍可以直达 则直接返回False 否则尝试下一个方向
                    if not ret:
                        return False
    
        # 只有尝试了所有的方向后 才返回True
        return True

    # 从食物位置出发 广度优先搜索遍历整个board
    # 计算出board中每个非SNAKE元素到达食物的路径长度
    def board_refresh(self):
        # 把遍历过的点压到queue堆栈中 while循环每次从queue中取一个点作为下一次的遍历 直到queue为空
        queue = []
        # 先把食物的点压到堆栈中
        queue.append(self.food)
        # inqueue用于记录该点是否被访问过 未访问过的点置0 访问过的点置1
        inqueue = [[0 for i in range(const.BOARD_WIDTH)] for i in range(const.BOARD_HEIGHT)]
        # found表示是否能找到蛇头 如果找到则表示可以吃到食物 则设置该值为True
        found = False
        # 当while循环结束后 除了蛇头蛇身还有不可达的地方 
        # 其他每个方格中的数字代表从它到食物的路径长度
        while True:
            # 如果queue中已经没有可以遍历的点了 则退出循环
            if len(queue) == 0:
                break
            # 从queue中取出一个点
            idx = queue.pop(0)

            # 如果这个点已经访问过的 则忽略
            if inqueue[idx[1]][idx[0]] == 1:
                continue
            # 把这个点设置为已经访问过了
            inqueue[idx[1]][idx[0]] = 1
            
            #print("idx = ", idx)
            # 遍历4个方向
            dir = ["left", "up", "right", "down"]
            for i in range(4):
                # 判断这个点是否能往这个方向移动(去寻找食物)
                if self.is_move_possible(idx, dir[i]):
                    # 如果可以移动 则对移动后的点进行判断
                    next = self.move(idx, dir[i])
                    # 如果移动后的点是蛇头 则循环结束
                    if next == self.head:
                        found = True
                    # 如果移动后的点不是蛇的身子 则可以把该点记录下来
                    elif next not in self.tailArr: 
                        # 如果该点的现在计算出来的距离比原来的要小(包括无限远) 则把现在计算出来的距离写入
                        if self.get_value(next) > self.get_value(idx) + 1:
                            # 注意食物旁边的点需要标记为1 其他点则标记为参考点的值+1 
                            if self.get_value(idx) == const.FOOD:
                                self.set_value(next, 1)
                            else:
                                self.set_value(next, self.get_value(idx) + 1)
                        # 如果该点没有在inqueue被标记 就是没有被访问过 则把该点添加到queue中
                        if inqueue[next[1]][next[0]] == 0:
                            queue.append(next)

        return found






