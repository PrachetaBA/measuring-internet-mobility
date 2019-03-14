import pickle
import networkx as nx
import random

#Read the graph from the file
def read_graph(graph_file_name):
    with open(graph_file_name,'rb') as f:
        g = pickle.load(f)
        return g

#Save source and destination lists to pickle file_name
def save_lists(lists,file_name):
    with open(file_name,'wb') as f:
        pickle.dump(lists,f,pickle.HIGHEST_PROTOCOL)

#Choose nodes
def choose_nodes(g, endpoints):
    #Pick given number of different source and destination pairs
    nodes = list(g.nodes())
    source_list = random.sample(nodes, endpoints)

    #For the same x sources, pick different destinations which are random
    counter = 0
    old_dest_list = list()
    while(counter<endpoints):
        destination = random.choice(nodes)
        if(destination not in source_list and destination not in old_dest_list):
            old_dest_list.append(destination)
            counter+=1

    counter = 0
    new_dest_list = list()
    while(counter<endpoints):
        destination = random.choice(nodes)
        if(destination not in source_list and destination not in new_dest_list and destination!=old_dest_list[counter]):
            new_dest_list.append(destination)
            counter+=1

    print("Source list is: " + str(source_list))
    print("Old destination list is: " + str(old_dest_list))
    print("New destination list is: " + str(new_dest_list))
    return source_list, old_dest_list, new_dest_list

def main():
    #TODO: Change to relative paths
    g = read_graph("C:\\Users\\prach\\OneDrive - University of Massachusetts\\UMass\\measuring-internet-mobility\\Dataset\\BGP_Routing_Table.pickle")
    source_list, old_dest_list, new_dest_list = choose_nodes(g, 200)
    saved = (source_list, old_dest_list, new_dest_list)
    save_lists(saved,"C:\\Users\\prach\\OneDrive - University of Massachusetts\\UMass\\measuring-internet-mobility\\Dataset\\Locations.pickle")

if __name__ == '__main__':
    main()
