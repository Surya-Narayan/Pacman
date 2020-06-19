import matplotlib.pyplot as plt
import matplotlib
import re
import math
prev=[-1,-1]
f=open("3.txt","r")
x=[]
y=[]

count=0
d=0
prevx,prevy=0,0
for line in f:
    tmp=re.findall("\d+.\\d+",line)
    if count==0:
        count=1
        prevx=float(tmp[0])
        prevy=float(tmp[1])
        continue
    d+=math.sqrt(pow(prevx-float(tmp[0]),2)+pow(prevy-float(tmp[1]),2))
    prevx=float(tmp[0])
    prevy=float(tmp[1])
print(d)
