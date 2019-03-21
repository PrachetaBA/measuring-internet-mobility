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

#Read the source and destination lists
def read_lists(file_name):
    with open(file_name,'rb') as f:
        locations = pickle.load(f)
    return locations

#Read the graph
def read_graph(graph_file_name):
    with open(graph_file_name,'rb') as f:
        g = pickle.load(f)
        return g

#define popular locations for each destination, define old and new destination
def pop_locations(g, source_list):
    locations = {}
    for source in source_list[:1]:
        locations[source] = random.sample(list(g.nodes()),6)
    print(locations)
    return locations

def old_destination(g, locations, source_list):
    old_dest = []
    for source in source_list[:1]:
        old_dest.append(random.choice(locations[source]))
    return old_dest

#pick a destination for the new location, with a zipf distribution
def new_destination(g, locations, source_list):
    #TODO: modify a to fit a "good" distribution
    new_dest = []
    a = 1.2
    for source in source_list[:1]:
        x = np.array(locations[source])
        y = np.array([1,2,3,4,5,6])
        weights = y ** (-a)
        weights /= weights.sum()
        bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))
        chosen_weights = dict(zip(x,weights))
        #chosen location with the zipf distribution
        sample = bounded_zipf.rvs(size=1)
        new_dest.append((sample[0],chosen_weights[sample[0]]))
    return new_dest

def main():
    g = read_graph(Path("../Dataset/BGP_Routing_Table.pickle"))
    locations = read_lists(Path("../Dataset/Locations.pickle"))
    source_list = locations[0]
    l = pop_locations(g,source_list)
    old_dest = old_destination(g, l, source_list)
    new_dest = new_destination(g, l, source_list)
    print(old_dest)
    print(new_dest)

if __name__ == '__main__':
    main()
