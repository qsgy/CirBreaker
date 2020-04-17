#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 17:35
# @Author  : Aries
# @Site    : 
# @File    : Cir.py
# @Software: PyCharm
#<editor-fold title='imports'>
import math
import random
import sys
from enum import Enum

import pygame
from pygame.locals import *
from pygame.math import *
from OyEngine import *
#</editor-fold>
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

#main logic游戏主逻辑
while True:
    screen.fill(COLORS['gray'])  #处理逻辑钱，清空画布
    pygame.draw.circle(screen,COLORS['white'],OUT_POSITION,RADIUS_OUT+10,10)

    #<editor-fold title='游戏状态的逻辑'>
    if  current_state==GameState.start:
        DrawText('Press any key to start', startTip, screen,
                 WINDOW_WIDTH / 2 - startTip.size('Press any key to start')[0] / 2,
                 WINDOW_HEIGHT / 2)  # 取屏幕中心减去文字宽度的一般，使得文字处于中心
        pygame.display.update()#更新画布
        WaitForPlayerToPressKey()
        current_state=GameState.init
        continue
    elif current_state==GameState.init:
        InitBallData()#刷新球的数据
        InitEnemyData()#刷新敌人的数据
        current_state=GameState.play
        continue
    elif current_state==GameState.play:
        if player_hp<=0:
            current_state=GameState.finish
        pass
        if len(enemys)==0:    #如果击杀一关的敌人.游戏速度加快，加十分
            InitEnemyData()
            PassLevel()


    elif current_state==GameState.finish:  #玩家死亡
        DrawText('Your score is:'+str(score)+',level:'+str(level), startTip, screen,
                 WINDOW_WIDTH / 2 - startTip.size('Press any key to start')[0] / 2,
                 WINDOW_HEIGHT / 2)  # 取屏幕中心减去文字宽度的一般，使得文字处于中心
        pygame.display.update()  # 更新画布
        WaitForPlayerToPressKey()
        current_state = GameState.init
        InitLevel()
        pass
    #</editor-fold>
    # <editor-fold title='用户输入'>


    for event in pygame.event.get():
        if event.type == QUIT:
            Terminate()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                paddle_move_left = True
            if event.key == K_RIGHT:
                paddle_move_right = True
            if event.key == K_ESCAPE:
                Terminate()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                paddle_move_left = False
            if event.key == K_RIGHT:
                paddle_move_right = False
        if event.type == MOUSEMOTION:
            mPos = event.pos
            mpol=Vector2(mPos[0]-OUT_POSITION[0],-mPos[1]+OUT_POSITION[1]).as_polar()[1]*math.pi/180
            mpol=(mpol%(2*math.pi)+2*math.pi)%(2*math.pi)       #范围为0-2pi
           # print(mpol)
    #</editor-fold>

    #<editor-fold title='游戏主逻辑'>
    #物理

    #球的移动
    ball_pos.x+=vel.x*detalTime
    ball_pos.y+=vel.y*detalTime
    protect_pos+=protect_v*detalTime
    #ball_pos=Vector2(mPos) #debug
    # 玩家的移动
        #按键移动
   # if paddle_move_left:
   #     player_current_v=PLAYER_V*0.5
  #  if paddle_move_right:
    #    player_current_v=-PLAYER_V*0.5

    charp = mpol - player_pos
    #print(charp)
        #追随鼠标
    if charp % (2 * math.pi) > PLAYER_V * detalTime * 2:
        charp = (charp % (2 * math.pi) + 2 * math.pi) % (2 * math.pi)  # 化为0-2pi
        if charp < math.pi:
           # print('1')
            player_current_v = PLAYER_V  * (charp ** 0.5)
        else:
             player_current_v = -PLAYER_V  * ((-charp + 2 * math.pi) ** 0.5)
            # print('2')
    else:
        player_current_v=0
    #print(player_current_v)
    player_pos += player_current_v*detalTime
    #player_pos=0#debug
    #和挡板的碰撞
    #PointCollision(Vector2(OUT_POSITION)+Vector2(math.cos(player_pos-PLAYER_RADIAN/2),-math.sin(player_pos))*(RADIUS_OUT-PLAYER_HEIGHT))
    #PointCollision(Vector2(OUT_POSITION)+Vector2(math.cos(player_pos+PLAYER_RADIAN/2),-math.sin(player_pos))*(RADIUS_OUT-PLAYER_HEIGHT))
    #pygame.draw.circle(screen,COLORS['black'],(int(OUT_POSITION[0]+math.cos(player_pos-PLAYER_RADIAN/2)*(RADIUS_OUT-PLAYER_HEIGHT)),
                                      #       int(OUT_POSITION[1]-math.sin(player_pos-PLAYER_RADIAN/2)*(RADIUS_OUT-PLAYER_HEIGHT))),20,0)#debug
    ball_dian=-(ball_pos-Vector2(OUT_POSITION)).as_polar()[1]*math.pi/180
    temp=math.fabs(ball_dian-player_pos)%(2*math.pi)
    if temp>math.pi:
        temp-=2*math.pi
    if math.fabs(temp)<=PLAYER_RADIAN/2:#如果在玩家角度范围内
        #print('ball:'+str(ball_dian)+',player'+str(player_pos)+'col')
        if OuterCollision(RADIUS_OUT-PLAYER_HEIGHT): #碰撞 方向摩擦力
            theta=(Vector2(OUT_POSITION)-ball_pos).as_polar()
            print('theta',theta)
            theta=-theta[1]
            if player_current_v>0:
                theta-=90
                #print('+')
            else:
                theta+=90
                #print('-')
            print('theta',theta)
            add=Vector2(math.cos(theta),-math.sin(theta))*player_current_v*PLAYER_FRI
            print(add)
            vel+=add
            #print('vel'+str(vel)+',add:'+str(add))
            pass
    else:
    #和墙壁的碰撞
        if OuterCollision(RADIUS_OUT):
            temp=math.fabs(ball_dian - protect_pos) % (2 * math.pi)
            if temp > math.pi:
                temp -= 2 * math.pi
            if  math.fabs(temp)<= PLAYER_PROTECT_RADIAN / 2:  # 如果在保护区范围内碰撞
               # print('life-', player_hp)
                player_hp -= 1
                pass
            pass
    #和敌人的碰撞
    for e in enemys:
        if PointCollision(Vector2(e[0]),e[1]):
            enemys.remove(e)
            score+=1

    #渲染------------------------------------------------------------------------------
        #敌人
    for e in enemys:
        pygame.draw.circle(screen, COLORS[e[2]], e[0], e[1], 0)
        pass
        #保护区
    pygame.draw.arc(screen,COLORS['light_red'],
                    (OUT_POSITION[0]-RADIUS_OUT-10,OUT_POSITION[1]-RADIUS_OUT-10,RADIUS_OUT*2+20,RADIUS_OUT*2+20),
                    protect_pos-PLAYER_PROTECT_RADIAN/2,protect_pos+PLAYER_PROTECT_RADIAN/2,12)
        #玩家挡板
    pygame.draw.arc(screen,COLORS['yellow'],
                    (OUT_POSITION[0]-RADIUS_OUT-10+PLAYER_HEIGHT,OUT_POSITION[1]-RADIUS_OUT-10+PLAYER_HEIGHT,RADIUS_OUT*2+20-PLAYER_HEIGHT*2,RADIUS_OUT*2+20-PLAYER_HEIGHT*2),
                    player_pos-PLAYER_RADIAN/2,player_pos+PLAYER_RADIAN/2,PLAYER_HEIGHT)

        #球
    pygame.draw.circle(screen, COLORS['ball'], (int(ball_pos.x), int(ball_pos.y)), BALL_RADIUS, 0)
        #分数和生命值UI
    DrawText( 'Life:%3s Score:%4s Level:%3s '%(str(player_hp),str(score),str(level)), mousePos,screen,0, 0)
    # </editor-fold>

    #<editor-fold title='更新处理'>
    pygame.display.update()
    clock.tick(FPS)
    detalTime=clock.get_time()*GAME_SPEED/1000 #每帧之间的时间，单位s
    #</editor-fold>



