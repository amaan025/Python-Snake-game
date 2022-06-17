# Screen res : 1600 * 900
from tkinter import *
import tkinter as tk
import random
import webbrowser
del_snake = []
GameOver = False
gamePause = False

def blocks():
    global wall1
    global wall2
    wall1 = canvas.create_rectangle(400,160,450,600,fill = "#EAEAEA")
    wall2 = canvas.create_rectangle(1150,300,1200,740,fill = "#EAEAEA")

def place_food():
    global food , foodx , foody
    placed_food = False
    food = canvas.create_oval(0,0, snake_size, snake_size, fill = "#AE431E")
    while(placed_food == False):
        placed_food = False
        foodx = random.randint(10,width - snake_size)
        foody = random.randint(10,height - snake_size)
        if (foodx >= 400 and foodx <= 450 and foody >=160 and foody <=600) or (foodx >= 1150 and foodx <= 1200 and foody >= 300 and foody <= 740 ) :
            placed_food = False
        else:
            canvas.move( food, foodx , foody )
            placed_food = True

def leftKey(event):
    global direction
    direction = "left"

def rightKey(event):
    global direction
    direction = "right"

def upKey(event):
    global direction
    direction = "up"

def downKey(event):
    global direction
    direction = "down"

def bossactivate():
    global direction
    direction = "B"

def shrink(event):
    if(len(snake) > 15):
        canvas.delete(snake.pop())

def pause(event):
    global gamePause
    gamePause = True

def resume(event):
    global gamePause
    gamePause = False

def boss_key(event):
    new = 1
    url = "https://www.google.com"
    webbrowser.open(url,new=new)

def window_dimentions(w,h):
    window = Tk()
    window.title("Snake Game")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window

width = 1600
height = 900
window = window_dimentions(width, height)
canvas = Canvas(window, bg = "#FFCC1D", width = width, height = height)
snake = []
snake_size = 15
snake.append(canvas.create_rectangle(snake_size , snake_size , snake_size * 2 , snake_size * 2 , fill="#0B4619" ))
score = 0
txt = "Score : " + str(score)
score_text = canvas.create_text(width/2 , 20 , fill = "black" , font="Times 30 italic bold" , text=txt )
canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<Down>", downKey)
canvas.bind("<S>", shrink)
canvas.bind("<P>", pause)
canvas.bind("<R>", resume)
canvas.bind("<B>", bossactivate)
canvas.focus_set()
direction = "right"

def grow_snake():
    last_element = len(snake)-1
    last_element_pos = canvas.coords(snake[last_element])
    snake.append(canvas.create_rectangle(0,0, snake_size,snake_size, fill="#116530"))
    if (direction == "left"):
        canvas.coords(snake[last_element+1],last_element_pos[0]+snake_size, last_element_pos[1],last_element_pos[2]+snake_size,last_element_pos[3])
    elif (direction == "right"):
        canvas.coords(snake[last_element+1],last_element_pos[0] - snake_size,last_element_pos[1],last_element_pos[2] - snake_size,last_element_pos[3])
    elif (direction == "up"):
        canvas.coords(snake[last_element+1],last_element_pos[0], last_element_pos[1]+snake_size,last_element_pos[2], last_element_pos[3]+snake_size)
    else:
        canvas.coords(snake[last_element+1],last_element_pos[0], last_element_pos[1]-snake_size,last_element_pos[2], last_element_pos[3]-snake_size)
    global score
    score += 10
    txt = "Score: " + str(score)
    canvas.itemconfigure(score_text, text=txt)

def move_food():
    global food, foodx, foody
    canvas.move(food, (foodx*(-1)), (foody*(-1)))
    foodx = random.randint(10,width-snake_size)
    foody = random.randint(10,height-snake_size)
    canvas.move(food, foodx, foody)
def overlapping(a,b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False
def move_snake():
    global canvas
    global GameOver
    global gamePause
    if GameOver:
        return
    if gamePause:
        window.after(90, move_snake)
        return
    canvas.pack()
    pos=[]
    pos.append(canvas.coords(snake[0]))
    if pos[0][0] < 0:
        canvas.coords(snake[0],width,pos[0][1],width-snake_size,pos[0][3])
    elif pos[0][2] > width:
        canvas.coords(snake[0],0-snake_size,pos[0][1],0,pos[0][3])
    elif pos[0][3] > height:
        canvas.coords(snake[0],pos[0][0],0 - snake_size,pos[0][2],0)
    elif pos[0][1] < 0:
        canvas.coords(snake[0],pos[0][0],height ,pos[0][2],height-snake_size)
    pos.clear()
    pos.append(canvas.coords(snake[0]))
    if direction == "left":
        canvas.move(snake[0], -snake_size,0)
    elif direction == "right":
        canvas.move(snake[0], snake_size,0)
    elif direction == "up":
        canvas.move(snake[0], 0,-snake_size)
    elif direction == "down":
        canvas.move(snake[0], 0,snake_size)
    elif direction == "B":
        boss_key()
    s_head_pos = canvas.coords(snake[0])
    food_pos = canvas.coords(food)
    if overlapping(s_head_pos, food_pos):
        move_food()
        grow_snake()
    for i in range(1,len(snake)):
        if overlapping(s_head_pos, canvas.coords(snake[i])):
            GameOver = True
            canvas.create_text(width/2,height/2,fill="black",font="Arial 20 italic bold", text="Game Over!")
    for i in range(wall1):
         if overlapping(s_head_pos, canvas.coords(wall1)):
             GameOver = True
             canvas.create_text(width/2,height/2,fill="black",font="Arial 20 italic bold", text="Game Over!")
    for i in range(wall2):
        if overlapping(s_head_pos, canvas.coords(wall2)):
            GameOver = True
            canvas.create_text(width/2,height/2,fill="black",font="Arial 20 italic bold", text="Game Over!")
    for i in range(1,len(snake)):
        pos.append(canvas.coords(snake[i]))
    for i in range(len(snake)-1):
        canvas.coords(snake[i+1],pos[i][0],pos[i][1],pos[i][2],pos[i][3])
    window.after(90, move_snake)

can=Canvas(window, width=1600,height=900)
can.pack()
can.config(bg="#CEE5D0")
can.create_text(800,100,fill="black",font=("Arial",40,'bold'),text="<------Snake   Game  ------>")
options_text1 = "1) Use arrow keys to move the snake"
options_text2 = "2) Use R to resume and P to pause the game"
options_text3 = "3) Use S as cheat code to shrink, if snake lenght is greater than 15"
options_text4 = "4) Use B key for boss key"
can.create_text(1000, 350, fill = "black", font = ("Arial",25,'bold'), text = "Controls :")
can.create_text(1000,400, fill = "black", font = ("Arial", 20 ), text = options_text1)
can.create_text(1000,450, fill = "black", font = ("Arial", 20 ), text = options_text2)
can.create_text(1000,500, fill = "black", font = ("Arial", 20 ), text = options_text3)
can.create_text(1000,550, fill = "black", font = ("Arial", 20 ), text = options_text4)

def start_game():
    global canvas
    width = 1600
    height = 900
    window = window_dimentions(width, height)
    canvas = Canvas(window, bg = "#FFCC1D", width = width, height = height)
    snake = []
    snake_size = 15
    snake.append(canvas.create_rectangle(snake_size , snake_size , snake_size * 2 , snake_size * 2 , fill="#0B4619" ))
    score = 0
    txt = "Score : " + str(score)
    score_text = canvas.create_text(width/2 , 20 , fill = "black" , font="Times 30 italic bold" , text=txt )
    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.bind("<S>", shrink)
    canvas.bind("<P>", pause)
    canvas.bind("<R>", resume)
    canvas.bind("<B>", boss_key)
    canvas.focus_set()
    direction = "right"
    blocks()
    place_food()
    move_snake()

play = Button(window, text = "Start", command = start_game)
play.place(x=200, y=400)
exit = Button(window, text="exit", command = window.destroy)
exit.place(x=200, y=500)

window.mainloop()
from tkinter import *
import tkinter as tk
import random
import webbrowser
del_snake = []
GameOver = False
gamePause = False
boss = 1


def blocks():
    global wall1
    global wall2
    wall1 = canvas.create_rectangle(400, 160, 450, 600, fill="#EAEAEA")
    wall2 = canvas.create_rectangle(1150, 300, 1200, 740, fill="#EAEAEA")


def place_food():
    global food, foodx, foody
    placed_food = False
    food = canvas.create_oval(0, 0, snake_size, snake_size, fill="#AE431E")
    while(placed_food == False):
        placed_food = False
        foodx = random.randint(10, width - snake_size)
        foody = random.randint(10, height - snake_size)
        if (foodx >= 400 and foodx <= 450 and foody >= 160 and foody <= 600) or (
                foodx >= 1150 and foodx <= 1200 and foody >= 300 and foody <= 740):
            placed_food = False
        else:
            canvas.move(food, foodx, foody)
            placed_food = True


def leftKey(event):
    global direction
    direction = "left"


def rightKey(event):
    global direction
    direction = "right"


def upKey(event):
    global direction
    direction = "up"


def downKey(event):
    global direction
    direction = "down"


def bossactivate():
    global direction
    direction = "B"


def shrink(event):
    if(len(snake) > 15):
        canvas.delete(snake.pop())


def pause(event):
    global gamePause
    gamePause = True


def resume(event):
    global gamePause
    gamePause = False


def boss_key(event):
    new = 1
    url = "https://www.google.com"
    webbrowser.open(url, new=new)


def window_dimentions(w, h):
    window = Tk()
    window.title("Snake Game")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window


width = 1600
height = 900
window = window_dimentions(width, height)
canvas = Canvas(window, bg="#FFCC1D", width=width, height=height)
snake = []
snake_size = 15
snake.append(
    canvas.create_rectangle(
        snake_size,
        snake_size,
        snake_size * 2,
        snake_size * 2,
        fill="#0B4619"))
score = 0
txt = "Score : " + str(score)
score_text = canvas.create_text(
    width / 2,
    20,
    fill="black",
    font="Times 30 italic bold",
    text=txt)
canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<Down>", downKey)
canvas.bind("<S>", shrink)
canvas.bind("<P>", pause)
canvas.bind("<R>", resume)
canvas.bind("<B>", bossactivate)
canvas.focus_set()
direction = "right"


def grow_snake():
    last_element = len(snake) - 1
    last_element_pos = canvas.coords(snake[last_element])
    snake.append(
        canvas.create_rectangle(
            0,
            0,
            snake_size,
            snake_size,
            fill="#116530"))
    if (direction == "left"):
        canvas.coords(snake[last_element + 1],
                      last_element_pos[0] + snake_size,
                      last_element_pos[1],
                      last_element_pos[2] + snake_size,
                      last_element_pos[3])
    elif (direction == "right"):
        canvas.coords(snake[last_element + 1],
                      last_element_pos[0] - snake_size,
                      last_element_pos[1],
                      last_element_pos[2] - snake_size,
                      last_element_pos[3])
    elif (direction == "up"):
        canvas.coords(snake[last_element + 1],
                      last_element_pos[0],
                      last_element_pos[1] + snake_size,
                      last_element_pos[2],
                      last_element_pos[3] + snake_size)
    else:
        canvas.coords(snake[last_element + 1],
                      last_element_pos[0],
                      last_element_pos[1] - snake_size,
                      last_element_pos[2],
                      last_element_pos[3] - snake_size)
    global score
    score += 10
    txt = "Score: " + str(score)
    canvas.itemconfigure(score_text, text=txt)


def move_food():
    global food, foodx, foody
    canvas.move(food, (foodx * (-1)), (foody * (-1)))
    foodx = random.randint(10, width - snake_size)
    foody = random.randint(10, height - snake_size)
    canvas.move(food, foodx, foody)


def overlapping(a, b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False


def move_snake():
    global canvas
    global GameOver
    global gamePause
    if GameOver:
        return
    if gamePause:
        window.after(90, move_snake)
        return
    canvas.pack()
    pos = []
    pos.append(canvas.coords(snake[0]))
    if pos[0][0] < 0:
        canvas.coords(
            snake[0],
            width,
            pos[0][1],
            width -
            snake_size,
            pos[0][3])
    elif pos[0][2] > width:
        canvas.coords(snake[0], 0 - snake_size, pos[0][1], 0, pos[0][3])
    elif pos[0][3] > height:
        canvas.coords(snake[0], pos[0][0], 0 - snake_size, pos[0][2], 0)
    elif pos[0][1] < 0:
        canvas.coords(
            snake[0],
            pos[0][0],
            height,
            pos[0][2],
            height -
            snake_size)
    pos.clear()
    pos.append(canvas.coords(snake[0]))
    if direction == "left":
        canvas.move(snake[0], -snake_size, 0)
    elif direction == "right":
        canvas.move(snake[0], snake_size, 0)
    elif direction == "up":
        canvas.move(snake[0], 0, -snake_size)
    elif direction == "down":
        canvas.move(snake[0], 0, snake_size)
    elif direction == "B":
        boss_key()
    s_head_pos = canvas.coords(snake[0])
    food_pos = canvas.coords(food)
    if overlapping(s_head_pos, food_pos):
        move_food()
        grow_snake()
    for i in range(1, len(snake)):
        if overlapping(s_head_pos, canvas.coords(snake[i])):
            GameOver = True
            canvas.create_text(
                width / 2,
                height / 2,
                fill="black",
                font="Arial 20 italic bold",
                text="Game Over!")
    for i in range(wall1):
        if overlapping(s_head_pos, canvas.coords(wall1)):
            GameOver = True
            canvas.create_text(
                width / 2,
                height / 2,
                fill="black",
                font="Arial 20 italic bold",
                text="Game Over!")
    for i in range(wall2):
        if overlapping(s_head_pos, canvas.coords(wall2)):
            GameOver = True
            canvas.create_text(
                width / 2,
                height / 2,
                fill="black",
                font="Arial 20 italic bold",
                text="Game Over!")
    for i in range(1, len(snake)):
        pos.append(canvas.coords(snake[i]))
    for i in range(len(snake) - 1):
        canvas.coords(snake[i + 1], pos[i][0], pos[i][1], pos[i][2], pos[i][3])
    window.after(90, move_snake)


can = Canvas(window, width=1600, height=900)
can.pack()
can.config(bg="#CEE5D0")
can.create_text(
    800,
    100,
    fill="black",
    font=(
        "Arial",
        40,
        'bold'),
    text="<------Snake   Game  ------>")
options_text1 = "1) Use arrow keys to move the snake"
options_text2 = "2) Use R to resume and P to pause the game"
options_text3 = "3) Use S as cheat code to shrink, if snake lenght is greater than 15"
options_text4 = "4) Use B key for boss key"
can.create_text(
    1000,
    350,
    fill="black",
    font=(
        "Arial",
        25,
        'bold'),
    text="Controls :")
can.create_text(
    1000,
    400,
    fill="black",
    font=(
        "Arial",
        20),
    text=options_text1)
can.create_text(
    1000,
    450,
    fill="black",
    font=(
        "Arial",
        20),
    text=options_text2)
can.create_text(
    1000,
    500,
    fill="black",
    font=(
        "Arial",
        20),
    text=options_text3)
can.create_text(
    1000,
    550,
    fill="black",
    font=(
        "Arial",
        20),
    text=options_text4)


def start_game():
    global canvas
    width = 1600
    height = 900
    window = window_dimentions(width, height)
    canvas = Canvas(window, bg="#FFCC1D", width=width, height=height)
    snake = []
    snake_size = 15
    snake.append(
        canvas.create_rectangle(
            snake_size,
            snake_size,
            snake_size * 2,
            snake_size * 2,
            fill="#0B4619"))
    score = 0
    txt = "Score : " + str(score)
    score_text = canvas.create_text(
        width / 2,
        20,
        fill="black",
        font="Times 30 italic bold",
        text=txt)
    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.bind("<S>", shrink)
    canvas.bind("<P>", pause)
    canvas.bind("<R>", resume)
    canvas.bind("<B>", boss_key)
    canvas.focus_set()
    direction = "right"
    blocks()
    place_food()
    move_snake()


play = Button(window, text="Start", command=start_game)
play.place(x=200, y=400)
exit = Button(window, text="exit", command=window.destroy)
exit.place(x=200, y=500)

window.mainloop()
