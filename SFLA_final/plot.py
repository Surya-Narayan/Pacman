import matplotlib.pyplot as plt
import matplotlib
import re
prev=[-1,-1]
f=open("3.txt","r")
x=[]
y=[]
for line in f:
    tmp=re.findall("\d+.\\d+",line)
    x.append(float(tmp[0]))
    y.append(float(tmp[1]))
plt.scatter(x,y)
plt.plot(x,y)
axes = plt.gca()
axes.set_xlim([0,30])
axes.set_ylim([0,30])
plt.ylim(max(plt.ylim()), min(plt.ylim()))
# for i in range(len(x)):
    # plt.scatter(x[i],y[i])
    # if prev[0]!=-1:
        # x_l=[prev[0],x[i]]
        # y_l=[prev[1],y[i]]
        # plt.plot(x_l,y_l)
    # prev[0]=x[i]
    # prev[1]=y[1]
    # print(x[i],y[i])

plt.show()
