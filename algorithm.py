#! usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
sns.set_context("notebook")

def opt_func(value):
    """The mathematical function to optimize. Here it calculates the distance to origin,
    i.e. optimal solution(minimum) is at 0.
    
    Arguments:
        value {np.ndarray} -- An individual value or frog
    
    Returns:
        float -- The output value or fitness of the frog
    """
    sum=0
    for i in value:
        sum = sum + abs(i)
    return sum

def gen_frogs(frogs, dimension, sigma, mu):
    """Generates a random frog population from gaussian normal distribution.
    
    Arguments:
        frogs {int} -- Number of frogs
        dimension {int} -- Dimension of frogs/ Number of features
        sigma {int/float} -- Sigma of gaussian distribution
        mu {int/float} -- Mu of Gaussian distribution
    
    Returns:
        numpy.ndarray -- A frogs x dimension array
    """
    frogs = sigma * (np.random.randn(frogs, dimension)) + mu
    return frogs

def sort_frogs(frogs, mplx_no, opt_func):
    """Sorts the frogs in decending order of fitness by the given function.
    
    Arguments:
        frogs {numpy.ndarray} -- Frogs to be sorted
        mplx_no {int} -- Number of memeplexes, when divides frog number should return an integer otherwise frogs will be skipped
        opt_func {function} -- Function to determine fitness
    
    Returns:
        numpy.ndarray -- A memeplexes x frogs/memeplexes array of indices, [0, 0] will be the greatest frog
    """

    # Find fitness of each frog
    fitness = np.array(list(map(opt_func, frogs)))
    # Sort the indices in decending order by fitness
    sorted_fitness = np.argsort(fitness)
    # Empty holder for memeplexes
    memeplexes = np.zeros((mplx_no, int(frogs.shape[0]/mplx_no)))
    # Sort into memeplexes
    for j in range(memeplexes.shape[1]):
        for i in range(mplx_no):
            memeplexes[i, j] = sorted_fitness[i+(mplx_no*j)]
    return memeplexes

def local_search(frogs, memeplex, opt_func, sigma, mu):
    """Performs the local search for a memeplex.
    
    Arguments:
        frogs {numpy.ndarray} -- All the frogs
        memeplex {numpy.ndarray} -- One memeplex
        opt_func {function} -- The function to optimize
        sigma {int/float} -- Sigma for the gaussian distribution by which the frogs were created
        mu {int/float} -- Mu for the gaussian distribution by which the frogs were created
    
    Returns:
        numpy.ndarray -- The updated frogs, same dimensions
    """

    # Select worst, best, greatest frogs
    frog_w = frogs[int(memeplex[-1])]
    frog_b = frogs[int(memeplex[0])]
    frog_g = frogs[0]
    # Move worst wrt best frog
    frog_w_new = frog_w + (np.random.rand() * (frog_b - frog_w))
    # If change not better, move worst wrt greatest frog
    if opt_func(frog_w_new) > opt_func(frog_w):
        frog_w_new = frog_w + (np.random.rand() * (frog_g - frog_w))
    # If change not better, random new worst frog
    if opt_func(frog_w_new) > opt_func(frog_w):
        frog_w_new = gen_frogs(1, frogs.shape[1], sigma, mu)[0]
    # Replace worst frog
    frogs[int(memeplex[-1])] = frog_w_new
    return frogs

def shuffle_memeplexes(frogs, memeplexes):
    """Shuffles the memeplexes without sorting them.
    
    Arguments:
        frogs {numpy.ndarray} -- All the frogs
        memeplexes {numpy.ndarray} -- The memeplexes
    
    Returns:
        numpy.ndarray -- A shuffled memeplex, unsorted, same dimensions
    """

    # Flatten the array
    temp = memeplexes.flatten()
    #Shuffle the array
    np.random.shuffle(temp)
    # Reshape
    temp = temp.reshape((memeplexes.shape[0], memeplexes.shape[1]))
    return temp

def sfla(opt_func, frogs=30, dimension=2, sigma=1, mu=0, mplx_no=5, mplx_iters=10, solun_iters=50):
    """Performs the Shuffled Leaping Frog Algorithm.
    
    Arguments:
        opt_func {function} -- The function to optimize.
    
    Keyword Arguments:
        frogs {int} -- The number of frogs to use (default: {30})
        dimension {int} -- The dimension/number of features (default: {2})
        sigma {int/float} -- Sigma for the gaussian normal distribution to create the frogs (default: {1})
        mu {int/float} -- Mu for the gaussian normal distribution to create the frogs (default: {0})
        mplx_no {int} -- Number of memeplexes, when divides frog number should return an integer otherwise frogs will be skipped (default: {5})
        mplx_iters {int} -- Number of times a single memeplex will be iterated before shuffling (default: {10})
        solun_iters {int} -- Number of times the memeplexes will be shuffled (default: {50})
    
    Returns:
        tuple(numpy.ndarray, numpy.ndarray, numpy.ndarray) -- [description]
    """

    # Generate frogs around the solution
    frogs = gen_frogs(frogs, dimension, sigma, mu)
    # Arrange frogs and sort into memeplexes
    memeplexes = sort_frogs(frogs, mplx_no, opt_func)
    # Best solution as greatest frog
    best_solun = frogs[int(memeplexes[0, 0])]
    # For the number of iterations
    for _ in range(solun_iters):
        # Shuffle memeplexes
        memeplexes = shuffle_memeplexes(frogs, memeplexes)
        # For each memeplex
        for mplx_idx, memeplex in enumerate(memeplexes):
            # For number of memeplex iterations
            for _ in range(mplx_iters):
                # Perform local search
                frogs = local_search(frogs, memeplex, opt_func, sigma, mu)
            # Rearrange memeplexes
            memeplexes = sort_frogs(frogs, mplx_no, opt_func)
            # Check and select new best frog as the greatest frog
            new_best_solun = frogs[int(memeplexes[0, 0])]
            if opt_func(new_best_solun) < opt_func(best_solun):
                best_solun = new_best_solun
    return best_solun, frogs, memeplexes.astype(int)

def main():
    # Run algorithm
    solun, frogs, memeplexes = sfla(opt_func, 100, 2, 1, 0, 5, 25, 50)
    print("Optimal Solution (closest to zero): {}".format(solun))
    # Place memeplexes
    for idx, memeplex in enumerate(memeplexes):
        plt.scatter(frogs[memeplex, 0], frogs[memeplex, 1], marker='x', label="memeplex {}".format(idx))
    plt.scatter(solun[0], solun[1], marker='o', label="Optimal Solution")
    plt.scatter(0, 0, marker='*', label='Actual Solution')
    # Plot properties
    plt.legend()
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Shuffled Frogs")
    # Show plot
    # plt.show()

if __name__ == '__main__':
    for i in range(0,10):
        main()