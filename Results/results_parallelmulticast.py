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

fc_path_len = read_results("res_parallelmulticast.pickle")
fc_path_len = sum(fc_path_len)/len(fc_path_len)
uc = 2117

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%f' % height,
                ha='center', va='bottom')
        
res = (fc_path_len, uc)
n_groups = 2
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8
rects1 = plt.bar(index, res, bar_width, color = 'c', label="Forwarding Costs")
autolabel(rects1)
plt.xlabel("Parallel Multicast")
plt.ylabel("Avg Cost over 200 endpoints")
plt.xticks(index, ('Forwarding Costs', 'Update Costs'))
plt.tight_layout()
plt.show()