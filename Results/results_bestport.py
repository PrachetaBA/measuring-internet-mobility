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
    fc_diff = results[0]
    fc_path_len = results[1]
    fc_shortest = results[2]
    uc = results[3]
    return fc_diff, fc_path_len, fc_shortest, uc

fc_diff, fc_path_len, fc_shortest, uc = read_results("res_best_port.pickle")

# fc_diff = sum(fc_diff)/len(fc_diff)
fc_path_len = sum(fc_path_len)/len(fc_path_len)
fc_shortest = sum(fc_shortest)/len(fc_shortest)
uc = sum(uc)/len(uc)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%f' % height,
                ha='center', va='bottom')
        
# print(fc_diff)
avg_fc = (fc_path_len, fc_shortest)
n_groups = 2
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
rects1 = plt.bar(index, avg_fc, bar_width, color = 'b', label="Forwarding Costs")
autolabel(rects1)
# rects2 = plt.bar(index + bar_width, avg_uc, bar_width, color = 'g', label="Update Costs")
# autolabel(rects2)
# plt.xlabel("Synchronization problem")
plt.ylabel("Avg Cost over 200 endpoints")
plt.xticks(index, ('Best Port', 'Shortest Path'))
# plt.legend()
plt.tight_layout()
plt.show()


