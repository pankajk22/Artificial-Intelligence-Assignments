import numpy as np
import random
import tkinter as Mazegame
from termcolor import colored
from PIL import ImageTk, Image
from tkinter import ttk, Canvas, Label
import sys
import time
from tqdm import tqdm

# np.random.seed(0)
maxint=100000000000

def distance(x1,y1,x2,y2):
    x=x2-x1
    y=y2-y1
    return ((x*x)+(y*y))


def cavemanAlgo(caveman_x,caveman_y,sheep_x,sheep_y,size):
    distance=maxint
    move='right'

    if(caveman_y<size-1):
        x=(sheep_x-caveman_x)
        y=(sheep_y-(caveman_y+1))
        caveman_right=((x*x)+(y*y))
        # print("Right move: ",caveman_right)
        if(distance>caveman_right):
            distance=caveman_right
            move='right'

    if(caveman_y>0):
        x=(sheep_x-caveman_x)
        y=(sheep_y-(caveman_y-1))
        caveman_left=((x*x)+(y*y))
        # print("Left Move: ",caveman_left)
        if(distance>caveman_left):
            distance=caveman_left
            move='left'

    if(caveman_x<size-1):
        x=(sheep_x-(caveman_x+1))
        y=(sheep_y-caveman_y)
        caveman_down=((x*x)+(y*y))
        # print("Down Move: ",caveman_down)
        if(distance>caveman_down):
            distance=caveman_down
            move='down'
        
    if(caveman_x>0):
        x=(sheep_x-(caveman_x-1))
        y=(sheep_y-caveman_y)
        caveman_up=((x*x)+(y*y))
        # print("Up Move: ",caveman_up)
        if(distance>caveman_up):
            distance=caveman_up
            move='up'
        
    

    
        
    
        
    
    # print(move)
    if(move=='down'):
        return(caveman_x+1,caveman_y)
    if(move=='up'):
        return(caveman_x-1,caveman_y)
    if(move=='right'):
        return(caveman_x,caveman_y+1)
    if(move=='left'):
        return(caveman_x,caveman_y-1)


def sheepAlgo(caveman1_x,caveman1_y,caveman2_x,caveman2_y,sheep_x,sheep_y,size,radius):
    x1=(sheep_x-caveman1_x)
    x2=(sheep_x-caveman2_x)
    y1=(sheep_y-caveman1_y)
    y2=(sheep_y-caveman2_y)

    if((((x1*x1)+(y1*y1))>(radius*radius)) and (((x2*x2)+(y2*y2))>(radius*radius))):
        return (sheep_x,sheep_y)
        
    sum_of_distances=0


    new_sheep_x=sheep_x
    new_sheep_y=sheep_y

    for d in range(1,3):
        if(sheep_x+d<size and sheep_y+d<size):

            distance_to_nearest_corner=distance(sheep_x+d,sheep_y+d,0,size-1)
            if(distance(sheep_x+d,sheep_y+d,size-1,0)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x+d,sheep_y+d,size-1,0)
            if(distance(sheep_x+d,sheep_y+d,0,0)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x+d,sheep_y+d,0,0)
            if(distance(sheep_x+d,sheep_y+d,size-1,size-1)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x+d,sheep_y+d,size-1,size-1)

            distance_to_caveman1=distance(sheep_x+d,sheep_y+d,caveman1_x,caveman1_y)
            distance_to_caveman2=distance(sheep_x+d,sheep_y+d,caveman2_x,caveman2_y)

            right_move=distance_to_caveman1+distance_to_caveman2+distance_to_nearest_corner
            if(sum_of_distances<right_move):
                sum_of_distances=right_move
                new_sheep_x=sheep_x+d
                new_sheep_y=sheep_y+d


        if(sheep_x-d>=0 and sheep_y-d>=0):

            distance_to_nearest_corner=distance(sheep_x-d,sheep_y-d,0,size-1)
            if(distance(sheep_x-d,sheep_y-d,size-1,0)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x-d,sheep_y-d,size-1,0)
            if(distance(sheep_x-d,sheep_y-d,0,0)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x-d,sheep_y-d,0,0)
            if(distance(sheep_x-d,sheep_y-d,size-1,size-1)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x-d,sheep_y-d,size-1,size-1)

            distance_to_caveman1=distance(sheep_x-d,sheep_y-d,caveman1_x,caveman1_y)
            distance_to_caveman2=distance(sheep_x-d,sheep_y-d,caveman2_x,caveman2_y)

            dist=distance_to_caveman1+distance_to_caveman2+distance_to_nearest_corner
            if(sum_of_distances<dist):
                sum_of_distances=dist
                new_sheep_x=sheep_x-d
                new_sheep_y=sheep_y-d


        if(sheep_x+d<size and sheep_y-d>=0):

            distance_to_nearest_corner=distance(sheep_x+d,sheep_y-d,0,size-1)
            if(distance(sheep_x+d,sheep_y-d,size-1,0)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x+d,sheep_y-d,size-1,0)
            if(distance(sheep_x+d,sheep_y-d,0,0)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x+d,sheep_y-d,0,0)
            if(distance(sheep_x+d,sheep_y-d,size-1,size-1)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x+d,sheep_y-d,size-1,size-1)

            distance_to_caveman1=distance(sheep_x+d,sheep_y-d,caveman1_x,caveman1_y)
            distance_to_caveman2=distance(sheep_x+d,sheep_y-d,caveman2_x,caveman2_y)

            dist=distance_to_caveman1+distance_to_caveman2+distance_to_nearest_corner
            if(sum_of_distances<dist):
                sum_of_distances=dist
                new_sheep_x=sheep_x+d
                new_sheep_y=sheep_y-d
        
        
        if(sheep_x-d>=0 and sheep_y+d<size):

            distance_to_nearest_corner=distance(sheep_x-d,sheep_y+d,0,size-1)
            if(distance(sheep_x-d,sheep_y+d,size-1,0)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x-d,sheep_y+d,size-1,0)
            if(distance(sheep_x-d,sheep_y+d,0,0)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x-d,sheep_y+d,0,0)
            if(distance(sheep_x-d,sheep_y+d,size-1,size-1)<distance_to_nearest_corner):
                distance_to_nearest_corner=distance(sheep_x-d,sheep_y+d,size-1,size-1)

            distance_to_caveman1=distance(sheep_x-d,sheep_y+d,caveman1_x,caveman1_y)
            distance_to_caveman2=distance(sheep_x-d,sheep_y+d,caveman2_x,caveman2_y)

            dist=distance_to_caveman1+distance_to_caveman2+distance_to_nearest_corner
            if(sum_of_distances<dist):
                sum_of_distances=dist
                new_sheep_x=sheep_x-d
                new_sheep_y=sheep_y+d
        

    return (new_sheep_x,new_sheep_y)

def Print(grid):
    for r in grid:
        for c in r:
            print(c,end = " ")
        print()





def main():

    sheep=0
    caveman=0
    for i in tqdm(range(0,1000)):
        size=8
        radius=2
        caveman1_x=random.randint(0,size-1)
        caveman1_y=random.randint(0,size-1)
        caveman2_x=random.randint(0,size-1)
        caveman2_y=random.randint(0,size-1)
        sheep_x=random.randint(0,size-1)
        sheep_y=random.randint(0,size-1)
        while((caveman1_x,caveman1_y)==(caveman2_x,caveman2_y) and (caveman2_x,caveman2_y==(sheep_x,sheep_y)) and (sheep_x,sheep_y)==(caveman1_x,caveman1_y)):
            caveman1_x=random.randint(0,size-1)
            caveman1_y=random.randint(0,size-1)
            caveman2_x=random.randint(0,size-1)
            caveman2_y=random.randint(0,size-1)
            sheep_x=random.randint(0,size-1)
            sheep_y=random.randint(0,size-1)
        i =0

        # caveman1_x=7
        # caveman1_y=0
        # caveman2_x=2
        # caveman2_y=3
        # sheep_x=6
        # sheep_y=7
        captured=0
        for i in range(0,100):
            # print("caveman-1 : ("+str(caveman1_x)+' , '+str(caveman1_y)+')')
            # print("caveman-2 : ("+str(caveman2_x)+' , '+str(caveman2_y)+')')
            # print("Sheep : ("+str(sheep_x)+' , '+str(sheep_y)+')')
            grid=[[0 for i in range(size)] for j in range(size)]
            
            grid[caveman1_x][caveman1_y]=1
            grid[caveman2_x][caveman2_y]=2
            grid[sheep_x][sheep_y]=3
            
            
            # Print(grid)
            
            if(distance(caveman1_x,caveman1_y,sheep_x,sheep_y)==1 or distance(caveman2_x,caveman2_y,sheep_x,sheep_y)==1):
                # print("Caveman captured the sheep in ",i," move")
                caveman+=1
                captured=1
                break
            else:
                (new_caveman1_x,new_caveman1_y)=cavemanAlgo(caveman1_x,caveman1_y,sheep_x,sheep_y,size)
                (new_caveman2_x,new_caveman2_y)=cavemanAlgo(caveman2_x,caveman2_y,sheep_x,sheep_y,size)
                if((new_caveman2_x,new_caveman2_y)==(new_caveman1_x,new_caveman1_y)):
                    (new_caveman2_x,new_caveman2_y)=(caveman2_x,caveman2_y)
                (new_sheep_x,new_sheep_y)=sheepAlgo(caveman1_x,caveman1_y,caveman2_x,caveman2_y,sheep_x,sheep_y,size,radius)

                # updating the variables
                caveman1_x=new_caveman1_x
                caveman1_y=new_caveman1_y
                caveman2_x=new_caveman2_x
                caveman2_y=new_caveman2_y
                sheep_x=new_sheep_x
                sheep_y=new_sheep_y
            # print('-----------------------------------------------------------------')
        if(captured==0):
            sheep+=1
        # print("Iterations : ",i+1)
        # print("Caveman couldn't captured sheep")
    print("Caveman Captured Sheep : ",caveman,' in 1000 times')
    print("Caveman couldn't captured sheep : ",sheep,' in 1000 times')
         

main()
        
    