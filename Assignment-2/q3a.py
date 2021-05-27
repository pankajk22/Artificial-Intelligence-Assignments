import random
import copy
import numpy as np


class wolverine_MDP():
    def __init__(self):
        self.jean_coordinates = [(0, 0), (3, 4)]
        jean_coordinate = random.choice(self.jean_coordinates)
        self.jean_x = jean_coordinate[0]
        self.jean_y = jean_coordinate[1]
        self.wall_x = 2
        self.wall_y = 3
        self.xavier_school_x = 0
        self.xavier_school_y = 4

    def start_state(self):

        self.wolverine_x = random.randint(0, 4)
        while(self.wolverine_x == self.wall_x):
            self.wolverine_x = random.randint(0, 4)

        self.wolverine_y = random.randint(0, 4)
        while(self.wolverine_y == self.wall_y):
            self.wolverine_y = random.randint(0, 4)

        self.magneto_x = random.randint(0, 4)
        while(self.magneto_x == self.wall_x or self.magneto_x == self.xavier_school_x):
            self.magneto_x = random.randint(0, 4)

        self.magneto_y = random.randint(0, 4)
        while(self.magneto_y == self.wall_y or self.magneto_y == self.xavier_school_y):
            self.magneto_y = random.randint(0, 4)

        state = (self.magneto_x, self.magneto_y, self.wolverine_x,
                 self.wolverine_y, self.jean_x, self.jean_y)

        return state

    def Is_End(self, state):

        m_x = state[0]
        m_y = state[1]
        w_x = state[2]
        w_y = state[3]
        j_x = state[4]
        j_y = state[5]

        if(m_x == w_x and w_x == j_x and m_y == w_y and w_y == j_y):
            return True
        elif(w_x == j_x and w_y == j_y):
            return True
        elif(m_x == w_x and m_y == w_y):
            return True
        else:
            return False

    def Reward(self, state):

        m_x = state[0]
        m_y = state[1]
        w_x = state[2]
        w_y = state[3]
        j_x = state[4]
        j_y = state[5]

        if(m_x == w_x and w_x == j_x and m_y == w_y and w_y == j_y):
            return -15
        elif(w_x == j_x and w_y == j_y):
            return 20
        elif(m_x == w_x and m_y == w_y):
            return -20
        else:
            return 0

    def lazy_magneto(self, state):
        result = []

        m_x = state[0]
        m_y = state[1]

        wall_coordinates = (self.wall_x, self.wall_y)
        school_coordinates = (self.xavier_school_x, self.xavier_school_y)
        if(m_x+1 < 5):
            if((m_x+1, m_y) != school_coordinates and (m_x+1, m_y) != wall_coordinates):
                result.append((m_x+1, m_y))
        if(m_y+1 < 5):
            if((m_x, m_y+1) != school_coordinates and (m_x, m_y+1) != wall_coordinates):
                result.append((m_x, m_y+1))
        if(m_x-1 >= 0):
            if((m_x-1, m_y) != school_coordinates and (m_x-1, m_y) != wall_coordinates):
                result.append((m_x-1, m_y))
        if(m_y-1 >= 0):
            if((m_x, m_y-1) != school_coordinates and (m_x, m_y-1) != wall_coordinates):
                result.append((m_x, m_y-1))

        return result
    
    def intelligent_magneto(self,state):
        result = []
        
        m_x = state[0]
        m_y = state[1]
        w_x = state[2]
        w_y = state[3]

        wall_coordinates=(self.wall_x,self.wall_y)
        school_coordinates=(self.xavier_school_x,self.xavier_school_y)
        if(m_x+1<5):
            if((m_x+1,m_y)!=school_coordinates and (m_x+1,m_y)!=wall_coordinates):
                result.append((m_x+1,m_y))
        if(m_y+1<5):
            if((m_x,m_y+1)!=school_coordinates and (m_x,m_y+1)!=wall_coordinates):
                result.append((m_x,m_y+1))
        if(m_x-1>=0):
            if((m_x-1,m_y)!=school_coordinates and (m_x-1,m_y)!=wall_coordinates):
                result.append((m_x-1,m_y))
        if(m_y-1>=0):   
            if((m_x,m_y-1)!=school_coordinates and (m_x,m_y-1)!=wall_coordinates):
                result.append((m_x,m_y-1))

        distance=100000000000
        valid_results=[]
        for valid_actions in result:
            x=valid_actions[0]-w_x
            y=valid_actions[1]-w_y
            dist=(x*x)+(y*y)
            distance=min(dist,distance)
            
        for valid_actions in result:
            x=valid_actions[0]-w_x
            y=valid_actions[1]-w_y
            dist=(x*x)+(y*y)
            if(dist==distance):
                valid_results.append((valid_actions))

        return valid_results


    def wolverine_valid_actions(self, state):

        result = []
        w_x = state[2]
        w_y = state[3]

        if(w_x+1 < 5):
            if((w_x+1, w_y) != (self.wall_x, self.wall_y)):
                result.append((w_x+1, w_y))
        if(w_y+1 < 5):
            if((w_x, w_y+1) != (self.wall_x, self.wall_y)):
                result.append((w_x, w_y+1))
        if(w_x-1 >= 0):
            if((w_x-1, w_y) != (self.wall_x, self.wall_y)):
                result.append((w_x-1, w_y))
        if(w_y-1 >= 0):
            if((w_x, w_y-1) != (self.wall_x, self.wall_y)):
                result.append((w_x, w_y-1))

        return result

    def new_position_for_lazy_magneto(self,state):
        m_x = state[0]
        m_y = state[1]
        j_x = state[4]
        j_y = state[5]

        index=self.jean_coordinates.index((j_x,j_y))
        if(random.randint(1,10)>8):
            if(index==1):
                jean_coordinate=self.jean_coordinates[0]
                j_x=jean_coordinate[0]
                j_y=jean_coordinate[1]
            else:
                jean_coordinate=self.jean_coordinates[1]
                j_x=jean_coordinate[0]
                j_y=jean_coordinate[1]
        
        magneto_next_step=self.lazy_magneto(state)
        if(random.randint(1,100)<=95):
            next_coordinate=random.choice(magneto_next_step)
            m_x=next_coordinate[0]
            m_y=next_coordinate[1]
        
        return (m_x,m_y,j_x,j_y)
    
    def new_position_for_intelligent_magneto(self,state):
        m_x = state[0]
        m_y = state[1]
        j_x = state[4]
        j_y = state[5]

        index=self.jean_coordinates.index((j_x,j_y))
        if(random.randint(1,10)>8):
            if(index==1):
                jean_coordinate=self.jean_coordinates[0]
                j_x=jean_coordinate[0]
                j_y=jean_coordinate[1]
            else:
                jean_coordinate=self.jean_coordinates[1]
                j_x=jean_coordinate[0]
                j_y=jean_coordinate[1]
        
        # magneto_next_step=[]
        magneto_next_step=self.intelligent_magneto(state)
        # moving_prob=0.95/len(actions)
        # for action in actions:
        #     if(action!=(self.wall_x,self.wall_y) and action!=(self.xavier_school_x,self.xavier_school_y)):
        #         magneto_next_step.append(action)
        if(random.randint(1,100)<=95):
            next_coordinate=random.choice(magneto_next_step)
            m_x=next_coordinate[0]
            m_y=next_coordinate[1]
        
        return (m_x,m_y,j_x,j_y)
    

    def allstates(self):
        jean_state = []
        magneto_state = []
        wolverine_state = []

        for pos in self.jean_coordinates:
            jean_state.append(pos)

        for i in range(0, 5):
            for j in range(0, 5):
                if((i, j) != (self.wall_x, self.wall_y) and (i, j) != (self.xavier_school_x, self.xavier_school_y)):
                    magneto_state.append((i, j))

        for i in range(0, 5):
            for j in range(0, 5):
                if((i, j) != (self.wall_x, self.wall_y)):
                    wolverine_state.append((i, j))

        allstates = []
        for j_state in jean_state:
            for m_state in magneto_state:
                for w_state in wolverine_state:

                    next_state = (
                        m_state[0], m_state[1], w_state[0], w_state[1], j_state[0], j_state[1])
                    allstates.append(next_state)
        return allstates

    def next_state_probabilty_reward(self, state, wolverine_action):

        m_x = state[0]
        m_y = state[1]
        w_x = state[2]
        w_y = state[3]
        j_x = state[4]
        j_y = state[5]

        stay_prob = 0.05
        jean_next_step_ = []
        magneto_next_step_ = []
        wolverine_next_step_ = []

        index = self.jean_coordinates.index((j_x, j_y))

        if(index == 1):
            jean_coordinate = self.jean_coordinates[0]
            jean_next_step_.append((jean_coordinate, 0.2))
        else:
            jean_coordinate = self.jean_coordinates[1]
            jean_next_step_.append((jean_coordinate, 0.2))
        jean_next_step_.append(((j_x, j_y), 0.8))

        moving_prob = 0.95
        wolverine_next_step_.append((wolverine_action, moving_prob))
        wolverine_next_step_.append(((w_x, w_y), stay_prob))

        magneto_next_step = self.lazy_magneto(state)
        moving_prob = 0.95/len(magneto_next_step)

        for step in magneto_next_step:
            magneto_next_step_.append((step, moving_prob))

        magneto_next_step_.append(((m_x, m_y), stay_prob))

        result = []

        for w_step in wolverine_next_step_:
            for m_step in magneto_next_step_:
                for j_step in jean_next_step_:

                    next_state = (m_step[0][0], m_step[0][1], w_step[0]
                                  [0], w_step[0][1], j_step[0][0], j_step[0][1])
                    next_state_probability = round(
                        m_step[1]*w_step[1]*j_step[1], 5)
                    reward = self.Reward(next_state)
                    result.append((next_state, next_state_probability, reward))

        # print(round(sum(t[1] for t in result ),3))
        return result


    def next_state_probabilty_reward_for_active_magneto(self, state, wolverine_action):

        m_x = state[0]
        m_y = state[1]
        w_x = state[2]
        w_y = state[3]
        j_x = state[4]
        j_y = state[5]

        stay_prob = 0.05
        jean_next_step_ = []
        magneto_next_step_ = []
        wolverine_next_step_ = []

        index = self.jean_coordinates.index((j_x, j_y))

        if(index == 1):
            jean_coordinate = self.jean_coordinates[0]
            jean_next_step_.append((jean_coordinate, 0.2))
        else:
            jean_coordinate = self.jean_coordinates[1]
            jean_next_step_.append((jean_coordinate, 0.2))
        jean_next_step_.append(((j_x, j_y), 0.8))

        moving_prob = 0.95
        wolverine_next_step_.append((wolverine_action, moving_prob))
        wolverine_next_step_.append(((w_x, w_y), stay_prob))

        magneto_next_step = self.intelligent_magneto(state)
        moving_prob = 0.95/len(magneto_next_step)

        for step in magneto_next_step:
            magneto_next_step_.append((step, moving_prob))

        magneto_next_step_.append(((m_x, m_y), stay_prob))

        result = []

        for w_step in wolverine_next_step_:
            for m_step in magneto_next_step_:
                for j_step in jean_next_step_:

                    next_state = (m_step[0][0], m_step[0][1], w_step[0]
                                  [0], w_step[0][1], j_step[0][0], j_step[0][1])
                    next_state_probability = round(
                        m_step[1]*w_step[1]*j_step[1], 5)
                    reward = self.Reward(next_state)
                    result.append((next_state, next_state_probability, reward))

        # print(round(sum(t[1] for t in result ),3))
        return result


    def Discount(self):
        return 0.85


def valueIteration_for_lazy_magneto(mdp):
    V = {}
    all_states = mdp.allstates()
    for state in all_states:
        V[state] = 0

    def Q(state, action):
        return sum(prob*(reward+(mdp.Discount()*V[newState]))for (newState, prob, reward) in mdp.next_state_probabilty_reward(state, action))

    iterations=1
    while True:
        newV = {}

        for state in all_states:
            if mdp.Is_End(state) == True:
                newV[state] = 0
            else:
                newV[state] = max(Q(state, action)
                                  for action in mdp.wolverine_valid_actions(state))

        iterations+=1
        if max(abs(V[state]-newV[state]) for state in all_states)<0.0001:
            break
            
        V=copy.deepcopy(newV)
    # print(iterations)
    pi={}
    for state in all_states:
        if mdp.Is_End(state)== True:
            pi[state]='End'
        else:
            pi[state]=max((Q(state,action),action) for action in mdp.wolverine_valid_actions(state))[1]

    # for state in all_states:
    #     print(state,'   ',V[state],'    ',pi[state])
    # print((sum(V[state] for state in all_states)/len(all_states)))
    return pi

def valueIteration_for_active_magneto(mdp):
    V = {}
    all_states = mdp.allstates()
    for state in all_states:
        V[state] = 0

    def Q(state, action):
        return sum(prob*(reward+(mdp.Discount()*V[newState]))for (newState, prob, reward) in mdp.next_state_probabilty_reward_for_active_magneto(state, action))

    iterations=1
    while True:
        newV = {}

        for state in all_states:
            if mdp.Is_End(state) == True:
                newV[state] = 0
            else:
                newV[state] = max(Q(state, action)
                                  for action in mdp.wolverine_valid_actions(state))

        iterations+=1
        if max(abs(V[state]-newV[state]) for state in all_states)<0.0001:
            break
            
        V=copy.deepcopy(newV)
    # print(iterations)
    pi={}
    for state in all_states:
        if mdp.Is_End(state)== True:
            pi[state]='End'
        else:
            pi[state]=max((Q(state,action),action) for action in mdp.wolverine_valid_actions(state))[1]

    # for state in all_states:
    #     print(state,'   ',V[state],'    ',pi[state])
    # print((sum(V[state] for state in all_states)/len(all_states)))

    return pi



def make_grid(state,mdp):
    
    grid=[['-' for i in range(5)] for j in range(5)]
    grid[mdp.wall_x][mdp.wall_y]='B'
    grid[mdp.xavier_school_x][mdp.xavier_school_y]='X'
    grid[state[0]][state[1]]='M'
    grid[state[2]][state[3]]='W'
    grid[state[4]][state[5]]='J'

    return grid

def Print(grid):
    for r in grid:
        for c in r:
            print(c,end = " ")
        print()
    print()
    print()

def play_game_for_lazy_magneto(mdp,policy):

    print("--------------------Playing Game for Lazy magneto---------------------")
    wolve=0
    jean=0
    magneto=0

    for i in range(15):
        state=mdp.start_state()
        print('Start State: ')
        grid=make_grid(state,mdp)
        Print(grid)
        if(policy[state]=='End'):

            print('End State: ')
            total_reward=mdp.Reward(state)
            # print(total_reward)
            if(total_reward==20):
                wolve+=1
            elif(total_reward==-20):
                magneto+=1
            elif(total_reward==-15):
                jean+=1
            Print(grid)
        else:
            while(policy[state]!='End'):
                (new_m_x,new_m_y,new_j_x,new_j_y)=mdp.new_position_for_lazy_magneto(state)
                wolverine_next_step=policy[state]
                new_w_x=wolverine_next_step[0]
                new_w_y=wolverine_next_step[1]

                new_state=(new_m_x,new_m_y,new_w_x,new_w_y,new_j_x,new_j_y)
                if(policy[new_state]=='End'):
                    print('End State: ')
                    total_reward=mdp.Reward(new_state)
                    # print(total_reward)

                    if(total_reward==20):
                        wolve+=1
                    elif(total_reward==-20):
                        magneto+=1
                    elif(total_reward==-15):
                        jean+=1
                grid=make_grid(new_state,mdp)
                Print(grid)
                state=copy.deepcopy(new_state)

    print()
    print("Wolverine wins : ",wolve)
    print("magneto Wins : ",magneto)
    print("All on same position : ",jean)

def play_game_for_Active_magneto(mdp,policy):

    print("--------------------Playing Game for Active magneto---------------------")
    wolve=0
    jean=0
    magneto=0

    for i in range(15):
        state=mdp.start_state()
        print('Start State: ')
        grid=make_grid(state,mdp)
        Print(grid)
        if(policy[state]=='End'):

            print('End State: ')
            total_reward=mdp.Reward(state)
            # print(total_reward)
            if(total_reward==20):
                wolve+=1
            elif(total_reward==-20):
                magneto+=1
            elif(total_reward==-15):
                jean+=1
            Print(grid)
        else:
            while(policy[state]!='End'):
                (new_m_x,new_m_y,new_j_x,new_j_y)=mdp.new_position_for_intelligent_magneto(state)
                wolverine_next_step=policy[state]
                new_w_x=wolverine_next_step[0]
                new_w_y=wolverine_next_step[1]

                new_state=(new_m_x,new_m_y,new_w_x,new_w_y,new_j_x,new_j_y)
                if(policy[new_state]=='End'):
                    print('End State: ')
                    total_reward=mdp.Reward(new_state)
                    # print(total_reward)

                    if(total_reward==20):
                        wolve+=1
                    elif(total_reward==-20):
                        magneto+=1
                    elif(total_reward==-15):
                        jean+=1
                grid=make_grid(new_state,mdp)
                Print(grid)
                state=copy.deepcopy(new_state)

    print()
    print("Wolverine wins : ",wolve)
    print("magneto Wins : ",magneto)
    print("All on same position : ",jean)



mdp = wolverine_MDP()
policy=valueIteration_for_lazy_magneto(mdp)
play_game_for_lazy_magneto(mdp,policy)
new_mdp=wolverine_MDP()
policy1=valueIteration_for_active_magneto(new_mdp)
play_game_for_Active_magneto(new_mdp,policy1)

