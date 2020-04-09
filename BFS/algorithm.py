import numpy as np
import matplotlib.pyplot as plt

best_solun=np.array(2)
def opt_func(value):
    output = np.sqrt((value ** 2).sum())
    return output

def gen_frogs(frogs, dimension):
    # frogs =  (np.random.randn(frogs, dimension)) 
    frogs =  (np.random.randint(1,28,(frogs, dimension))) 
    print(frogs)
    print(np.shape(frogs))
    return frogs

def sort_frogs(frogs, mplx_no, opt_func):
    
    # Find fitness of each frog
    fitness = np.array(list(map(opt_func, frogs)))
    sorted_fitness = np.argsort(fitness)
    memeplexes = np.zeros((mplx_no, int(frogs.shape[0]/mplx_no)))
    for j in range(memeplexes.shape[1]):
        for i in range(mplx_no):
            memeplexes[i, j] = sorted_fitness[i+(mplx_no*j)]
    return memeplexes

def local_search(frogs, memeplex, opt_func):
    # Select worst, best, greatest frogs
    frog_w = frogs[int(memeplex[-1])]
    frog_b = frogs[int(memeplex[0])]
    frog_g = best_solun
    # print(memeplex)
    # Move worst wrt best frog
    frog_w_new = frog_w + (np.random.rand() * (frog_b - frog_w))
    # If change not better, move worst wrt greatest frog
    if opt_func(frog_w_new) > opt_func(frog_w):
        frog_w_new = frog_w + (np.random.rand() * (frog_g - frog_w))
    # If change not better, random new worst frog
    if opt_func(frog_w_new) > opt_func(frog_w):
        frog_w_new = gen_frogs(1, frogs.shape[1])[0]
    # Replace worst frog
    frogs[int(memeplex[-1])] = frog_w_new
    return frogs

def shuffle_memeplexes(frogs, memeplexes):
    # Flatten the array
    temp = memeplexes.flatten()
    #Shuffle the array
    np.random.shuffle(temp)
    # Reshape
    temp = temp.reshape((memeplexes.shape[0], memeplexes.shape[1]))
    return temp

def sfla(opt_func, frogs, dimension, mplx_no, mplx_iters, solun_iters):
    # Generate frogs around the solution
    frogs = gen_frogs(frogs, dimension)
    memeplexes = sort_frogs(frogs, mplx_no, opt_func)
    # Best solution as greatest frog
    global best_solun 
    best_solun = frogs[int(memeplexes[0, 0])]
    # For the number of iterations
    for i in range(solun_iters):
        # Shuffle memeplexes
        memeplexes = shuffle_memeplexes(frogs, memeplexes)
        # For each memeplex
        for mplx_idx, memeplex in enumerate(memeplexes):
            # For number of memeplex iterations
            for j in range(mplx_iters):
                # Perform local search
                frogs = local_search(frogs, memeplex, opt_func)
            # Rearrange memeplexes
            memeplexes = sort_frogs(frogs, mplx_no, opt_func)
            # Check and select new best frog as the greatest frog
            new_best_solun = frogs[int(memeplexes[0, 0])]
            if opt_func(new_best_solun) < opt_func(best_solun):
                best_solun = new_best_solun
    return best_solun, frogs, memeplexes.astype(int)

def main():
    # Run algorithm
    solun, frogs, memeplexes = sfla(opt_func, 80, 2, 5, 25, 50)
    print("Optimal Solution (closest to zero): {}".format(solun))
    # print(frogs)
    # print(memeplexes)

    plt.scatter(solun[0], solun[1], marker='o', label="Optimal Solution")
    plt.scatter(0, 0, marker='*', label='Actual Solution')
    
    # Place memeplexes
    for idx, memeplex in enumerate(memeplexes):
        # print(frogs[memeplex,0],frogs[memeplex,1])
        # print(count)
        # count+=1
        # print((frogs[memeplex]))
        plt.scatter(frogs[memeplex, 0], frogs[memeplex, 1], marker='x', label="memeplex {}".format(idx))
        # plt.pause(0.5)
        # plt.scatter( (frogs[memeplex])[0][0], (frogs[memeplex])[0][0], marker='x', label="memeplex {}".format(idx))    
    # Plot properties
    plt.legend()
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Shuffled Frogs")
    # Show plot
    plt.show()

if __name__ == '__main__':
    main()