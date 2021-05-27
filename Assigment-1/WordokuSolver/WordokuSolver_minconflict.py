import random
import copy
import math
import time
from tkinter.constants import W
import numpy as np

def Print(worduko):
    for i in range(9):
        for j in range(9):
            print(worduko[i][j], end=' '),
        print('\n')
def count_conflict(worduko,irow,icol):
    # print(worduko)
    # print(irow)
    # print(icol)
    val=worduko[irow][icol]
    conflicts=0
   
    for i in range(len(worduko)):
        if worduko[i][icol] == val and i != irow:
            conflicts=conflicts+1

    for j in range(len(worduko[0])):
        if worduko[irow][j] == val and j != icol:
            conflicts=conflicts+1

    for i in range(3 * (irow // 3), 3 * (irow // 3) + 3):
        for j in range(3 * (icol// 3), 3 * (icol // 3) + 3):
            if val == worduko[i][j] and not (i == irow and j == icol):
                conflicts=conflicts+1
    # print("Count COnflict:"+str(conflicts))
    return conflicts

def get_random_conflicts(worduko,original_wordkudo,random_conflict_value):
    row=0
    col=0
    for row in range(len(worduko)):
            for col in range(len(worduko[row])):
                if(original_wordkudo[row][col]=='*' and count_conflict(worduko,row,col)>0):
                    # print(random_conflict_value)
                    if(random_conflict_value==0):
                        return (row,col)
                    random_conflict_value=random_conflict_value-1
    return (row,col)

def min_conflict(selected_domain,worduko,selected_row,selected_col):
    # print(selected_domain)
    initial_letter=worduko[selected_row][selected_col]
    selected_letter=selected_domain[0]
    worduko[selected_row][selected_col]=selected_letter
    min_conflicts=10000
    for index in range(len(selected_domain)):
        # print("Available:"+str(count_conflict(worduko,selected_row,selected_col))
        letters=selected_domain[index]
        if(letters!=initial_letter):
            worduko[selected_row][selected_col]=letters
            conflicts=count_conflict(worduko,selected_row,selected_col)
            # print("Available choices: "+letters+"   Conflicts: "+str(conflicts))
            if(conflicts<min_conflicts):
                selected_letter=letters
                min_conflicts=conflicts

    
    
    # print(rand_list,min_conflicts)
    # selected_letter=random.choice(rand_list)
    # print("Selected:"+str(selected_letter))
    return selected_letter

def intialize_worduko(worduko,variables):
    for row in range(len(worduko)):
        for col in range(len(worduko[row])):
            if(worduko[row][col]=='*'):
                domain_of_variable=variables[row][col].get_domain()
                worduko[row][col]=random.choice(domain_of_variable)


class Variable ():
    def __init__(self, position, domain):
        self.position = position
        self.domain = domain

    def remove_domain(self, num):
        try:
            self.domain.remove(num)
        except:
            pass

    def Print_object(self):

        print(self.position,end='   ')
        print(self.domain,end=' ')
    def get_domain(self):
        return self.domain

def update_constraints(state, variables):

    for row in range(len(state)):
        for column in range(len(state[row])):
            if state[row][column] == '*':
                continue

            for i in range(len(state)):
                if variables[i][column] == None:
                    continue

                variables[i][column].remove_domain(state[row][column])

            for j in range(len(state[0])):
                if variables[row][j] == None:
                    continue

                variables[row][j].remove_domain(state[row][column])

            for i in range(3 * (row // 3), 3 * (row // 3) + 3):
                for j in range(3 * (column // 3), 3 * (column // 3) + 3):
                    if variables[i][j] == None:
                        continue

                    variables[i][j].remove_domain(state[row][column])


def count_variables(variables):
    count = 0
    for i in range(len(variables)):
        for j in range(len(variables[i])):
            if variables[i][j] != None:
                count += 1

    return count

def Total_conflicts(wordoku):
    conflict=0

    for i in range(len(wordoku)):
        for j in range(len(wordoku[i])):
            conflict=conflict+count_conflict(wordoku,i,j)
    
    return conflict


def select_variable(variables):
    best_variable_position = None
    minimum_domain_values = None

    for i in range(len(variables)):
        for j in range(len(variables[i])):
            if variables[i][j] == None:
                continue

            if minimum_domain_values == None or minimum_domain_values > len(variables[i][j].domain):
                minimum_domain_values = len(variables[i][j].domain)
                best_variable_position = (i, j)

    return best_variable_position


def valid_variables(variables):
    for i in range(len(variables)):
        for j in range(len(variables[i])):
            if variables[i][j] == None:
                continue
            if len(variables[i][j].domain) == 0:
                return False

    return True


def is_valid_state(state, letter_domain):

    # print(letter_domain)
    # print(len(state[0]))
    for row in range(len(state)):
        for column in range(len(state[row])):
            if state[row][column] == '*':
                continue
            # print(state[row][column])
            # print(row)
            # print(column)

            if state[row][column] not in letter_domain:
                return False

            for i in range(len(state)):
                if state[i][column] == state[row][column] and i != row:
                    return False

            for j in range(len(state[0])):
                if state[row][j] == state[row][column] and j != column:
                    return False

            for i in range(3 * (row // 3), 3 * (row // 3) + 3):
                for j in range(3 * (column // 3), 3 * (column // 3) + 3):
                    if state[row][column] == state[i][j] and not (i == row and j == column):
                        return False

    return True




def main():

    # starting the main function
    start_time = time.process_time ()
    for loop in range(int(8e10)):
        # reading the file
        file = open("input5.txt", "r")
        lines = file.readlines()
        file.close()
        worduko = []
        letter_domain = set()
        # adding the wordoku in 2-d vector
        for line in lines:
            row = []
            row = list(line)
            for letter in row:
                if letter != '*' and letter != '\n':
                    letter_domain.add(letter)
            if (row[-1] == '\n'):
                row = row[:-1]
            worduko.append(row)
        # Print(worduko)

        # copying the wordoku
        original_wordkudo=copy.deepcopy(worduko)
        # if not is_valid_state(worduko, letter_domain):
        #     print("NOT POSSIBLE")
        #     return

        # creating the 2-d variable array where variable[i][j] will have Variable object that has domain to that position
        variables = [[None for i in range(len(worduko))]
                    for j in range(len(worduko[0]))]

        for i in range(len(worduko)):
            for j in range(len(worduko[i])):
                if worduko[i][j] == '*':
                    # print(letter_domain)
                    variables[i][j] = (Variable((i, j), list(letter_domain)))


        # slicing down the domains of the variables 
        update_constraints(worduko, variables)
        # for i in range(9):
        #     for j in range(9):
        #         if(worduko[i][j]!='*'):
        #             print(worduko[i][j])

        #         else:
        #             # print(variables[i][j])
        #             variables[i][j].Print_object()
        #         print(" ")
        #     print('\n')


        # initializing the wordoku with some values of their domain
        intialize_worduko(worduko,variables)
        # Print(worduko)
        if(is_valid_state(worduko,letter_domain)==True):
            print("Answer Came")
            Print(worduko)
        # print("\n")
        # Print(original_wordkudo)

        # starting the master loop 
        for ind in range(1500):
            # print("ind",ind)
            total_c=Total_conflicts(worduko)
            # print("Total Conflict:",total_c)
            # Print(worduko)

            # list of total conflicts
            total_conflited_variable=[]
            for row in range(len(worduko)):
                for col in range(len(worduko[row])):
                    if(original_wordkudo[row][col]=='*' and count_conflict(worduko,row,col)>0):
                        total_conflited_variable.append(row*9+col)
            # print("Total Conflicted Variable=",(total_conflited_variable))

            # checking the total number of conflicts
            if(len(total_conflited_variable)==0):
                Print(worduko)
                with open("solution.txt", 'w') as file:
                    file.writelines(''.join(str(j)
                                for j in i) + '\n' for i in worduko)
                print ("Time Taken = ", time.process_time() - start_time)
                return True
            

            random_conflict_value= random.choice(total_conflited_variable)

            # print(total_conflited_variable)
            # print(random_conflict_value)

            
            
            selected_row=random_conflict_value//9
            selected_col=random_conflict_value%9      
            # print(selected_row)
            # print(selected_col)
            selected_domain=variables[selected_row][selected_col].get_domain()
            

            # print(selected_domain)


            # selecting the letter with minimum conflicts
            letter_with_minimum_conflicts=min_conflict(selected_domain,worduko,selected_row,selected_col)
            # print(letter_with_minimum_conflicts)
            
            # adding the letter with minimum conflicts to the wordoku
            worduko[selected_row][selected_col]=letter_with_minimum_conflicts

        # Print(worduko)

        

    return False







    

# if(solution_state == None):
#     Print("Not Possible")
#     return

# Print(solution_state)
# with open("solution.txt", 'w') as file:
#     file.writelines(''.join(str(j)
# 
#                             for j in i) + '\n' for i in solution_state)


answer =main()

if(answer==False):
    print("Could not find answer")
