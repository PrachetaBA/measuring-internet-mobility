import networkx as nx
import pickle
import random
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import bgp_path_selection
from pathlib import Path

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

#find the path from source to destination
def find_path(g, source, dest):
    bgp_path_selection.peer_flag = False
    return bgp_path_selection.build_path(g, source, dest)

#forwarding cost
def forwarding_cost(old_path, new_path):
    return len(new_path) - len(old_path)

#indirection paths assuming old_dest = home agent
def get_paths(g, source, old_dest, new_dest):
    old_path = find_path(g, source, old_dest)
    new_path = find_path(g, source, old_dest) + find_path(g, old_dest, new_dest)[1:]
    return old_path, new_path

def main():
    g = read_graph(Path("../Dataset/BGP_Routing_Table.pickle"))
    locations = read_lists(Path("../Dataset/Locations.pickle"))
    source_list = locations[0]
    old_dest_list = locations[1]
    new_dest_list = locations[2]
    total_fc = []
    for i in range(10):
        s = source_list[i]
        od = old_dest_list[i]
        nd = new_dest_list[i]
        op, np = get_paths(g, s, od, nd)
        print(op, "  ",np)
        total_fc.append(forwarding_cost(op,np))
        print(i)
    print(total_fc)

if __name__ == '__main__':
    main()
