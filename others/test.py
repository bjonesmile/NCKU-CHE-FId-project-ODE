import numpy as np
import itertools
import csv
import winsound
import itertools

t_step = 1
sim_time = 240

sv1 = 3 #Sa
sv2 = 1 #T
sv_set = [sv1,sv2]

sv_num = 2

sa_point = np.max(sv_set)

sv_list = []

for i in range(sv_num):
    if sv_set[i] == sa_point:
        sv_list.append(np.arange(sa_point+t_step,sim_time+1,t_step)) 
    else :
        sv_list.append(np.arange(sa_point,sim_time+1,t_step)) 
    
print(sv_list)

print("init state:")

state_list = [0,1]
print(list(itertools.product([0,1],repeat=1)))

exit()

sv1_list = np.arange(sa_point+t_step,sim_time+1,t_step)
sv1_list = np.arange(sa_point,sim_time+1,t_step)

t_list = np.arange(sv,240,5)
print(len(t_list))

total_list = []
total_list.extend([{'var':'Sa','point':t} for t in t_list])
total_list.extend([{'var':'T','point':t} for t in t_list])
print(total_list)
print(len(total_list))

def beep():
    print("\a")

