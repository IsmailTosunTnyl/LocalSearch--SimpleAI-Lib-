# knapsack problem with local search
from simpleai.search import SearchProblem, hill_climbing, hill_climbing_random_restarts, simulated_annealing, genetic
import random
import time
import pandas as pd
from tabulate import tabulate

class LocalSearch(SearchProblem):
    def __init__(self, items, max_weight):
        self.items = items
        self.max_weight = max_weight
        super(LocalSearch, self).__init__(initial_state=None)

    def actions(self, state):
        if state is None:
            return ['add']
        else:
            return ['add', 'remove']

    def result(self, state, action):
        if state is None:
            state = []
        if action == 'add':
            return state + [1]
        elif action == 'remove':
            return state[:-1]

    def value(self, state):
        if state is None:
            return 0
        weight = 0
        value = 0
        for item, selected in zip(self.items, state):
            if selected:
                weight += item[0]
                value += item[1]
        if weight > self.max_weight:
            return 0
        else:
            return value

    def generate_random_state(self):
        state = []
        for item in self.items:
            if random.random() < 0.5:
                state.append(1)
            else:
                state.append(0)
        return state
    

    def crossover(self, state1, state2):
        index = random.randint(1, len(state1) - 1)
        return state1[:index] + state2[index:]
    

    def mutate(self, state):
        index = random.randint(0, len(state) - 1)
        new_state = state[:]
        if new_state[index] == 1:
            new_state[index] = 0
        else:
            new_state[index] = 1
        return new_state


def sampleTestCases():
    weights = [[5, 3, 7, 2],
               [12, 2, 1, 1, 4],
               [24, 10, 10, 7],
               [10, 20, 30],
               [12, 2, 1, 1, 4, 5, 7, 5, 8, 10],
               [24, 10, 10, 7, 2, 8, 6, 5, 9, 12, 20, 18, 13, 5, 4],
               [10, 20, 30]]

    values = [[12, 5, 10, 7],
              [4, 2, 1, 2, 10],
              [24, 18, 18, 10],
              [60, 100, 120],
              [4, 2, 1, 2, 10, 15, 3, 10, 4, 8],
              [50, 10, 25, 30, 20, 25, 40, 15, 12, 22, 35, 45, 55, 100, 60],
              [60, 100, 120]]
    
    max_weights = [12,15,25,50,20,50,50]
    
    # create graphs to compare the results
    with open('TestResults.txt', 'w') as f:
        for i in range(len(weights)):
            items = []
            max_weight = max_weights[i]
            for j in range(len(weights[i])):
                items.append((weights[i][j], values[i][j]))

            df = pd.DataFrame(columns=['Time Taken','Value'],index=['Hill Climbing','Hill Climbing Random Restarts','Simulated Annealing','Genetic'])

            print("\n \n")
            print("****************Sample Test Case****************")
            print("Test Case: ", i+1)
            print("Max Weight: ", max_weight)
            print("Items: ", items)
            print("\n \n")

            problem = LocalSearch(items, max_weight)
            starttime = time.time()
            print('Hill Climbing')
            result = hill_climbing(problem)
            print(result.state)
            print(result.value)
            endtime = time.time() - starttime
            print("Time taken: ", endtime)
            df.loc['Hill Climbing'] = [endtime,result.value]


            starttime = time.time()
            print('Hill Climbing Random Restarts')
            result = hill_climbing_random_restarts(problem, restarts_limit=100)
            print(result.state)
            print(result.value)
            endtime = time.time() - starttime
            print("Time taken: ", endtime)
            df.loc['Hill Climbing Random Restarts'] = [endtime,result.value]

            starttime = time.time()
            print('Simulated Annealing')
            result = simulated_annealing(problem, iterations_limit=1000)
            print(result.state)
            print(result.value)
            endtime = time.time() - starttime
            print("Time taken: ", endtime)
            df.loc['Simulated Annealing'] = [endtime,result.value]

            starttime = time.time()
            print('Genetic')
            result = genetic(problem, iterations_limit=1000,mutation_chance=0.2)
            print(result.state)
            print(result.value)
            endtime = time.time() - starttime
            print("Time taken: ", endtime)
            df.loc['Genetic'] = [endtime,result.value]

            # plot the graphs
            df.plot(kind='bar',y='Time Taken',title='Time Taken for Test Case '+str(i+1),figsize=(20,20)).get_figure().savefig("graphs/"+'Time'+str(i+1)+'.png')
            df.plot(kind='bar',y='Value',title='Value for Test Case '+str(i+1),figsize=(20,20)).get_figure().savefig("graphs/"+'Value'+str(i+1)+'.png')
            print(tabulate(df, headers='keys', tablefmt='psql'))
            # save the results to a file
            f.write("*****************Sample Test Case*****************"+"\n")
            f.write("Case: "+str(i+1)+"\n")
            f.write("Max Weight: "+str(max_weight)+"\n")
            f.write("Items: "+str(items)+"\n")
            f.write(tabulate(df, headers='keys', tablefmt='psql'))
            f.write("\n \n")

if __name__ == '__main__':
    
    #uncomment the following line to run the sample test cases
    #sampleTestCases()
    
    
    # take input from user
    items = []
    max_weight = int(input("Enter the maximum capacity of the knapsack: "))
    n = int(input("Enter the number of items: "))
    for i in range(n):
        weight = int(input("Enter the weight of item " + str(i) + ": "))
        value = int(input("Enter the value of item " + str(i) + ": "))
        items.append((weight, value))
        

    problem = LocalSearch(items, max_weight)
    print('Hill Climbing')
    result = hill_climbing(problem)
    print(result.state)
    print(result.value)
    print('Hill Climbing Random Restarts')
    result = hill_climbing_random_restarts(problem, restarts_limit=100)
    print(result.state)
    print(result.value)
    print('Simulated Annealing')
    result = simulated_annealing(problem, iterations_limit=1000)
    print(result.state)
    print(result.value)
    print('Genetic')
    result = genetic(problem, iterations_limit=1000)
    print(result.state)
    print(result.value)
