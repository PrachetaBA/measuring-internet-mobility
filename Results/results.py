"""
Plotting results of the experiments, and comparing the difference between them 
"""
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict
import numpy as np

def read_results(file_name):
    with open(file_name, 'rb') as f:
        results = pickle.load(f)
    if len(results)==3:
        return results[1], results[2]
    elif len(results)==2:
        return results[1]
    else:
        return results

def average(fc, uc=None):
    if uc==None:
        return sum(fc)/len(fc)
    else:
        return sum(fc)/len(fc), sum(uc)/len(uc)

forwarding_costs_n, update_costs_n = read_results("res_best_port.pickle")
forwarding_costs_g = read_results("res_gns.pickle")
forwarding_costs_i = read_results("res_indirection.pickle")
forwarding_costs_p = read_results("res_parallelmulticast.pickle")

# print(forwarding_costs_p)
# print(type(forwarding_costs_p))

fc_n, uc_n = average(forwarding_costs_n, update_costs_n)
fc_g = average(forwarding_costs_g)
fc_i = average(forwarding_costs_i)
fc_p = average(forwarding_costs_p)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%f' % height,
                ha='center', va='bottom')
        
avg_fc = (fc_n, fc_p, fc_g, fc_i)
print(avg_fc)
#2118 is the total number of nodes we have 
avg_uc = (uc_n, 2117, 100, 1)
print(avg_uc)
n_groups = 4
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
rects1 = plt.bar(index, avg_fc, bar_width, color = 'b', label="Forwarding Costs")
autolabel(rects1)
rects2 = plt.bar(index + bar_width, avg_uc, bar_width, color = 'g', label="Update Costs")
autolabel(rects2)
plt.xlabel("Synchronization problem")
plt.ylabel("Avg Cost over 200 endpoints")
plt.xticks(index + bar_width, ('Name-based', 'Parallel Multicast', 'Lookup-based', 'Indirection'))
plt.legend()
plt.tight_layout()
plt.show()
