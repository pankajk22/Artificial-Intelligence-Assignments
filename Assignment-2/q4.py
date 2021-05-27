import random
import numpy as np
import copy


def Probabilty(arr1, arr2):
    prob = 1.0
    for i in range(len(arr1)):
        if(arr1[i] == arr2[i]):
            prob = prob*(3/4)
        else:
            prob = prob*(1/4)

    return prob


transition_matrix = [
    [0.2, 0.8, 0, 0, 0, 0],
    [0.4, 0.2, 0.2, 0, 0, 0],
    [0, 0.27, 0.2, 0.27, 0.27, 0],
    [0, 0, 0.4, 0.2, 0.27, 0],
    [0, 0, 0, 0.8, 0.2, 0],
    [0, 0, 0.8, 0, 0, 0.2]
]


state_variables = [[0, 1, 1, 1], [1, 0, 1, 0], [
    1, 0, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [0, 1, 1, 1]]
num_of_states = len(state_variables)

possible_states = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [
    0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]

init_probabilities = [1/6 for i in range(6)]

# print(init_probabilities)


emission_matrix = []

for state in state_variables:
    row = []
    for s in possible_states:
        prob = Probabilty(state, s)
        row.append(prob)
    emission_matrix.append(row)

# print(emission_matrix)


def convert(list):

    # Converting integer list to string list
    s = [str(i) for i in list]

    # Join list items using join()
    res = str("".join(s))

    return(res)


def viterbi(observations):

    timeSteps = 100
    V = np.zeros((num_of_states, timeSteps))
    prev = np.zeros((num_of_states, timeSteps))
    for i in range(num_of_states):
        V[i, 0] = init_probabilities[i]*emission_matrix[i][observations[0]]
        prev[i, 0] = 0

    for t in range(1, timeSteps):
        for s in range(num_of_states):
            curr_max = V[0][t-1]*transition_matrix[0][s]
            prev_st_max = 0
            for prev_st in range(1, num_of_states):
                trans_prob = V[prev_st][t-1]*transition_matrix[prev_st][s]
                if trans_prob > curr_max:
                    curr_max = trans_prob
                    prev_st_max = prev_st

            max_probb = curr_max*emission_matrix[s][observations[t]]
            V[s][t] = max_probb
            prev[s][t] = prev_st_max

    predicted = []
    max_prob = 0
    max_state = None
    predicted = []
    for st in range(num_of_states):
        if V[st, -1] > max_prob:
            max_prob = V[st, -1]
            max_state = st

    predicted.append(max_state)
    last_state = int(max_state)
    for t in range(timeSteps-2, -1, -1):
        predicted.insert(0, int(prev[last_state][t+1]))
        last_state = int(prev[last_state][t+1])

    return predicted


state_name = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']

r_state = random.choice(state_name)
actual_state = []
observed_values = []

for i in range(100):
    index = state_name.index(r_state)
    actual_value = state_variables[index]
    actual_state.append(index)
    observed_value = copy.deepcopy(actual_value)
    # print('Actual',actual_value)
    for i in range(len(observed_value)):
        if(random.randint(0, 100) <= 25):
            # print("yes")
            if(observed_value[i] == 1):
                # print("1")
                observed_value[i] = 0
            else:
                # print('0')
                observed_value[i] = 1
        # else:
        #     print("No")
    # print('Observed',observed_value)
    num = convert(observed_value)
    # print(num)
    num_ = int(num, 2)
    # print(num_)
    observed_values.append(num_)
    next_state = r_state
    if(random.randint(1, 100) <= 80):
        cummulative_prob = []
        transition_row = transition_matrix[index]
        c_sum = 0
        for p in transition_row:
            c_sum += p
            cummulative_prob.append(c_sum)

        random_prob = random.random()

        for i in range(1, len(cummulative_prob)):
            # print(random_prob,' ',cummulative_prob[i-1],'    ',cummulative_prob[i])
            if(random_prob <= cummulative_prob[i] and random_prob > cummulative_prob[i-1]):
                next_state = state_name[i]
                # print("found")
                break

        r_state = next_state

predicted_states = viterbi(observed_values)
right = 0
wrong = 0
for i in range(10):
    if(actual_state[(i*10)-1] == predicted_states[(i*10)-1]):
        right += 1
    else:
        wrong += 1
    print("Actual State: ", actual_state[(i*10)-1])
    print("Predicted State: ", predicted_states[(i*10)-1])

print("Accuracy :", right/(right+wrong))
