#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/17 15:56
# @Author  : Aries
# @Site    : 
# @File    : Functions.py
# @Software: PyCharm
from OyEngine import *

# <editor-fold desc="functions">
def Terminate():# 退出游戏
    pygame.quit()
    sys.exit()
def DrawText(text, font, surface, x, y):# 显示文字
    text_obj = font.render(text, 1, COLORS['black'])
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
def WaitForPlayerToPressKey():# 等待用户输入.点击鼠标或者按键均不再阻塞。
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                Terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Terminate()
                return
            if event.type==MOUSEBUTTONDOWN:
                return
        clock.tick(FPS)
def InstantiateBricks():
    pass
def InitBallData():
    global ball_pos,vel
    theta=random.uniform(0,2*math.pi)
    ball_pos.x=int(WINDOW_WIDTH/2+math.cos(theta)*RADIUS_OUT*0.6)
    ball_pos.y=int(WINDOW_HEIGHT/2+math.sin(theta)*RADIUS_OUT*0.6)
    if random.randint(0,1):
        vel.x=random.uniform(BALL_V/2,BALL_V)
    else:
        vel.x=random.uniform(-BALL_V/2,-BALL_V)
    if random.randint(0, 1):
        vel.y = random.uniform(BALL_V / 2, BALL_V)
    else:
        vel.y = random.uniform(-BALL_V / 2, -BALL_V)
def OuterCollision(outRadius):#内圆弧和球碰撞
    global ball_pos,vel
    if (ball_pos.x-OUT_POSITION[0])**2+(ball_pos.y-OUT_POSITION[1])**2>=(BALL_RADIUS-outRadius)**2:
        fa=Vector2(OUT_POSITION[0]-ball_pos.x,OUT_POSITION[1]-ball_pos.y).normalize() #指向圆心的法线
        dif=Vector2.dot(vel,fa)
        if dif<0:   #防止内部反弹
            vel-=fa*2*Vector2.dot(vel,fa)
        if (ball_pos.x+vel.x*detalTime - OUT_POSITION[0]) ** 2 + (ball_pos.y+vel.y*detalTime - OUT_POSITION[1]) ** 2 >= (BALL_RADIUS - outRadius) ** 2:#如果下一次球还是处于碰撞，则先移动一次
            ball_pos+=vel*detalTime
        return True
    return False
def PointCollision(pos=Vector2(),r=0):#球和点的碰撞
    global ball_pos,vel
    if (ball_pos-pos).length()<=r+BALL_RADIUS:
       # print('point')
        fa=(pos-ball_pos).normalize()
        dif=Vector2.dot(vel,fa )
        if dif>0:   #防止内部反弹
         vel -= fa * 2 * Vector2.dot(vel, fa)
        return True
    return False
def InitEnemyData():
    global enemys

    lX=[i*WINDOW_WIDTH/(ENEMY_SPAWN_RADIUS/ENEMY_MAX_R*2) for i in range(ENEMY_SPAWN_RADIUS//ENEMY_MIN_R*2)]
    lY=[i*WINDOW_HEIGHT/(ENEMY_SPAWN_RADIUS/ENEMY_MAX_R*2) for i in range(ENEMY_SPAWN_RADIUS//ENEMY_MIN_R*2)]
    for x in lX:
        for y in lY:
            if (Vector2(x,y)-Vector2(OUT_POSITION)).length()<ENEMY_SPAWN_RADIUS:
                r = random.randint(ENEMY_MIN_R, ENEMY_MAX_R)
                col = random.randint(1, 3)
                enemys+=[((int(x),int(y)),r,'enemy'+str(col))]
                pass
            pass
    #print(enemys)
    pass
def InitLevel():#刷新关卡信息，玩家生命值，关卡数，分数
    global level,score,player_hp,GAME_SPEED
    level=0
    score=0
    player_hp=HP_LIMIT
    GAME_SPEED=1
def PassLevel():
    global level,score,GAME_SPEED
    score += 10
    level += 1
    GAME_SPEED += 0.1
# </editor-fold>
