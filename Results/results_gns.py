"""
Plotting results of best port forwarding and comparing the difference between them 
"""
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict
import numpy as np

def read_results(file_name):
    with open(file_name, 'rb') as f:
        results = pickle.load(f)
    return results

gns_fc = []
for i in range(9):
    gns_fc.append(read_results("res_gns"+str(i+1)+".pickle"))

gns_fc_avg = []
for i in gns_fc:
    gns_fc_avg.append(sum(i)/len(i))

total_nodes = 2118
x_axis = [total_nodes//2, total_nodes//4, total_nodes//8, total_nodes//16, total_nodes//32, total_nodes//64, \
total_nodes//128, total_nodes//256, total_nodes//512]


fig, ax = plt.subplots()
plt.plot(x_axis, gns_fc_avg, 'g^')
plt.xlabel('Number of lookup servers in the network')
plt.ylabel('Average forwarding cost')
plt.title('lookup servers vs. forwarding cost')
plt.tight_layout()
plt.show()
