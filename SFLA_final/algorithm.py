import numpy as np
import matplotlib.pyplot as plt
import time
import math
count=0
allf=dict()
globalopt=[]
def opt_func(value):
    # print(globalopt)
    l=np.array(globalopt)
    value.astype(int)
    # print(l)
    output=abs(int(value[0])-int(l[0]))+abs(int(value[1])-int(l[1]))
    # output = np.sqrt(((value-l) ** 2).sum())
    return output

def gen_frogs(frogs, dimension, sigma, mu):

    l=[]
    # for i in range(100):
        # l.append(np.random.randint( (28,30) ) )
    #Choose randomly from list of possible points
    l=np.random.randint(0,28,(frogs,dimension))
    global allf
    for i in l:
        allf[tuple(i)]=list()
    return l

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

def mean_memeplexes(frogs,memeplex):
    s=[0,0]
    for m in range(len(memeplex)):
        # print(frogs[int(memeplex[m])])
        s[0]+=frogs[int(memeplex[m])][0]
        s[1]+=frogs[int(memeplex[m])][1]
        # s+=frogs[int(memeplex[m])]
    s[0]=s[0]/len(memeplex)
    s[1]=s[1]/len(memeplex)
    return s

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
    global allf
    
    # Select worst, best, greatest frogs
    frog_w = frogs[int(memeplex[-1])]
    frog_b = frogs[int(memeplex[0])]
    frog_g = frogs[0]

    #Get mean and median
    mn=sum(frogs[int(i)] for i in memeplex)//len(memeplex)
    median=frogs[int(memeplex[len(memeplex)//2])]

    if manhattan1(mn,frog_b)>manhattan1(median,frog_b):
        avg=mn
    else:
        avg=median
    # Move worst wrt best frog    
    # frog_w_new = frog_w + (np.random.randn() * (frog_b - frog_w))
    frog_w_new = frog_w + (np.random.randn() * (avg - frog_w))
    frog_w_new.astype(int)

    # rndm=np.random.randn()
    # wtd_avg=rndm*(mn)+(1-rndm)*median
    # frog_w_new = frog_w + (np.random.randn() * (wtd_avg - frog_w))
    # frog_w_new.astype(int)
 
    # If change not better, move worst wrt greatest frog
    if opt_func(frog_w_new) > opt_func(frog_w):
 
        frog_w_new = frog_w + (np.random.randn() * (frog_g - frog_w))
        frog_w_new.astype(int)

    # If change not better, random new worst frog
    if opt_func(frog_w_new) > opt_func(frog_w):
        global count
        count+=1
        frog_w_new=np.random.randint(0,28,(1,2))
        frog_w_new=frog_w_new[0]
        # frog_w_new = gen_frogs(1, frogs.shape[1], sigma, mu)[0]
    # Replace worst frog
    # print(frogs[int(memeplex[-1])],":",frog_w_new)
    f_w=[0,0]
    f_w[0]=frogs[int(memeplex[-1])][0]
    f_w[1]=frogs[int(memeplex[-1])][1]
    frogs[int(memeplex[-1])] = frog_w_new
    
    # if(tuple(cpy) not in allf.keys()):
    #     for i in allf.keys():
    #         if (list(cpy) in allf[i]) and (list(frog_w_new) not in allf[i]):
    #             print("Added",cpy,":",frog_w_new)
    #             allf[i].append(list(frog_w_new))
    # # elif(list(frog_w_new) not in allf[tuple(cpy)]):
    # else:
    #     # print(frog_w,":",frog_w_new)
    #     allf[tuple(cpy)]=[]
    #     print("Added",cpy,":",frog_w_new)
    #     allf[tuple(cpy)].append(list(frog_w_new))
    f_w_new=[0,0]
    f_w_new[0]=int(frog_w_new[0])
    f_w_new[1]=int(frog_w_new[1])
    if(tuple(f_w) not in allf.keys()):
        # it is in a list
        for i in allf.keys():
            if(list(f_w) in allf[i]):
                if(list(f_w_new) not in allf[i]):
                    # print("---------------",allf[i][-1])
                    if(opt_func(np.array(allf[i][-1])) > 1):
                        allf[i].append(f_w_new)
    else:
        if(f_w_new not in allf[tuple(f_w)]):
            allf[tuple(f_w)].append(f_w_new)
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

def manhattan1(o,o2):
        # print(o,type(o))
        return abs(int(o[0])-int(o2[0])) +  abs(int(o[1])-int(o2[1]))

def sfla(optimum,opt_func, frogs, dimension=2, sigma=1, mu=0, mplx_no=5, mplx_iters=10, solun_iters=50):
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
    global globalopt
    globalopt=optimum
    global allf
    allf=dict()
    # print(globalopt)
    # Generate frogs around the solution
    frogs = gen_frogs(frogs, dimension, sigma, mu)
    # print(frogs)
    # Arrange frogs and sort into memeplexes
    memeplexes = sort_frogs(frogs, mplx_no, opt_func)
    # Best solution as greatest frog
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
                frogs = local_search(frogs, memeplex, opt_func, sigma, mu)
            # Rearrange memeplexes
            # print(count)
            memeplexes = sort_frogs(frogs, mplx_no, opt_func)
            # Check and select new best frog as the greatest frog
            new_best_solun = frogs[int(memeplexes[0, 0])]
            if opt_func(new_best_solun) < opt_func(best_solun):
                best_solun = new_best_solun
    # return best_solun, frogs, memeplexes.astype(int)
    # allf1=dict()
    # for i in allf.keys():
    #     for x in allf[i]:
    #         # x[0]=int(x[0])
    #         # x[1]=int(x[1])
    #         if i not in allf1.keys():
    #             allf1[i]=[]
    #             allf1[i].append(list(x))
    #         if list(x) not in allf[i]:
    #             allf1[i].append(list(x))
    final=dict()
    frogs=allf
    for f in frogs.keys():
        for t in frogs[f]:
            if t[0]==best_solun[0] and t[1]==best_solun[1] or manhattan1(t,best_solun)<5:
                ctd=[]
                ctd.append(f)
                for i in range(len(frogs[f])-1):
                    if opt_func(np.array(ctd[-1]) ) < opt_func( np.array(frogs[f][i]) ):
                        continue
                    # plt.scatter(frogs[f][i][0],frogs[f][i][1])
                    ctd.append(frogs[f][i])
                # print(f,":",ctd)
                final[f]=ctd
                # plt.show() 

    # return best_solun, allf, memeplexes.astype(int)
    return best_solun, final, memeplexes.astype(int)

def main():
    # Run algorithm
    #Frogs
    # frogs=[]
    # for i in range(100):
        # frogs.append(np.array([i,i]))
    # frogs=np.array(frogs)
    # frogs=np.reshape(frogs,(100,2))
    
    solun, frogs, memeplexes = sfla([15,15],opt_func, 20, 2, 1, 0, 5, 10, 10)
    # for f in frogs.keys():
    #     for t in frogs[f]:
    #         if t[0]==solun[0] and t[1]==solun[1]:
    #             ctd=[]
    #             ctd.append(f)
    #             for i in range(len(frogs[f])-1):
    #                 if opt_func(np.array(ctd[-1]) ) < opt_func( np.array(frogs[f][i]) ):
    #                     continue
    #                 plt.scatter(frogs[f][i][0],frogs[f][i][1])
    #                 ctd.append(frogs[f][i])
    #             print(f,":",ctd)    
    #             # plt.show() 
    
        # l=frogs[f]
        # for s in l:
            # if s[0]==solun[0] and s[1]==solun[1]:
                # count+=1
                # print("The frog ",f," reaches the solution")
    # print("\n","total Frogs:",len(list(frogs.keys())),"Frogs that reach sol:",count)
    # key=tuple()
    # lent=0
    # for i in frogs.keys():
        # print(i,":",(frogs[i]))
    #     if(len(frogs[i])>lent):
    #         key=i
    #         lent=len(frogs[i])
    # print(frogs[key])
    # print(frogs)
    global count
    print("Optimal Solution (closest to zero): {}".format(solun),count)
    tmp=count
    count=0
    return solun,tmp
    # Place memeplexes
    # for idx, memeplex in enumerate(memeplexes):
    #     plt.scatter(frogs[memeplex, 0], frogs[memeplex, 1], marker='x', label="memeplex {}".format(idx))
    # plt.scatter(solun[0], solun[1], marker='o', label="Optimal Solution")
    # plt.scatter(13, 29, marker='*', label='Actual Solution')
    # # Plot properties
    # plt.legend()
    # plt.xlabel("x-axis")
    # plt.ylabel("y-axis")
    # plt.title("Shuffled Frogs")
    # # Show plot
    # plt.show()

if __name__ == '__main__':
    l=[]
    mx,my=0,0
    c=0
    # global count
    for i in range(10):
        sol,tmp=main()
        c+=tmp
        # global count
        # count=0
        mx+=sol[0]
        my+=sol[1]
        l.append(sol)
    
    mx=mx//10
    my=my//10
    print(mx,my)
    vx,vy=0,0
    d=0
    for i in l:
        # print(mx,i[0],mx,i[1])
        # print(math.sqrt(pow(i[0]-mx,2)+pow(i[1]-my,2)))
        d+=math.sqrt(pow(i[0]-15,2)+pow(i[1]-15,2))
        # vx=+pow(mx-i[0],2)
        # vy=+pow(mx-i[1],2)
    print("Variance:",d)
    print("Avg New Random Frogs:",c/10)    