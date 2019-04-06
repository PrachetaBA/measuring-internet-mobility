import networkx as nx
import pickle
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import bgp_path_selection
from pathlib import Path
import numpy as np
import scipy.stats as stats
import random
import matplotlib.pyplot as plt
from collections import defaultdict

#Read the source and destination lists
def read_lists(file_name):
    with open(file_name,'rb') as f:
        data = pickle.load(f)
    return data

#Read the graph
def read_graph(graph_file_name):
    with open(graph_file_name,'rb') as f:
        g = pickle.load(f)
        return g
#save lists
def save_lists(lists,file_name):
    with open(file_name,'wb') as f:
        pickle.dump(lists,f,pickle.HIGHEST_PROTOCOL)

#find the path from source to destination
def find_path(g, source, dest):
    bgp_path_selection.peer_flag = False
    return bgp_path_selection.build_path(g, source, dest)

#define popular locations for each destination, define old and new destination
def pop_locations(g, source_list):
    locations = {}
    for source in source_list:
        locations[source] = random.sample(list(g.nodes()),6)
    print(locations)
    return locations


def old_destination(g, locations, source_list):
    old_dest = []
    for source in source_list:
        old_dest.append(random.choice(locations[source]))
    return old_dest

#pick a destination for the new location, with a zipf distribution
def new_destination(g, locations, source_list):
    new_dest = defaultdict(list)
    a = 1.
    for source in source_list:
        x = np.array(locations[source])
        y = np.array([1,2,3,4,5,6])
        weights = y ** (-a)
        weights /= weights.sum()
        bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))
        chosen_weights = dict(zip(x,weights))
        # print(chosen_weights)
        #chosen location with the zipf distribution
        sample = bounded_zipf.rvs(size=10)
        print(sample)
        for i in range(len(sample)):
            new_dest[source].append((sample[i],chosen_weights[sample[i]]))
    return new_dest

"""
For each source node, new_destination is generated 10 times, and the cost associated with forwarding
to these locations is noted. Unpopular location is characterized by probability < 0.1.
The assumption is that the request is sent to all popular locations, and if the endpoint is at an Unpopular
location, it is sent to it last.
To calculate forwarding cost, overlapping path counts should be done only once.
Update cost is the cost associated with changes to unpopular locations?
"""
def forwarding_cost(g, source, l, new_dest):
    paths = []
    pop_l = l[:4]
    for node in pop_l:
        paths.append(find_path(g, source, node))
    #get unique paths traversed --- forwarding cost in all cases,
    pop_unique_links = [y for x in paths for y in x]
    pop_path_cost = len(set(pop_unique_links))
    #check if the new_dest is a popular location or unpopular location
    #if unpopular, forwarding_cost will be added to existing forwarding cost
    unpop_l = pop_l
    if new_dest[1]<0.1:
        unpop_l.append(new_dest[0])
        npaths = []
        for node in unpop_l:
            npaths.append(find_path(g, source, node))
        unpop_unique_links = [y for x in npaths for y in x]
        unpop_path_cost = len(set(unpop_unique_links))
        return unpop_path_cost
    else:
        return pop_path_cost

def createlist():
    g = read_graph(Path("../Dataset/BGP_Routing_Table.pickle"))
    locations = read_lists(Path("../Dataset/Locations.pickle"))
    source_list = locations[0]
    l = pop_locations(g,source_list)
    old_dest = old_destination(g, l, source_list)
    new_dest = new_destination(g, l, source_list)
    parallel_multicast = (l, old_dest, new_dest)
    save_lists(parallel_multicast, Path("../Dataset/PMulticast_Locations.pickle"))

def save_results(lists,file_name):
    with open(file_name,'wb') as f:
        pickle.dump(lists,f,pickle.HIGHEST_PROTOCOL)

def main():
    g = read_graph(Path("../Dataset/BGP_Routing_Table.pickle"))
    locations = read_lists(Path("../Dataset/Locations.pickle"))
    source_list = locations[0]
    data = read_lists(Path("../Dataset/PMulticast_Locations.pickle"))
    locations = data[0]
    old_dest = data[1]
    new_dest = data[2]
    '''
    how to call fc for each of the destination in the sampled destination
    we have 10 destinations generated according to the zipfian distribution,
    even if we average the path cost, we find that the forwarding cost does
    not change as much, because the unpopular destinations are small, can be proven
    k = 8304
    v = new_dest[k]
    print(v)
    fc = forwarding_cost(g, k, locations[k], v[8])
    print(fc)
    '''
    #temporary new destination
    # tmpdest = {key:value for key,value in list(new_dest.items())[0:5]}
    total_fc = []
    i=0
    for k,v in new_dest.items():
        print(i)
        fc = 0
        for dest in v:
            fc += forwarding_cost(g, k, locations[k], dest)
        fc=fc/10
        total_fc.append(fc)
        i+=1
    # print(total_fc)
    results = (total_fc)
    # print(results)
    save_results(results, Path("../Results/res_parallelmulticast.pickle"))

if __name__ == '__main__':
    # createlist()
    main()
