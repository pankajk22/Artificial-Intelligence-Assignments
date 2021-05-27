import random
import copy
import math
import time
import numpy as np

def Print(worduko):
    for i in range(9):
        for j in range(9):
            print(worduko[i][j], end=' '),
        print('\n')


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

        print(self.position)
        print(self.domain)


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


def backtrack(state, variables, letter_domain):
    # Print(state)
    # print("\n")
    if count_variables(variables) == 0:
        return state

    var_postion = select_variable(variables)
    # print(var_postion)
    for value in variables[var_postion[0]][var_postion[1]].domain:
        new_variables = copy.deepcopy(variables)
        new_state = copy.deepcopy(state)

        new_state[var_postion[0]][var_postion[1]] = value
        new_variables[var_postion[0]][var_postion[1]] = None

        update_constraints(new_state, new_variables)

        if valid_variables(new_variables):
            solution_state = backtrack(new_state, new_variables, letter_domain)
            if solution_state is None:
                continue
            elif is_valid_state(solution_state, letter_domain):
                return solution_state


def main():

    file = open("input5.txt", "r")
    lines = file.readlines()
    file.close()
    worduko = []
    letter_domain = set()
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
    if not is_valid_state(worduko, letter_domain):
        print("NOT POSSIBLE")
        return

    variables = [[None for i in range(len(worduko))]
                 for j in range(len(worduko[0]))]

    for i in range(len(worduko)):
        for j in range(len(worduko[i])):
            if worduko[i][j] == '*':
                # print(letter_domain)
                variables[i][j] = (Variable((i, j), list(letter_domain)))

    update_constraints(worduko, variables)
    solution_state = backtrack(worduko, variables, letter_domain)
    if(solution_state == None):
        Print("Not Possible")
        return

    Print(solution_state)
    with open("solution.txt", 'w') as file:
        file.writelines(''.join(str(j)
                                for j in i) + '\n' for i in solution_state)


main()
