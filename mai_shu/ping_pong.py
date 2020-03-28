# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 22:14:39 2020

@author: ZCM
"""

import turtle as t

game = t.Screen()
game.title("比目鱼打球")
game.bgcolor('black')
game.setup(800, 600)
game.tracer(0)

# 创建try球拍
ry = t.Turtle()
ry.ht()
ry.up()
ry.color('yellow')
ry.shape('square')
ry.shapesize(5, 1)
ry.goto(-350, 0)
ry.st()

def ry_up():
    print('ww')
    y = ry.ycor()
    y = y + 8
    ry.sety(y)
    
def ry_down():
    print('ss')
    y = ry.ycor()
    y = y - 8
    ry.sety(y)

# 创建zcm球拍
cm = t.Turtle()
cm.ht()
cm.up()
cm.color('white')
cm.shape('square')
cm.shapesize(5, 1)
cm.goto(350, 0)
cm.st()

def cm_up():
    y = cm.ycor()
    y = y + 8
    cm.sety(y)
    
def cm_down():
    y = cm.ycor()
    y = y - 8
    cm.sety(y)
    
# 创建乒乓球
pp = t.Turtle()
pp.up()
pp.speed(0)
pp.color('white')
pp.shape('circle')
pp.st()
pp.dx = 1
pp.dy = 1

player_speed = 10
ry_score = 0
cm_score = 0

def write_score():
    pen.clear()
    score_text = "润钰：{}    楚明: {}".format(ry_score, cm_score)
    pen.write(score_text, align = 'center', font = ('Arial', 20, 'bold'))
    
pen = t.Turtle()
pen.ht()
pen.up()
pen.color('white')
pen.goto(-30, 250)
write_score()

game.listen()
game.onkey(ry_up, 'w')
game.onkey(ry_down, 's')

game.onkey(cm_up, 'Up')
game.onkey(cm_down, 'Down')

while True:
    game.update()
    pp.setx(pp.xcor() + pp.dx)
    pp.sety(pp.ycor() + pp.dy)
    
    if pp.ycor() > 290 or pp.ycor() < -290:
        pp.dy *= -1
        
    if pp.ycor() < cm.ycor() + 50 and pp.ycor() > cm.ycor() - 50 and pp.xcor() >= 330:
        pp.dx *= -1
        pp.setx(329)
        
    if pp.ycor() < ry.ycor() + 50 and pp.ycor() > ry.ycor() - 50 and pp.xcor() <= -330:
        pp.dx *= -1
        pp.setx(-329)
        
    # 球出界
    if pp.xcor() > 350:
        pp.goto(0, 0)
        ry_score += 1
        write_score()
    
    if pp.xcor() < -350:
        pp.goto(0, 0)
        cm_score += 1
        write_score()
                                           
game.mainloop()
