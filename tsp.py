import random
import numpy as np
import math
from numba import jit
import time


# constants :
DIMENSION = 48
POPULATION_SIZE = 10000
file_name = "48cities"
MUTATION_RATE = 0.8


def get_distance_matrix(n):
    tsp_data = open(f"F:\PycharmProjects\pythonProject1\\travelling salesman\main\\{file_name}.txt","r")
    tsp_data = tsp_data.readlines()
    lines = []

    for line in tsp_data:
        data = [line.split(" ")[2],line.split(" ")[3]]
        #print(data)
        lines.append(data)

    for data in lines:
        data[1] = data[1][:-1]

    distance = np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            #print(i," ",j)
            distance[i][j] = round(math.sqrt((float(lines[i][0]) - float(lines[j][0]))**2 + (float(lines[i][1]) - float(lines[j][1]))**2) , 2)

    return distance

def init_population():
    population = []
    for i in range(POPULATION_SIZE):
        population.append(list(range(0,DIMENSION)))
        random.shuffle(population[i])
        population[i].append(None)
    return population

def print_population(population):
    count = 1
    for individual in population:
        print(count,"_ ",individual)
        count += 1
    print("---- end -----")

def value_function(population, distance,number):
    count = 0
    for individual in population:
        if count < number:
            count += 1
            continue
        individual[-1] = 0
        for i in range(DIMENSION-1):
            individual[-1] += distance[individual[i]][individual[i+1]]
        individual[-1] = round(individual[-1],2)
        count += 1
    return population

def cross_over(population):
    half = DIMENSION//2
    for i in range(0,POPULATION_SIZE,2):
        child1 = []
        child1 = child1 + population[i][:half]
        for j in range(DIMENSION):
            if population[i+1][j] not in child1:
                child1.append(population[i+1][j])
        child1.append(None)

        child2 = []
        child2 = child2 + population[i+1][:half]
        for j in range(DIMENSION):
            if population[i][j] not in child2:
                child2.append(population[i][j])
        child2.append(None)

        population.append(child1)
        population.append(child2)
    return population

def mutation(population):

    chosen_ones = np.arange(POPULATION_SIZE,POPULATION_SIZE*2,1,dtype = int)
    np.random.shuffle(chosen_ones)
    x = DIMENSION - 1
    for i in range(int(POPULATION_SIZE*MUTATION_RATE)):
        cell1 = random.randint(0, x)
        cell2 = random.randint(0, x)
        population[chosen_ones[i]][cell1],population[chosen_ones[i]][cell2] = population[chosen_ones[i]][cell2],population[chosen_ones[i]][cell1]
    return population

distance = get_distance_matrix(DIMENSION)
population = init_population()
population = value_function(population, distance,0)

count = 1
while(True):
    population = cross_over(population)
    population = mutation(population)
    population = value_function(population, distance,POPULATION_SIZE)
    population.sort(key=lambda x:x[-1])
    population = population[:POPULATION_SIZE]
    print(count,"_ ",population[0][-1])
    if population[0][-1] <= 2000000:
        print(population[0])
    count += 1