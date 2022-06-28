from graphics import *
import sys
import numpy as np
import winsound
from math import inf as infinity
import time
import copy

def drawI(win,x,y,color):
    offset = 4
    line = Line(Point(30*(x)+15,30*y+offset),Point(30*(x)+15,30*(y+1)-offset))
    
    line.setFill(color)
    line.setWidth(5)
    line.draw(win)
    
def bound_box(x,y,x_min,x_max,y_min,y_max):
    cur_x_start = start_from(x,y)[0][0]
    cur_x_end = end_at(x,y)[0][0]
    cur_y_start = start_from(x,y)[1][1]
    cur_y_end = end_at(x,y)[1][1]
   
    if cur_x_start < x_min:
        x_min = cur_x_start
    if cur_x_end > x_max:
        x_max = cur_x_end
        
    if cur_y_start < y_min:
        y_min = cur_y_start
    if cur_y_end > y_max:
        y_max = cur_y_end
    
    return [(x_min,x_max),(y_min,y_max)]

def drawO(board,win, x, y,x_min,x_max,y_min,y_max):
   
    bound = bound_box(x,y,x_min,x_max,y_min,y_max)
    
    board[x][y] = 0
    offset = 5
    center = Point(30*x+15,30*y+15)

    circle = Circle(center,15 - offset)
    circle.setOutline('blue')
    circle.setWidth(5)
    circle.draw(win)
    
    return bound

def drawX(board,win,x,y,x_min,x_max,y_min,y_max):
    
    bound = bound_box(x,y,x_min,x_max,y_min,y_max)
    
    board[x][y] = 1
    offset = 5
    line1 = Line(Point(30*x+offset,30*y+offset),Point(30*(x+1)-offset,30*(y+1)-offset))
    line2 = Line(Point(30*x+offset,30*(y+1)-offset),Point(30*(x+1)-offset,30*y+offset))
    
    line1.setFill('red')
    line2.setFill('red')
    line1.setWidth(5)
    line2.setWidth(5)
    line1.draw(win)
    line2.draw(win)
    
    return bound
    
def drawFin(win,x1,y1,x2,y2,check):
    if check:
        line = Line(Point(x1,y1),Point(x2,y2))
        line.setFill('red')
        line.setWidth(2)
        line.draw(win)

def isGameOver(win,board,check):
    # diagonal \
    i = -20
    j = 20
    while i < 21:
        # x and y is the cordinate that we start to seach \
        # x = 0, 0, 0, ...., 0, 1, 2, 3, ...., 20
        if i < 0:
            x = 0
        else:
            x = i
        # y = 20, 19,18, ...., 0, 0, 0, ...., 0
        if j > 0 :
            y = j
        else:
            y = 0
        
        temp = -2 # suppose the begin value is null
        counter = 1 # to count stone in align
        while(x < 25 and y < 25):
    
            if board[x][y] == temp:
                counter += 1
            elif board[x][y] != -1:
                temp = board[x][y]
                counter = 1
            else:
                temp = -2
                counter = 1
            
            if counter == 5:
                drawFin(win,(x-4)*30+5,(y-4)*30+5,(x+1)*30-5,(y+1)*30-5,check)
                return 1
            
            x += 1
            y += 1
        i += 1
        j -= 1
        
    # diagonal /
    i = 20
    j = -20
    while j < 21:
        # x and y is the cordinate that we start to seach \
        # x = 20, 20, 20, ...., 20, 19, 18, 17, ...., 0
        if i > 0:
            x = 20
        else:
            x = abs(i)
        # y = 20, 19,18, ...., 0, 0, 0, ...., 0
        if j < 0 :
            y = abs(j)
        else:
            y = 0
        
        temp = -2 # suppose the begin value is O
        counter = 1 # to count stone in align
        while(x < 25 and y < 25):
    
            if board[x][y] == temp:
                counter += 1
            elif board[x][y] != -1:
                temp = board[x][y]
                counter = 1
            else:
                temp = -2
                counter = 1
            
            if counter == 5:
                drawFin(win,(x)*30+5,(y+1)*30-5,(x+4+1)*30-5,(y-4)*30+5,check)
                return 1
            
            x -= 1
            y += 1
        i -= 1
        j += 1
     
    # row
    y = 0
    while y < 25:
        temp = -2 # suppose the begin value is O
        counter = 1 # to count stone in align
        x = 0
        while x < 21:
            if board[x][y] == temp:
                counter += 1
            elif board[x][y] != -1:
                temp = board[x][y]
                counter = 1
            else:
                temp = -2
                counter = 1
            
            if counter == 5:
                
                drawFin(win,(x+1)*30-5,y*30+15,(x-4)*30+5,y*30+15,check)
                return 1
            
            x += 1
        y += 1
        
    # col
    # row
    x = 0
    while x < 25:
        temp = -2 # suppose the begin value is O
        counter = 1 # to count stone in align
        y = 0
        while y < 21:
            if board[x][y] == temp:
                counter += 1
            elif board[x][y] != -1:
                temp = board[x][y]
                counter = 1
            else:
                temp = -2
                counter = 1
            
            if counter == 5:
                
                drawFin(win,x*30+15,(y+1)*30-5,x*30+15,(y-4)*30+5,check)
                return 1
            
            y += 1
        x += 1
         
    return 0
    

def row(win,x,y,w,board,player):
    # w is end position
    
    # check if win
    # windwo size 5
    start = x
    end = start + 4
    qualify = 0
    while end < w+1:
        for i in range (start,end+1):
            if board[i][y] == player:
                qualify += 1
            else:
                qualify = 0
                break
        if qualify == 5:
            return (10000,0)
        else:
            qualify = 0
            start += 1
            end += 1
            
    # check green
    # window size 6
    start = x
    end = start + 5
    qualify = 0
    while end < w+1:
        if board[start][y] != -1 or board[end][y] != -1:
            start += 1
            end += 1
            continue
        for i in range (start+1,end):
            if board[i][y] == player:
                qualify += 1
            elif board[i][y] != player and board[i][y] != -1:
                qualify = 0
                break
        if qualify == 4:
            # erase later
            # drawI(win,start,y,'green')
            # drawI(win,end,y,'green')
            return(1000,0)
        else:
            qualify = 0
            start += 1
            end += 1
            
    # check magenta
    # window size 5
    start = x
    end = start + 4
    qualify = 0
    while end < w+1:
        for i in range (start,end+1):
            if board[i][y] == player:
                qualify += 1
            elif board[i][y] != player and board[i][y] != -1:
                qualify = 0
                break
        if qualify == 4:
            # erase later
            for i in range(start,end+1):
                if board[i][y] == -1:
                    # drawI(win,i,y,'magenta')
                    break
            return (1,3)
        else:
            qualify = 0
            start += 1
            end += 1
    
    # check cyan
    # window size is 6
    start = x
    end = start + 5
    qualify = 0
    
    while end < w+1:
        if board[start][y] != -1 or board[end][y] != -1:
            start += 1
            end += 1
            continue
        next_blank = (-1,-1)
        for i in range (start+1,end):
            if board[i][y] == player:
                qualify += 1
            elif board[i][y] != player and board[i][y] != -1:
                qualify = 0
                break
            # erase later
            else:
                if next_blank[0] == -1:
                    next_blank = (i,y)
                else:
                    qualify = 0
                    break

        if qualify == 3:
            # drawI(win,next_blank[0],next_blank[1],'cyan')
            return (2,2)
        elif next_blank[0] != -1:
            start = next_blank[0]
            end = start + 5
        else:
            start += 1
            end += 1
    
    # check yellow
    # window size 5
    
    start = x
    end = start + 4
    qualify = 0
    while end < w+1:
        if board[start][y] != -1 or board[end][y] != -1:
            start += 1
            end += 1
            continue
        next_blank = (-1,-1)
        for i in range (start+1,end):
            if board[i][y] == player:
                qualify += 1
            elif board[i][y] != player and board[i][y] != -1:
                qualify = 0
                break
            # erase later
            else:
                if next_blank[0] == -1:
                    next_blank = (i,y)
                else:
                    qualify = 0
                    break
        if qualify == 2:
            # drawI(win,next_blank[0],next_blank[1],'yellow')
            return(1,0)
        elif next_blank[0] != -1:
            start = next_blank[0]
            end = start + 4
        else:
            start += 1
            end += 1      

    return (0,0)    

def column(win,x,y,w,board,player):   
    # w is end position
    
    # check if win
    # windwo size 5
    start = y
    end = start + 4
    qualify = 0
    while end < w+1:
        for i in range (start,end+1):
            if board[x][i] == player:
                qualify += 1
            else:
                qualify = 0
                break
        if qualify == 5:
            return (10000,0)
        else:
            qualify = 0
            start += 1
            end += 1
            
    # check green
    # window size 6
    start = y
    end = start + 5
    qualify = 0
    while end < w+1:
        if board[x][start] != -1 or board[x][end] != -1:
            start += 1
            end += 1
            continue
        for i in range (start+1,end):
            if board[x][i] == player:
                qualify += 1
            elif board[x][i] != player and board[x][i] != -1:
                qualify = 0
                break
        if qualify == 4:
            # erase later
            # drawI(win,x,start,'green')
            # drawI(win,x,end,'green')
            return(1000,0)
        else:
            qualify = 0
            start += 1
            end += 1
            
    # check magenta
    # window size 5
    start = y
    end = start + 4
    qualify = 0
    while end < w+1:
        for i in range (start,end+1):
            if board[x][i] == player:
                qualify += 1
            elif board[x][i] != player and board[x][i] != -1:
                qualify = 0
                break
        if qualify == 4:
            # erase later
            for i in range(start,end+1):
                if board[x][i] == -1:
                    # drawI(win,x,i,'magenta')
                    break
            return (1,3)
        else:
            qualify = 0
            start += 1
            end += 1
    
    # check cyan
    # window size is 6
    start = y
    end = start + 5
    qualify = 0
    
    while end < w+1:
        if board[x][start] != -1 or board[x][end] != -1:
            start += 1
            end += 1
            continue
        next_blank = (-1,-1)
        for i in range (start+1,end):
            if board[x][i] == player:
                qualify += 1
            elif board[x][i] != player and board[x][i] != -1:
                qualify = 0
                break
            # erase later
            else:
                if next_blank[1] == -1:
                    next_blank = (x,i)
                else:
                    qualify = 0
                    break

        if qualify == 3:
            # drawI(win,next_blank[0],next_blank[1],'cyan')
            return (2,2)
        elif next_blank[1] != -1:
            start = next_blank[1]
            end = start + 5
        else:
            start += 1
            end += 1
    
    # check yellow
    # window size 5
    
    start = y
    end = start + 4
    qualify = 0
    while end < w+1:
        if board[x][start] != -1 or board[x][end] != -1:
            start += 1
            end += 1
            continue
        next_blank = (-1,-1)
        for i in range (start+1,end):
            if board[x][i] == player:
                qualify += 1
            elif board[x][i] != player and board[x][i] != -1:
                qualify = 0
                break
            # erase later
            else:
                if next_blank[0] == -1:
                    next_blank = (x,i)
                else:
                    qualify = 0
                    break
        if qualify == 2:
            # drawI(win,next_blank[0],next_blank[1],'yellow')
            return(1,0)
        elif next_blank[0] != -1:
            start = next_blank[1]
            end = start + 4
        else:
            start += 1
            end += 1  
    
    return (0,0)    

def diag1(win,x,y,w,z,board,player):
    # diagonal \
    # w is end position
    # check if win
    # windwo size 5
    startx = x
    starty = y
    endx = startx + 4
    endy = starty + 4
    qualify = 0
    while endx < w+1 and endy < z+1:
        for i in range (0,5):
            if board[startx+i][starty+i] == player:
                qualify += 1
            else:
                qualify = 0
                break
        if qualify == 5:
            return (10000,0)
        else:
            qualify = 0
            startx += 1
            starty += 1
            endx += 1
            endy += 1
            
    # check green
    # window size 6
    startx = x
    starty = y
    endx = startx + 5
    endy = starty + 5
    qualify = 0
    while endx < w+1 and endy < z+1:
        if board[startx][starty] != -1 or board[endx][endy] != -1:
            startx += 1
            starty += 1
            endx += 1
            endy += 1
            continue
        for i in range (0,6):
            if board[startx+i][starty+i] == player:
                qualify += 1
            elif board[startx+i][starty+i] != player and board[startx+i][starty+i] != -1:
                qualify = 0
                break
        if qualify == 4:
            # erase later
            # drawI(win,startx,starty,'green')
            # drawI(win,endx,endy,'green')
            return(1000,0)
        else:
            qualify = 0
            startx += 1
            starty += 1
            endx += 1
            endy += 1
    
    # check magenta
    # window size 5
    startx = x
    starty = y
    endx = startx + 4
    endy = starty + 4
    qualify = 0
    while endx < w+1 and endy < z+1:
        for i in range (0,5):
            if board[startx+i][starty+i] == player:
                qualify += 1
            elif board[startx+i][starty+i] != player and board[startx+i][starty+i] != -1:
                qualify = 0
                break
        if qualify == 4:
            # erase later
            for i in range(0,5):
                if board[startx+i][starty+i] == -1:
                    # drawI(win,startx+i,starty+i,'magenta')
                    break
            return (1,3)
        else:
            qualify = 0
            startx += 1
            starty += 1
            endx += 1
            endy += 1
    
    # check cyan
    # window size is 6
    startx = x
    starty = y
    endx = startx + 5
    endy = starty + 5
    qualify = 0
    
    while endx < w+1 and endy < z+1:
        if board[startx][starty] != -1 or board[endx][endy] != -1:
            startx += 1
            starty += 1
            endx += 1
            endy += 1
            continue
        next_blank = (-1,-1)
        for i in range (1,5):
            if board[startx+i][starty+i] == player:
                qualify += 1
            elif board[startx+i][starty+i] != player and board[startx+i][starty+i] != -1:
                qualify = 0
                break
            # erase later
            else:
                if next_blank[0] == -1:
                    next_blank = (startx+i,starty+i)
                else:
                    qualify = 0
                    break

        if qualify == 3:
            # drawI(win,next_blank[0],next_blank[1],'cyan')
            return (2,2)
        elif next_blank[0] != -1:
            startx = next_blank[0]
            starty = next_blank[1]
            endx = startx + 5
            endy = starty + 5
        else:
            startx += 1
            starty += 1
            endx += 1
            endy += 1
            
    # check yellow
    # window size 5
    
    startx = x
    starty = y
    endx = startx + 4
    endy = starty + 4
    qualify = 0
    while endx < w+1 and endy <= z+1:
        if board[startx][starty] != -1 or board[endx][endy] != -1:
            startx += 1
            starty += 1
            endx += 1
            endy += 1
            continue
        next_blank = (-1,-1)
        for i in range (1,4):
            if board[startx+i][starty+i] == player:
                qualify += 1
            elif board[startx+i][starty+i] != player and board[startx+i][starty+i] != -1:
                qualify = 0
                break
            # erase later
            else:
                if next_blank[0] == -1:
                    next_blank = (startx+i,starty+i)
                else:
                    qualify = 0
                    break
        if qualify == 2:
            # drawI(win,next_blank[0],next_blank[1],'yellow')
            return(1,0)
        elif next_blank[0] != -1:
            startx = next_blank[0]
            starty = next_blank[1]
            endx = startx + 4
            endy = starty + 4
        else:
            startx += 1
            starty += 1
            endx += 1  
            endy += 1
    
    return (0,0)

def diag2(win,x,y,w,z,board,player):
    # diagonal /
    # w is end position
    # check if win
    # windwo size 5
    startx = x
    starty = y
    endx = startx - 4
    endy = starty + 4
    qualify = 0
   
    while endx > w-1 and endy < z+1:
        for i in range (0,5):
            if board[startx-i][starty+i] == player:
                qualify += 1
            else:
                qualify = 0
                break
        if qualify == 5:
            return (10000,0)
        else:
            qualify = 0
            startx -= 1
            starty += 1
            endx -= 1
            endy += 1
            
    # check green
    # window size 6
    startx = x
    starty = y
    endx = startx - 5
    endy = starty + 5
    qualify = 0
    while endx > w-1 and endy < z+1:
        if board[startx][starty] != -1 or board[endx][endy] != -1:
            startx -= 1
            starty += 1
            endx -= 1
            endy += 1
            continue
        for i in range (0,6):
            if board[startx-i][starty+i] == player:
                qualify += 1
            elif board[startx-i][starty+i] != player and board[startx-i][starty+i] != -1:
                qualify = 0
                break
        if qualify == 4:
            # erase later
            # drawI(win,startx,starty,'green')
            # drawI(win,endx,endy,'green')
            return(1000,0)
        else:
            qualify = 0
            startx -= 1
            starty += 1
            endx -= 1
            endy += 1
    
    # check magenta
    # window size 5
    startx = x
    starty = y
    endx = startx - 4
    endy = starty + 4
    qualify = 0
    while endx > w-1 and endy < z+1:
        for i in range (0,5):
            if board[startx-i][starty+i] == player:
                qualify += 1
            elif board[startx-i][starty+i] != player and board[startx-i][starty+i] != -1:
                qualify = 0
                break
        if qualify == 4:
            # erase later
            for i in range(0,5):
                if board[startx-i][starty+i] == -1:
                    # drawI(win,startx-i,starty+i,'magenta')
                    break
            return (1,3)
        else:
            qualify = 0
            startx -= 1
            starty += 1
            endx -= 1
            endy += 1
    
    # check cyan
    # window size is 6
    startx = x
    starty = y
    endx = startx - 5
    endy = starty + 5
    qualify = 0

    while endx > w-1 and endy < z+1:
        if board[startx][starty] != -1 or board[endx][endy] != -1:
            startx -= 1
            starty += 1
            endx -= 1
            endy += 1
            continue
        next_blank = (-1,-1)
        for i in range (1,5):
            if board[startx-i][starty+i] == player:
                qualify += 1
            elif board[startx-i][starty+i] != player and board[startx-i][starty+i] != -1:
                qualify = 0
                break
            # erase later
            else:
                if next_blank[0] == -1:
                    next_blank = (startx-i,starty+i)
                else:
                    qualify = 0
                    break

        if qualify == 3:
            # drawI(win,next_blank[0],next_blank[1],'cyan')
            return (2,2)
        elif next_blank[0] != -1:
            startx = next_blank[0]
            starty = next_blank[1]
            endx = startx - 5
            endy = starty + 5
        else:
            startx -= 1
            starty += 1
            endx -= 1
            endy += 1
            
    # check yellow
    # window size 5
    
    startx = x
    starty = y
    endx = startx - 4
    endy = starty + 4
    qualify = 0
    while endx > w-1 and endy < z+1:
        if board[startx][starty] != -1 or board[endx][endy] != -1:
            startx -= 1
            starty += 1
            endx -= 1
            endy += 1
            continue
        next_blank = (-1,-1)
        for i in range (1,4):
            if board[startx-i][starty+i] == player:
                qualify += 1
            elif board[startx-i][starty+i] != player and board[startx-i][starty+i] != -1:
                qualify = 0
                break
            # erase later
            else:
                if next_blank[0] == -1:
                    next_blank = (startx-i,starty+i)
                else:
                    qualify = 0
                    break
        if qualify == 2:
            # drawI(win,next_blank[0],next_blank[1],'yellow')
            return(1,0)
        elif next_blank[0] != -1:
            startx = next_blank[0]
            starty = next_blank[1]
            endx = startx - 4
            endy = starty + 4
        else:
            startx -= 1
            starty += 1
            endx -= 1  
            endy += 1
    
    return (0,0)

def start_from(x,y):
    return [(max(x-4,0),y),(x,(max(y-4,0))),(x-min(4,x,y),y-min(4,x,y)),(x+min(4,min(24-x,y)),y-min(4,min(24-x,y)))]
    # the furthest position since start
    #return [(x,0),(0,y),(x-min(x,y),y-min(x,y)),(x+min(24-x,y),y-min(24-x,y))]

def end_at(x,y):
    return [(min(x+4,24),y),(x,min(y+4,24)),(x+min(24-max(x,y),4),y+min(24-max(x,y),4)),(x-min(4,min(x,24-y)),y+min(4,min(x,24-y)))]

def put_score(win,x,y,board,player): 
    # score = 0
    # power = 0
    # for i in range(0,255024):
    score, power = row(win,start_from(x,y)[0][0],start_from(x,y)[0][1],end_at(x,y)[0][0],board,player)
    temp_score, temp_power = column(win,start_from(x,y)[1][0],start_from(x,y)[1][1],end_at(x,y)[1][1],board,player)
    score += temp_score
    power += temp_power
    temp_score, temp_power = diag1(win,start_from(x,y)[2][0],start_from(x,y)[2][1],end_at(x,y)[2][0],end_at(x,y)[2][1],board,player)
    score += temp_score
    power += temp_power
    temp_score, temp_power = diag2(win,start_from(x,y)[3][0],start_from(x,y)[3][1],end_at(x,y)[3][0],end_at(x,y)[3][1],board,player)
    score += temp_score
    power += temp_power
    
    if power>3:
        score += pow(3,power)
    
    return score

def empty_cells(board,bound):
    
    cells = []
    for i in range(bound[0][0],bound[0][1]+1):
        for j in range(bound[1][0],bound[1][1]+1):
            if board[i][j] == -1:
                cells.append((i,j))
    # for i in range(0,25):
    #     for j in range(0,25):
    #         if board[i][j] == -1:
    #             cells.append((i,j))
    
    return cells

def evaluate(win,x,y,board,player):
    temp = board[x][y]
    #print(board)
    score = put_score(win,x,y,board,player)
    board[x][y] = 1-temp
    score += put_score(win,x,y,board,1-player)
    #temp = board[x][y]
    
    return score
 
def minimax(win,board, depth, player,maximizingPlayer,x,y,bound):
    if depth ==0 or isGameOver(win,board,False):
        return 0
    
    if maximizingPlayer:
        maxEval = -infinity
        
    
    return best

# def minimax(win,board, depth, player,x,y,bound):
#     if player == 0:
#         best = [-1, -1, -infinity]
#     else:
#         best = [-1, -1, +infinity]

#     if depth == 0 or isGameOver(win,board,False):
#         score = evaluate(win,x, y,board,player)
#         #print(score)
#         return [-1,-1,score]
    
#     for cell in empty_cells(board,bound):
#         x, y = cell[0], cell[1]
#         board[x][y] = player
#         # get bound
#         score = minimax(win,board, depth - 1, 1-player,x,y,bound)
        
#         board[x][y] = 1-player

#         score[0], score[1] = x, y
        
#         if player == 0:
#             if score[2] > best[2]:
#                 best = score  # max value
#         else:
#             if score[2] < best[2]:
#                 best = score  # min value
                
    
#     return best

def AI_turn(win,board,player,bound):
    ai_score = 0
    max_ai_score = 0
    max_ai_x = 0
    max_ai_y = 0
    human_score = 0
    max_human_score = 0
    max_human_x = 0
    max_human_y = 0
    
    cells = empty_cells(board,bound)
    
    for x in range (0,len(cells)):
        i = cells[x][0]
        j = cells[x][1]
        if board[i][j] == -1:
            board[i][j] = 1-player
            ai_score = put_score(win,i,j,board,1-player) # to maximize ai socre
            # return if AI win
            if ai_score >= 1000:
                bound = drawO(board,win, i, j,bound[0][0],bound[0][1],bound[1][0],bound[1][1])
                return bound
            
            board[i][j] = player # switch to human
            ai_score += put_score(win,i,j,board,player) # to minimize human score
            if ai_score > max_ai_score:
                max_ai_score = ai_score
                max_ai_x = i
                max_ai_y = j
            # board[i][j] = player
            # human_score = put_score(win,i,j,board,player) # to minimize human score
            # board[i][j] = 1-player # switch to human
            # human_score += put_score(win,i,j,board,1-player) # to maximize ai score
            # if human_score > max_human_score:
            #     max_human_score = human_score
            #     max_human_x = i
            #     max_human_y = j
            board[i][j] = -1 # reset to blank
    if max_ai_score > max_human_score:
        bound = drawO(board,win, max_ai_x, max_ai_y,bound[0][0],bound[0][1],bound[1][0],bound[1][1])
    else:
        bound = drawO(board,win, max_human_x, max_human_y,bound[0][0],bound[0][1],bound[1][0],bound[1][1])
      
    return bound

def main():

    global win
    global boxsize
    board = [[-1 for x in range(25)] for y in range(25)]
    width = 750
    height = 750
    squares = 25
    bound = [(24,0),(24,0)] # [(x_min,x_max),(y_min,y_max)]
    win = GraphWin("Gomuku", width, height)
    win.setBackground('white')

    for i in range(squares - 1):
        hline = Line(Point(0, (width/squares) * (i + 1)), Point(width,  (width/squares) * (i + 1)))
        hline.setFill('silver')
        hline.draw(win)
        vline = Line(Point((height/squares) * (i + 1), 0), Point((height/squares) * (i + 1), height))
        vline.setFill('silver')
        vline.draw(win)
        # first is AI turn 
    time.sleep(0.5)
    bound = drawO(board,win, 12, 11,bound[0][0],bound[0][1],bound[1][0],bound[1][1])

    while True:
  
        p1mouse = win.getMouse()
        p1x = p1mouse.getX()
        p1y = p1mouse.getY()
        p1x_accurate = int(p1x/30)
        p1y_accurate = int(p1y/30)
        bound = drawX(board,win, p1x_accurate, p1y_accurate,bound[0][0],bound[0][1],bound[1][0],bound[1][1])
        if isGameOver(win,board,True):
            print("Human Win!")
            time.sleep(2)
            break
        
        # p2mouse = win.getMouse()
        # p2x = p2mouse.getX()
        # p2y = p2mouse.getY()
        # p2x_accurate = int(p2x/30)
        # p2y_accurate = int(p2y/30)
        # drawO(board,win, p2x_accurate, p2y_accurate)
        
        player = 1
        bound = AI_turn(win,board,player,bound)
        if isGameOver(win,board,True):
            print("Computer Win!")
            time.sleep(2)
            break 
        
        # player = 1
        # depth = 1
        # board_clone = copy.deepcopy(board)
        # best = minimax(win,board_clone, depth, player,p1x_accurate,p1y_accurate,bound)
        # print(best)
        # drawO(board,win, best[0],best[1],bound[0][0],bound[0][1],bound[1][0],bound[1][1])
        # if isGameOver(win,board,True):
        #     print("Computer Win!")
        #     time.sleep(2)
        #     break
        # print(put_score(win,p1x_accurate,p1y_accurate,board,1))
        # board_clone = copy.deepcopy(board)
        # pos = minimax(win,board_clone, 1, 1,p1x_accurate,p1y_accurate,bound)
        # drawO(board,win, pos[0],pos[1],bound[0][0],bound[0][1],bound[1][0],bound[1][1])
        # print(pos[0],pos[1])
            
main()