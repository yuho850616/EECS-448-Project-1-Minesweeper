# import the pygame library, all this learned from
# http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
from workspace.tile import tile
from workspace.executive import executive
from GUI.inputgui import inputGui
from tkinter import *

import pygame

pygame.init()
pygame.display.init()

# definition of colors
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
BLACK = (0, 0, 0)
DARKGREY = (169, 169, 169)

# tile width and height constant
WIDTH = 20
HEIGHT = 20

# margin between tiles
MARGIN = 5

#ask the user for input
"""print("Welcome to Pysweeper!")
print("Input Board Attributes :)")
print("Width = ")
w = input()
print("Height = ")
h = input()
print("Number of Bombs =")
b = input()"""

w=2
h=2
b=1
incorrect = True

try:
    while (incorrect == True):
        screen = Tk()
        inputScreen = inputGui(screen)
        screen.mainloop()
        w = inputScreen.getWidth()
        h = inputScreen.getHeight()
        b = inputScreen.getBombNum()
        if (w >= 2) and (h >= 2) and (b >= 1) and 1 <= ((w*h)-b) <= 1088:
            incorrect = False

except ValueError:
    pass




#calculate the required screen size based on amount of tiles
screen_width = (int(w) * 20) + ((int(w)+1)*5)
screen_height = (int(h) * 20) + ((int(h)+1)*5)

# create the screen surface
size = screen_width, screen_height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pysweeper")
icon = pygame.image.load("MemoryLeakLogo.png")
pygame.display.set_icon(icon)
#create tile grid
board = [[tile() for i in range(int(w))]for j in range(int(h))]

# main draw loop
program_end = False
font = pygame.font.SysFont('Ariel', 22)

# looping multiple rects
row = int(h)
column = int(w)

# game logic grid
grid = [[0] * row for i in range(column)]
bomb = pygame.image.load("bomb.png")
flag = pygame.image.load("flag.png")


#Sets clock rate
clock = pygame.time.Clock()
exe = executive(int(h), int(w), int(b))
exe.run()
gamestate = 0
while not program_end and gamestate == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_end = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(event.button == 1):
                pos = pygame.mouse.get_pos()
                c = pos[0] // (WIDTH + MARGIN)
                r = pos[1] // (HEIGHT + MARGIN)
                if(c >= column):
                    c = column - 1
                if(r >= row):
                    r = row - 1
                print(c, r)
                exe.gameBoard.reveal_tile(c,r)

            elif(event.button == 3):
                pos = pygame.mouse.get_pos()
                c = pos[0] // (WIDTH + MARGIN)
                r = pos[1] // (HEIGHT + MARGIN)
                exe.gameBoard.flag_tile(c,r)
    screen.fill(DARKGREY)


    for i in range(row):
        for j in range(column):
            color = GREY

            if exe.gameBoard.board[j][i].isVisible == False:
                grid[j][i] = pygame.draw.rect(screen, color,
                                              [(MARGIN + WIDTH) * j + MARGIN, (HEIGHT + MARGIN) * i + MARGIN, WIDTH,
                                               HEIGHT])

            if exe.gameBoard.board[j][i].isVisible == True:
                color = WHITE
                grid[j][i] =  pygame.draw.rect(screen, color,
                                              [(MARGIN + WIDTH) * j + MARGIN, (HEIGHT + MARGIN) * i + MARGIN, WIDTH,
                                               HEIGHT])
            if exe.gameBoard.board[j][i].isBomb == True and exe.gameBoard.board[j][i].isVisible == True :
                grid[j][i] = pygame.draw.rect(screen, color,
                                              [(MARGIN + WIDTH) * j + MARGIN, (HEIGHT + MARGIN) * i + MARGIN, WIDTH,
                                               HEIGHT])
                temp = grid[j][i].move(-5, -5)
                screen.blit(bomb, temp)
            if exe.gameBoard.board[j][i].adjBomb >  0 and exe.gameBoard.board[j][i].isVisible == True:
                temp = grid[j][i].move(5,5)
                screen.blit(font.render(str(exe.gameBoard.board[j][i].adjBomb), True, BLACK), (temp))
            if exe.gameBoard.board[j][i].isFlagged == True and exe.gameBoard.board[j][i].isVisible == False:
                screen.blit(flag,grid[j][i])
    gamestate = exe.checkWinLose()

    clock.tick(60)
    pygame.display.flip()
if (gamestate == 2):
            print("YOU LOSE")
elif (gamestate == 1):
            print("YOU WIN")
pygame.quit()
