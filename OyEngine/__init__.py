#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 17:35
# @Author  : Aries
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
import pygame
import math
import random
import sys
from enum import Enum
from pygame.locals import *
from pygame.math import *
#在这里初始化游戏的所有资源和变量
pygame.init()
# 一些关于长度的常量定义
    #窗体
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
    #外圆半径圆心
RADIUS_OUT=280
OUT_POSITION=(WINDOW_WIDTH//2,WINDOW_HEIGHT//2)
    #球半径
BALL_RADIUS=6
    #砖长宽
TRICK_HEIGHT=16
TRICK_WIDTH=30
TRICK_PAD=8
#颜色
COLORS={'white':(255,255,255),
        'light_blue':(100,100,255),
        'black':(0,0,0),
        'ball':(102,255,100),
        'gray':(200, 200, 200),
        'yellow':(238,173,14),
        'light_red':(255,100,100),
        'enemy1':(255,106,106),
        'enemy2':(238,99,99),
        'enemy3':(255,130,71),
        }
#砖块
    #刷出砖块的起点和终点
trick_area=[(WINDOW_WIDTH//2-TRICK_WIDTH*10,WINDOW_HEIGHT//2-TRICK_HEIGHT*10),(WINDOW_WIDTH//2+TRICK_WIDTH*10,WINDOW_HEIGHT//2+TRICK_HEIGHT*10)]
#时间
FPS=40
detalTime=0#每帧的时间 s
mPos=(0,0) #鼠标的位置
mpol=math.pi*1.5     #鼠标的方位角
#游戏逻辑
    #游戏
class GameState(Enum):
    start=0     #游戏开始界面
    init=1      #加载一局的游戏资源
    play=2      #玩游戏中
    finish=3    #游戏结束
    pass
current_state=GameState.start#当前游戏状态
global GAME_SPEED
GAME_SPEED=1  #游戏速度
    #玩家
HP_LIMIT=3
global player_hp
player_hp=HP_LIMIT #玩家生命条数
global score,level
level=0
score=0
PLAYER_START_POS=math.pi*1
player_pos=PLAYER_START_POS      #玩家位置，处于下方的-90度
PLAYER_V=2                      #玩家旋转角速度
player_current_v=0              #玩家当前速度
PLAYER_FRI=30                    #挡板摩擦力。越大对球的切向加速越快
PLAYER_RADIAN=math.pi*0.1        #玩家挡板弧度
PLAYER_HEIGHT=10                 #玩家挡板高度
paddle_move_left=False      #玩家按键
paddle_move_right=False
    #protect area
PLAYER_PROTECT_RADIAN=math.pi*0.9#玩家保护区弧度
protect_pos=player_pos           #保护区起始位置，弧度
protect_v=0.05                   #保护区 弧度移动速度
        #球的速度和位置
global vel,ball_pos
vel=Vector2()
ball_pos=Vector2()
BALL_V=130       #球初始速度基值
#敌人
ENEMY_SPAWN_RADIUS=RADIUS_OUT//2 #生成敌人的半径圆域
ENEMY_MAX_R=20  #生成球的最大半径
ENEMY_MIN_R=12   #生成球的最小半径
global enemys #[(pos,r,color)] 敌人列表
enemys=[]


#<editor-fold title='游戏对象的初始化'>
#UI
startTip = pygame.font.SysFont('arial', 48)
mousePos = pygame.font.SysFont('arial', 20)
scoreText = pygame.font.SysFont('arial', 40)
#init game frame
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #窗口
pygame.display.set_caption('Circle Breaker')#the name of the window
clock=pygame.time.Clock()#timer

#</editor-fold>


