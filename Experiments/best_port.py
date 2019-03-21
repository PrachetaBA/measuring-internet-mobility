import networkx as nx
import pickle
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# from bgp_path_selection import build_path
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

#find the path before and after mobility
def find_paths(g, source, old_dest, new_dest):
    bgp_path_selection.peer_flag = False
    old_path = bgp_path_selection.build_path(g, source, old_dest)
    bgp_path_selection.peer_flag = False
    new_path = bgp_path_selection.build_path(g, source, new_dest)
    return old_path, new_path

#find the forwarding cost - name based forwarding
def forwarding_cost(old_path, new_path):
    return len(new_path) - len(old_path)

#find update cost for a particular movement
def update_cost(g, old_dest, new_dest):
    uc_count = 0
    for node in g.nodes():
        if old_dest in g.nodes[node] and len(g.nodes[node][old_dest])>1:
            next_hop_old = g.nodes[node][old_dest][1]
        else:
            next_hop_old = 0
        if new_dest in g.nodes[node] and len(g.nodes[node][new_dest])>1:
            next_hop_new = g.nodes[node][new_dest][1]
        else:
            next_hop_new = 0
        if next_hop_old!=next_hop_new:
            uc_count+=1
    return uc_count

def save_results(lists,file_name):
    with open(file_name,'wb') as f:
        pickle.dump(lists,f,pickle.HIGHEST_PROTOCOL)

def main():
    g = read_graph(Path("../Dataset/BGP_Routing_Table.pickle"))
    locations = read_lists(Path("../Dataset/Locations.pickle"))
    source_list = locations[0]
    old_dest_list = locations[1]
    new_dest_list = locations[2]
    total_fc = []
    total_uc = []
    for i in range(len(source_list)):
        s = source_list[i]
        od = old_dest_list[i]
        nd = new_dest_list[i]
        op,np = find_paths(g, s, od, nd)
        total_fc.append(forwarding_cost(op,np))
        total_uc.append(update_cost(g, od, nd))
        # print(i)
    print(total_fc)
    print(total_uc)
    results = (total_fc, total_uc)
    save_results(results, Path("../Results/res_best_port.pickle"))

if __name__ == '__main__':
    main()
