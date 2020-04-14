import turtle
from random import randrange

snake = [[0, 0], [0, 10], [0, 20]]
aim = [0, 10]
food = [-10, 0]

def change_direction(x, y):
    aim[0] = x
    aim[1] = y

def suqare(x, y, size, color):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.color(color)
    turtle.begin_fill()

    for i in range(4):
        turtle.forward(size)
        turtle.left(90)
    turtle.end_fill()

def inside(head):
    return -250 < head[0] < 250 and -250 < head[1] < 250

import copy
def snake_move():
    head = copy.deepcopy(snake[-1])
    head = [head[0] + aim[0], head[1] + aim[1]]
    if head in snake or not inside(head):
        print("game over!")
        suqare(head[0], head[1], 10, 'red')
        return
    if head == food :
        food[0] = randrange(-15, 15) * 10
        food[1] = randrange(-15, 15) * 10
    else :
        snake.pop(0)

    snake.append(head)
    turtle.clear()
    suqare(food[0], food[1], 10, 'yellow')
    for body in snake:
        suqare(body[0], body[1], 10, "purple")
    turtle.update()
    turtle.ontimer(snake_move, 300)

turtle.setup(500, 500)
turtle.tracer(False)
turtle.hideturtle()
turtle.listen()
turtle.onkey(lambda : change_direction(0, 10), 'Up')
turtle.onkey(lambda : change_direction(0, -10), 'Down')
turtle.onkey(lambda : change_direction(-10, 0), 'Left')
turtle.onkey(lambda : change_direction(10, 0), 'Right')
snake_move()
turtle.done()
