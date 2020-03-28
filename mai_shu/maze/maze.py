# 创建游戏背景
import turtle as t
import random as r

mz = t.Screen()
mz.setup(700, 700)
mz.bgcolor("black")
mz.title("尼莫迷宫")
mz.register_shape('wall.gif')
mz.register_shape('e.gif')
mz.register_shape('gold.gif')
mz.register_shape('pl.gif')
mz.register_shape('pr.gif')
mz.tracer(0)

levels = []
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXX   XXXXXX  XXXXXXXXXXX",
    "XXXP XXXXXXX  XXXXXXXXXXX",
    "XXX  XXXXXXX  XXXXXXXXXXX",
    "XXX                  XXXX",
    "XXXXXXX XXXX  XXXXX  XXXX",
    "XXXXXXXGXXXX  XXXXXE  EXX",
    "XXXXXXXXXXXX  XXXXX   XXX",
    "XXXXXXXXXXXX  XXXXX    XX",
    "XX                     XX",
    "XXXX  XXXXXX  XXXX  GXXXX",
    "XXXX  XXXXXX  XXXXXXXXXXX",
    "XXXXE            XXXXXXXX",
    "XXXXXXXXXXEXXXX  XXXXXXXX",
    "XXXXXXXXXXXXXXX  XXXXXXXX",
    "XXXXGXXXXXXXXXX  XXEXXXXX",
    "XX               XXXXXXXX",
    "XX   XXXXXXXXXXXXXXXXXXXX",
    "XX   XXXXX              X",
    "XX   XXXXXXXXXXXXX  XXXXX",
    "XX     XXXXXXXXXXX  XXXXX",
    "XX            XXXX      X",
    "XXXX                    X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ]
levels.append(level_1)

class Gold(t.Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.shape('gold.gif')
        self.speed(0)
        self.penup()
        
class Devil(t.Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.shape('e.gif')
        self.speed(0)
        self.penup()
    
    def move(self):
        self.turn()
        if self.fx == 'U':
            go_x = self.xcor()
            go_y = self.ycor() + 24
        elif self.fx == 'D':
            go_x = self.xcor()
            go_y = self.ycor() - 24
        elif self.fx == 'R':
            go_x = self.xcor() + 24
            go_y = self.ycor()
        elif self.fx == 'L':
            go_x = self.xcor() - 24
            go_y = self.ycor()
        
        if go_x > -288 and go_x < 288 and go_y < 288 and go_y > -288:
            self.goto(go_x, go_y)
        t.ontimer(self.move, r.randint(100, 300))
        
    def turn(self):
        # 实现跟随功能
        if self.distance(player) < 96:
            if self.xcor() < player.xcor():
                self.fx = 'R'
            elif self.xcor() > player.xcor():
                self.fx = 'L'
            elif self.ycor() < player.ycor():
                self.fx = 'U'
            elif self.ycor() > player.ycor():
                self.fx = 'D'
        else:
            self.fx = r.choice(['U', 'D', 'R', 'L'])

class Player(t.Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.shape('pr.gif')
        self.speed(0)
        self.penup()
    
    def go_right(self):
        self.shape('pr.gif')
        go_x = self.xcor() + 24
        go_y = self.ycor()
        self.move(go_x, go_y)
        
    def go_left(self):
        self.shape('pl.gif')
        go_x = self.xcor() - 24
        go_y = self.ycor()
        self.move(go_x, go_y)
        
    def go_up(self):
        go_x = self.xcor()
        go_y = self.ycor() + 24
        self.move(go_x, go_y)
        
    def go_down(self):
        go_x = self.xcor()
        go_y = self.ycor() - 24
        self.move(go_x, go_y)
        
    def move(self, go_x, go_y):
        if (go_x, go_y) not in walls:
            self.goto(go_x, go_y)
            self.look_for_gold(go_x, go_y)
            
    def look_for_gold(self, go_x, go_y):
        global score
        for g in golds:
            if g.distance(player) == 0:
                score += 1
                g.ht()
                golds.remove(g)

class Pen(t.Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.shape('wall.gif')
        self.speed(0)
        self.penup()
    
    def make_maze(self, level):
        for i in range(len(level)):
            row = level[i]
            for j in range(len(row)):
                screen_x = -288 + 24 * j
                screen_y = 288 - 24 * i
                if row[j] == 'X':
                    self.goto(screen_x, screen_y)
                    self.stamp()
                    walls.append((screen_x, screen_y))
                elif row[j] == 'P':
                    player.goto(screen_x, screen_y)
                    player.st()
                elif row[j] == 'G':
                    gold = Gold()
                    golds.append(gold)
                    gold.goto(screen_x, screen_y)
                    gold.st()
                elif row[j] == 'E':
                    e = Devil()
                    devils.append(e)
                    e.goto(screen_x, screen_y)
                    e.st()

# 得分
score = 0
pen = Pen()
player = Player()
walls = []
golds = []
devils = []
pen.make_maze(level_1)

mz.listen()
mz.onkey(player.go_right, 'Right')
mz.onkey(player.go_left, 'Left')
mz.onkey(player.go_up, 'Up')
mz.onkey(player.go_down, 'Down')

for e in devils:
    t.ontimer(e.move, r.randint(100, 300))

while True:
    mz.update()
    
mz.mainloop()