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
    for source in source_list[:2]:
        locations[source] = random.sample(list(g.nodes()),5)
    print(locations)
    return locations

#pick a destination for the new location, with a zipf distribution
def new_destination(g, locations, source_list):
    a = 2.
    for source in source_list[:2]:
        x = np.array(locations[source])
        weights = x ** (-a)
        weights /= weights.sum()
        bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))
        sample = bounded_zipf.rvs(size=200)
        print(sample)
        print()

def main():
    g = read_graph(Path("../Dataset/BGP_Routing_Table.pickle"))
    locations = read_lists(Path("../Dataset/Locations.pickle"))
    source_list = locations[0]
    l = pop_locations(g,source_list)
    new_destination(g,l, source_list)

if __name__ == '__main__':
    main()
