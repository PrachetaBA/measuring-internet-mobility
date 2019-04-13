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

#define the gns servers
def gns_servers(g, n):
    gns = random.sample(g.nodes(), n)
    return gns

#keep dictionary of closest servers
def nearest_gns_servers(g, gns, source_list):
    best_gns = {}
    i=0
    for source in source_list:
        i+=1
        print(i, end=' ')
        best_gns[source]=closest_gns(g,gns,source)
    print()
    return best_gns

#find closest gns server
def closest_gns(g, gns, source):
    gns_len = float("inf")
    gns_ser = 0
    if source in gns:
        return source
    for server in gns:
        path = find_path(g, source, server)
        if len(path)<gns_len:
            gns_len = len(path)
            gns_ser = server
            if len(path)==2:
                break 
    return server

#forwarding cost
def forwarding_cost(old_path, new_path):
    return len(new_path) - len(old_path)

#alternative forwarding_cost
def forwarding_cost_2(new_path):
    return len(new_path)

#gns paths
def get_paths(g, nearest_gns, source, old_dest, new_dest):
    server = nearest_gns[source]
    old_path = find_path(g, source, server) + find_path(g, server, source)[1:] + find_path(g, source, old_dest)[1:]
    new_path = find_path(g, source, server) + find_path(g, server, source)[1:] + find_path(g, source, new_dest)[1:]
    return old_path, new_path

def save_results(lists,file_name):
    with open(file_name,'wb') as f:
        pickle.dump(lists,f,pickle.HIGHEST_PROTOCOL)

def save_gns(g, source_list, no_gns_servers, file_name):
    gns = gns_servers(g, no_gns_servers)
    nearest_gns = nearest_gns_servers(g, gns, source_list)
    list_gns = (gns,nearest_gns)
    with open(Path(file_name),'wb') as f:
        pickle.dump(list_gns,f,pickle.HIGHEST_PROTOCOL)

def read_gns(file_name):
    with open(Path(file_name),'rb') as f:
        gns_info = pickle.load(f)
    return gns_info[0],gns_info[1]

def main():
    for x in range(6,7):
        g = read_graph(Path("../Dataset/BGP_Routing_Table.pickle"))
        locations = read_lists(Path("../Dataset/Locations.pickle"))
        source_list = locations[0]
        old_dest_list = locations[1]
        new_dest_list = locations[2]
        total_fc = []
        total_fc_2 = []
        gns, nearest_gns = read_gns("../Dataset/GNS_Servers_expt"+str(x+1)+".pickle")
        for i in range(len(source_list)):
            s = source_list[i]
            od = old_dest_list[i]
            nd = new_dest_list[i]
            op, np = get_paths(g, nearest_gns, s, od, nd)
            # print(op, "  ",np)
            # total_fc.append(forwarding_cost(op,np))
            total_fc_2.append(forwarding_cost_2(np))
            print(i, end=' ')
        results = (total_fc_2)
        save_results(results, Path("../Results/res_gns"+str(x+1)+".pickle"))

if __name__ == '__main__':
    #g = read_graph(Path("../Dataset/BGP_Routing_Table.pickle"))
    #total_nodes = len(g.nodes())
    #locations = read_lists(Path("../Dataset/Locations.pickle"))
    #source_list = locations[0]
    #experiments_gns = [total_nodes//2, total_nodes//4, total_nodes//8, total_nodes//16, total_nodes//32, total_nodes//64, total_nodes//128, total_nodes//256, total_nodes//512]
    #for i in range(4, len(experiments_gns)):
    #    file_name = "../Dataset/GNS_Servers_expt"+str(i+1)+".pickle"
    #    save_gns(g, source_list, experiments_gns[i], file_name)
    main()
