import random
import copy
import math
import time
import numpy as np
from matplotlib import pyplot as plt

# POPULATION_SIZE = 100
CROSSOVER_PROBABILITY = 0.4
MUTATION_PROBABILITY = 0.2
MAXIMUM_ITERATIONS = 1e9
best_fitness=[]

#this function calculates number of attacking pairs
def fitness(individual):
    clashes=0
    # print(individual)
    clashes=clashes+ abs(len(individual))-len(np.unique(individual))
    diagonal_clashes=0
    for row in range(len(individual)):
        for col in range(len(individual)):
            if row != col:
                if(abs(row-col)==abs(individual[row]-individual[col])):
                    diagonal_clashes=diagonal_clashes+1
    clashes=clashes+ diagonal_clashes//2
    # print(clashes)
    return clashes


    

def crossover(individual1, individual2):
    # print(str(len(individual1)))
    if(individual1==individual2):
        individual2=generate_individual(len(individual1))
        return (individual1,individual2)
    cut = random.randint(2,5)
    individual1 = individual1[:cut] + individual2[cut:]
    individual2 = individual2[:cut] + individual1[cut:]

    return (individual1,individual2)



def mutation(individual):
    index = random.randint (0, len (individual) - 1)
    individual[index] = random.randint (1, len(individual))

    return individual
    

def generate_individual(n):
    result = list(range(1, n + 1))
    np.random.shuffle(result)
    return result

class Genetic(object):

    def __init__(self, n ,pop_size):
        #initializing a random individuals with size of initial population entered by user
        self.n=n
        self.queens = []
        for i in range(pop_size):
            self.queens.append(generate_individual(n))

    #generating individuals for a single iteration of algorithm
    def generate_population(self, random_selections=5):
        candid_parents = []
        candid_fitness = []
        #getting individuals from queens randomly for an iteration
        for i in range(random_selections-1):
            candid_parents.append(self.queens[random.randint(0, len(self.queens) - 1)])
            candid_fitness.append(fitness(candid_parents[i]))
        
        sorted_fitness = copy.deepcopy(candid_fitness)
        #sort the fitnesses of individuals

        sorted_fitness=np.argsort(np.array(candid_fitness))

        # print(candid_parents)
        # print(sorted_fitness)
        #getting 2 first individuals(min attackings)
        index1=sorted_fitness[0]
        parent1=candid_parents[index1]
        
        index2=sorted_fitness[1]
        parent2=candid_parents[index2]



        # print("Parent-1: "+str(parent1))
        # print("Parent-2: "+str(parent2))
        # print("Fitness of Parent-1: "+str(fitness(parent1)))
        # print("Fitness of Parent-2: "+str(fitness(parent2)))
        
        #crossover the two parents
        child1=[]
        child2=[]
        if(random.randint (0, 10000)) / 10000.0 <= CROSSOVER_PROBABILITY :
            (child1,child2)=crossover(parent1,parent2)

        # mutation
        if(len(child1)==self.n and len(child2)==self.n):
            if(random.randint(0,10000))/10000.0 <=MUTATION_PROBABILITY and len(child1)==8 and len(child2)==8:
                child1=mutation(child1)
                child2=mutation(child2)
            

            # print("Child-1: "+str(child1))
            # print("Child-2: "+str(child2))
            # print("Fitness of Child-1: "+str(fitness(child1)))
            # print("Fitness of Child-1: "+str(fitness(child2)))
        
            #in code below check if each child is better than each one of queens individuals, set that individual the new child
            
            
            # print("Adding child-1 in population")
            self.queens.append(child1)
            
            # print("Adding child-2 in population")
            self.queens.append(child2)

            queens_fitness=[]
            for queen in self.queens:
                queens_fitness.append(fitness(queen))

            fitness_index=np.argsort(np.array(queens_fitness))
            self.queens.pop(fitness_index[len(fitness_index)-1])
            queens_fitness.pop(fitness_index[len(fitness_index)-1])

            fitness_index=np.argsort(np.array(queens_fitness))
            self.queens.pop(fitness_index[len(fitness_index)-1])
            queens_fitness.pop(fitness_index[len(fitness_index)-1])
            
            

        

    def finished(self):
        best_fit=1000
        global best_fitness
        for i in self.queens:
            #we check if for each queen there is no attacking(cause this algorithm should work for n queen,
            # it was easier to use attacking pairs for fitness instead of non-attacking)
            x=fitness(i)
            best_fit=min(best_fit,x)
            if(fitness(i)==0):
                best_fitness.append(best_fit)
                return [True,i]
        best_fitness.append(best_fit)
        return [False,self.queens[0]]
            

    def start(self, random_selections=5):
        #generate new population and start algorithm until number of attacking pairs is zero
        iterations=0
        start_time = time.process_time ()
        while self.finished()[0]==False and iterations<MAXIMUM_ITERATIONS:
            self.generate_population(random_selections)
            iterations=iterations+1
        final_state = self.finished()
        print(('Solution : ' + str(final_state[1])))
        print("Number of Queens: ",n)
        print("Iterations :"+str(iterations))
        print("Time Taken = ", time.process_time() - start_time)
        print("CrossOver Probability: ",CROSSOVER_PROBABILITY)
        print("Mutation Probability: ", MUTATION_PROBABILITY)


# ******************** N-Queen Problem With GA Algorithm ***********************

# n=(int)(input('Enter the value of N -'))
initial_population=(int)(input('Enter initial population size -'))

legend_list=[]
for n in range(5,10):

    algorithm = Genetic(n=n,pop_size=initial_population)
    algorithm.start()
    plt.plot(best_fitness)
    legend_list.append('Value of N is '+str(n))
    best_fitness=[]
plt.legend(legend_list)
plt.show()
