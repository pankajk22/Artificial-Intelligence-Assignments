import sys
import time
import numpy as np
import tkinter as Mazegame
from termcolor import colored
from PIL import ImageTk, Image
from tkinter import ttk, Canvas, Label

class PriorityQueue(object): 
    def __init__(self): 
        self.queue = [] 
  
    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 

    def show(self):
        print(self.queue)
    def size(self):
        return(len(self.queue))
    # for checking if the queue is empty 
    def isEmpty(self): 
        return len(self.queue) == 0
  
    # for inserting an element in the queue 
    def insert(self, data): 
        self.queue.append(data) 
  
    # for popping an element based on Priority 
    def delete(self): 
        try: 
            min = 0
            for i in range(len(self.queue)): 
                if self.queue[i][0] < self.queue[min][0]: 
                    min = i 
            item = self.queue[min] 
            del self.queue[min] 
            return item 
        except IndexError: 
            print() 
            exit() 

#This function initializes lion and meat positions
def startend_postion(n):
    start = 0
    end = n*n-1
    return start, end

#This function randomly create walls in maze
def randomize(n):
    limit = np.random.randint(n*n/4,n*n/2)
    checklist = list()

    for i in range(limit):
        hold = np.random.randint(n*n-1)
        chk = 0
        for j in range(len(checklist)):
            if checklist[j] == hold or hold == 0:
                chk = 1
        if chk == 0:
            checklist.append(hold)
    return checklist

#This function prepares full maze layout
def prepare_maze(n, checklist, start, end):
    maze = [[0 for i in range(n)] for j in range(n)]
    for i in range(len(checklist)):
        maze[checklist[i]//n][checklist[i]%n] = 1

    maze[start//n][start%n] = 0
    maze[end//n][end%n] = 0

    return maze

#
def display_maze(n, maze, pos):
    print("")
    for i in range(n):
        for j in range(n):
            if pos == i*n+j:
                print(colored("[8]", "blue"), end="")
            elif maze[i][j] == 0:
                print(colored("[0]", "green"), end="")
            elif maze[i][j] == 1:
                print(colored("[1]", "red"), end="")
            elif maze[i][j] == -1:
                print(colored("[3]", "yellow"), end="")
            elif maze[i][j] == 2:
                print(colored("[3]", "cyan"), end="")
        print("")

def make_screen(n):
    if n in range(2,9):
       size = 300
    elif n in range(9,43):
       size = 640
    elif n in range(43, 75):
       size = 750
    else:
        print("Invalid Maze size")
        sys.exit()

    cell_width = int(size/n)
    cell_height = int(size/n)

    screen = Mazegame.Tk()
    screen.title("Will lion find meat??")
    grid = Canvas(screen, width = cell_width*n, height = cell_height*n, highlightthickness=0)
    grid.pack(side="top", fill="both", expand="true")

    rect = {}
    for col in range(n):
        for row in range(n):
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            rect[row, col] = grid.create_rectangle(x1,y1,x2,y2, fill="red", tags="rect")
    return grid, rect, screen, cell_width

def load_img(size, path, end):
    xcod = end//n
    ycod = end%n
    load = Image.open(path)
    load = load.resize((size, size), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x = ycod*size, y = xcod*size)
    return img

# This function redraws maze and updates the maze according to the traversal at 'delay' time interval
def redraw_maze(grid, rect, screen, n, maze, pos, delay, size, end):
    grid.itemconfig("rect", fill="green")
    path2 = "./meat.png"
    for i in range(n):
        for j in range(n):
            item_id = rect[i,j]
            if pos == i*n+j:
                grid.itemconfig(item_id, fill="blue")
            elif maze[i][j] == 0:                       # positions where lion can move
                grid.itemconfig(item_id, fill="salmon")
            elif maze[i][j] == 1:                       # blocked positions/walls
                grid.itemconfig(item_id, fill="black")
            elif maze[i][j] == -1:                      # positions visited    
                grid.itemconfig(item_id, fill="DeepSkyBlue2")
            elif maze[i][j] == 2:
                grid.itemconfig(item_id, fill="SpringGreen2")

    load_img(size, path2, end)
    screen.update_idletasks()
    screen.update()
    time.sleep(delay)
    return

def button(text, win, window):
    b = ttk.Button(window, text=text, command = win.destroy)
    b.pack()

def popup_win(msg, title, path ,screen):
    popup = Mazegame.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text = msg, font=("Times", 20))
    label.pack(side="top", fill="x", pady=50, padx=50)
    button("Close Maze", screen, popup)
    button("Close popup", popup, popup)
    popup.mainloop()

#This functions check neighbours of current position i.e. current row and col    
def check_pos(row, col, n, maze):
    if row in range(n) and col+1 in range(n) and maze[row][col+1] == 0:
        return 1
    elif row+1 in range(n) and col in range(n) and maze[row+1][col] == 0:
        return 1
    elif row in range(n) and col-1 in range(n) and maze[row][col-1] == 0:
        return 1
    elif row-1 in range(n) and col in range(n) and maze[row-1][col] == 0:
        return 1
    return 0    

# This function will contain all your search algorithms
# maze[row][col] should be used to refer to any position of maze
# pos is the starting position of maze and end is ending position
# pos//n will give row index and pos%n will give col index
# you can use list as stack or any other data structure to traverse the positions of the maze.


def search_algo_dfs(n, maze, start, end):       #dfs
    pos = start  
    delay = 0.1
    grid, rect, screen, wid = make_screen(n)

    memory = 1
    cost=0
    start_time = time.process_time ()
    visited=np.zeros(n*n)
    stack=[pos]
    while True:

        if(len(stack)==0):
            print("Lion cannot reach ")
            break

        print(stack)
        pos=int(stack[-1])
        cost+=3
        stack.pop()
        redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, end)

        # print("pos="+str(pos))
        if(pos==end):
            print("Lion reached!!!")
            break
        visited[pos]
        row=int(pos//n)
        col=int (pos%n)
        
        if(row-1>0 and maze[row-1][col]==0):
            if visited[((row-1)*n)+col] ==0:
                stack.append(((row-1)*n)+col)
                visited[((row-1)*n)+col]=1
                # cost+=3

        if(col-1>0 and maze[row][col-1]==0):
            if visited[((row)*n)+(col-1)]==0:
                stack.append(((row)*n)+(col-1))
                visited[((row)*n)+(col-1)]=1
                # cost+=3
        
        if(row+1<n and maze[row+1][col]==0):
            if visited[((row+1)*n)+col]==0:
                stack.append(((row+1)*n)+col)
                visited[((row+1)*n)+col]=1
                # cost+=3
                
        if(col+1<n and maze[row][col+1]==0):
            if visited[((row)*n)+(col+1)]==0:
                stack.append(((row)*n)+(col+1))
                visited[((row)*n)+(col+1)]=1
                # cost+=3

        if(len(stack)>memory):
            memory=len(stack)
                
        
    print ("Time Taken = ", time.process_time() - start_time)
    print ("Memory Taken By Stack = " + str (memory))   
    print ("Total Cost Taken= "+str(cost))
    popup_win("   ", "   ", "./final.png" , screen)

def search_algo_bfs(n, maze, start, end):       #bfs
    pos = start  
    delay = 0.1
    grid, rect, screen, wid = make_screen(n)

    memory = 1
    cost=0
    start_time = time.process_time ()
    visited=np.zeros(n*n)
    queue=[pos]
    while True:

        if(len(queue)==0):
            print("Lion cannot reach ")
            break

        print(queue)
        pos=queue.pop(0)
        cost+=5
        redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, end)

        # print("pos="+str(pos))
        if(pos==end):
            print("Lion reached!!!")
            break
        visited[pos]
        row=int(pos//n)
        col=int (pos%n)
        
        if(row-1>0 and maze[row-1][col]==0):
            if visited[((row-1)*n)+col] ==0:
                queue.append(((row-1)*n)+col)
                visited[((row-1)*n)+col]=1
                # cost+=5
        if(col-1>0 and maze[row][col-1]==0):
            if visited[((row)*n)+(col-1)]==0:
                queue.append(((row)*n)+(col-1))
                visited[((row)*n)+(col-1)]=1
                # cost+=5
        
        if(row+1<n and maze[row+1][col]==0):
            if visited[((row+1)*n)+col]==0:
                queue.append(((row+1)*n)+col)
                visited[((row+1)*n)+col]=1
                # cost+=5
                
        if(col+1<n and maze[row][col+1]==0):
            if visited[((row)*n)+(col+1)]==0:
                queue.append(((row)*n)+(col+1))
                visited[((row)*n)+(col+1)]=1
                # cost+=5

        if(len(queue)>memory):
            memory=len(queue)
                
        
    print ("Time Taken = ", time.process_time() - start_time)
    print ("Memory Taken By Stack = " + str (memory))   
    print ("Total Cost Taken= "+str(cost))
    popup_win("   ", "   ", "./final.png" , screen)

def search_algo_vcs(n, maze, start, end): 
    pos = start  
    delay = 0.1
    grid, rect, screen, wid = make_screen(n)

    memory = 1
    cost=0
    start_time = time.process_time ()
    visited=np.zeros(n*n)
    p_queue=PriorityQueue()
    p_queue.insert((0,pos))
    while True:

        if(p_queue.size()==0):
            print("Lion cannot reach ")
            break

        p_queue.show()
        (cost,pos)=p_queue.delete()
        redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, end)

        # print("pos="+str(pos))
        if(pos==end):
            print("Lion reached!!!")
            break
        visited[pos]
        row=int(pos//n)
        col=int(pos%n)
        
        if(col+1<n and maze[row][col+1]==0):
            if visited[((row)*n)+(col+1)]==0:
                nextpos=((row)*n)+(col+1)
                p_queue.insert((cost+2,nextpos))
                visited[((row)*n)+(col+1)]=1
                # total_cost+=2

        if(row-1>0 and maze[row-1][col]==0):
            if visited[((row-1)*n)+col] ==0:
                nextpos=((row-1)*n)+col
                p_queue.insert((cost+2,nextpos))
                visited[((row-1)*n)+col]=1
                # total_cost+=2
        if(col-1>0 and maze[row][col-1]==0):
            if visited[((row)*n)+(col-1)]==0:
                nextpos=((row)*n)+(col-1)
                p_queue.insert((cost+2,nextpos))
                visited[((row)*n)+(col-1)]=1
                # total_cost+=2
        
        if(row+1<n and maze[row+1][col]==0):
            if visited[((row+1)*n)+col]==0:
                nextpos=((row+1)*n)+col
                p_queue.insert((cost+3,nextpos))
                visited[((row+1)*n)+col]=1
                # total_cost+=3
                
        

        if(p_queue.size()>memory):
            memory=p_queue.size()
                
        
    print ("Time Taken = ", time.process_time() - start_time)
    print ("Memory Taken By Stack = " + str (memory))   
    print ("Total Cost Taken= "+str(cost))
    popup_win("   ", "   ", "./final.png" , screen)

def manhattan_distance (pos_1, pos_2) :
    return abs (pos_1[0] - pos_2[0]) + abs (pos_1[1] - pos_2[1])

def search_algo_a_star(n, maze, start, end): 
    pos = start  
    delay = 0.1
    grid, rect, screen, wid = make_screen(n)
    pos1=[pos//n,pos%n]
    pos2=[end//n,end%n]
    memory = 1
    cost=0
    start_time = time.process_time ()
    visited=np.zeros(n*n)
    p_queue=PriorityQueue()
    p_queue.insert((0+manhattan_distance(pos1,pos2),pos))
    while True:

        if(p_queue.size()==0):
            print("Lion cannot reach ")
            break

        p_queue.show()
        (cost,pos)=p_queue.delete()
        redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, end)
        
        # print("pos="+str(pos))
        if(pos==end):
            print(str(manhattan_distance([int(pos//n),int(pos%n)],pos2)))
            print("Lion reached!!!")
            break
        visited[pos]
        row=int(pos//n)
        col=int(pos%n)
        pos1=[row,col]
        cost=cost-manhattan_distance(pos1,pos2)
        if(col+1<n and maze[row][col+1]==0):
            if visited[((row)*n)+(col+1)]==0:
                pos1=[row,col+1]
                nextpos=((row)*n)+(col+1)
                p_queue.insert((cost+2+manhattan_distance(pos1,pos2),nextpos))
                visited[((row)*n)+(col+1)]=1
                # total_cost+=2

        if(row-1>0 and maze[row-1][col]==0):
            if visited[((row-1)*n)+col] ==0:
                pos1=[row-1,col]
                nextpos=((row-1)*n)+col
                p_queue.insert((cost+2+manhattan_distance(pos1,pos2),nextpos))
                visited[((row-1)*n)+col]=1
                # total_cost+=2
        if(col-1>0 and maze[row][col-1]==0):
            if visited[((row)*n)+(col-1)]==0:
                pos1=[row,col-1]
                nextpos=((row)*n)+(col-1)
                p_queue.insert((cost+2+manhattan_distance(pos1,pos2),nextpos))
                visited[((row)*n)+(col-1)]=1
                # total_cost+=2
        
        if(row+1<n and maze[row+1][col]==0):
            if visited[((row+1)*n)+col]==0:
                pos1=[row+1,col]
                nextpos=((row+1)*n)+col
                p_queue.insert((cost+3+manhattan_distance(pos1,pos2),nextpos))
                visited[((row+1)*n)+col]=1
                # total_cost+=3
                
        

        if(p_queue.size()>memory):
            memory=p_queue.size()
                
        
    print ("Time Taken = ", time.process_time() - start_time)
    print ("Memory Taken By Stack = " + str (memory))   
    print ("Total Cost Taken= "+str(cost))
    popup_win("   ", "   ", "./final.png" , screen)





if __name__ == "__main__":
    n = 10 # size of maze
    start, end = startend_postion(n)
    randno = randomize(n)
    maze = prepare_maze(n, randno, start, end)
    search_algo_dfs(n, maze, start, end)

