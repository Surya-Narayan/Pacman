import random
import time

#Sample position
pos=[5,4]

#Manhattan Distance
def manhattan_dist(indiv,pos):
    return abs(indiv[0]-pos[0]) + abs(indiv[1]-pos[1])

#Parameters
m=3
n=8
q=4
N=20
Smax=1

# Truly random numbers by changing seed wrt time
random.seed(time.gmtime()[5])

#Initializing the population
pop=[ [ random.randint(1,50) , random.randint(1,50) ] for _ in range(n*m) ]

#Evaluate each meme
scores=[manhattan_dist(pos,x) for x in pop]

#Sorting the population
sorted_pop = [x for _,x in sorted(zip(scores,pop),reverse=True)]

memeplexes=[[]]*m
print(memeplexes)
# for indiv in sorsted_pop:
