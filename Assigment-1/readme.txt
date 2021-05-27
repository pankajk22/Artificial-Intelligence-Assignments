Read Me:

Q1.
 Required Module :
import sys
import time
import numpy as np
import tkinter as Mazegame
from termcolor import colored
from PIL import ImageTk, Image
from tkinter import ttk, Canvas, Label

For running the bfs change the line 464 to search_algo_dfs(n, maze, start, end)
For running the dfs change the line 464 to search_algo_bfs(n, maze, start, end)
For running the vfs change the line 464 to search_algo_vcs(n, maze, start, end)
For running the A-star change the line 464 to search_algo_a_star(n, maze, start, end)

For running the file write: python lion_in_maze.py

Q2.

Required Module:
import random
import copy
import math
import time
import numpy as np

Default Assumption:
CROSSOVER_PROBABILITY = 0.6
MUTATION_PROBABILITY = 0.01
MAXIMUM_ITERATIONS = 1e9

For running the file write: python GA.py 

Q3.

Required Module:
import random
import copy
import math
import time
from tkinter.constants import W
import numpy as np

For BackTracking: python WordokuSolver_Backtracking.py
For minconflict: python WordokuSolver_minconflict.py

