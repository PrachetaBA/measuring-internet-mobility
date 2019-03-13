# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 15:13:12 2019

@author: prach
"""

import networkx as nx
from collections import deque
import random
import pickle
#demo graph 1
"""
g = nx.DiGraph()
g.add_edge(1,5,rel=-1)
g.add_edge(5,1,rel=1)
g.add_edge(2,5,rel=-1)
g.add_edge(5,2,rel=1)
g.add_edge(5,7,rel=-1)
g.add_edge(7,5,rel=1)
g.add_edge(3,6,rel=-1)
g.add_edge(6,3,rel=1)
g.add_edge(6,7,rel=-1)
g.add_edge(7,6,rel=1)
g.add_edge(10,7,rel=0)
g.add_edge(7,10,rel=0)
g.add_edge(8,7,rel=0)
g.add_edge(7,8,rel=0)
g.add_edge(8,10,rel=0)
g.add_edge(10,8,rel=0)
g.add_edge(4,8,rel=-1)
g.add_edge(8,4,rel=1)
g.add_edge(4,9,rel=-1)
g.add_edge(9,4,rel=1)
g.add_edge(9,10,rel=-1)
g.add_edge(10,9,rel=1)
g.add_edge(7,11,rel=1)
g.add_edge(11,7,rel=-1)
g.add_edge(2,11,rel=-1)
g.add_edge(11,2,rel=1)
g.add_edge(6,11,rel=0)
g.add_edge(11,6,rel=0)
"""
# peer_flag = False

#demo_Graph-2
def build_small_graph(text_file_name):
    try:
        f = open(text_file_name,"r")
        for line in f:
            line = line.rstrip('\n')
            a = line.split(sep="|")
            from_node = int(a[0])
            to_node = int(a[1])
            rel = int(a[2])
            #if from_node in nodes_new_g and to_node in nodes_new_g:
            if from_node not in g:
                g.add_node(from_node)
            if to_node not in g:
                g.add_node(to_node)
            g.add_edge(from_node, to_node, rel=rel)
            if(rel==-1):
                g.add_edge(to_node, from_node,rel=1)
            if(rel==0):
                g.add_edge(to_node,from_node,rel=0)
            if(rel==1):
                g.add_edge(to_node, from_node, rel=-1)

        f.close()
    except IndexError as error:
        print(error)

    return g


def get_providers(g, node):
    p_list = list(g.adj[node])
    for n in p_list[:]:
        if g.__getitem__(node)[n]['rel']!=-1:
            p_list.remove(n)
    return p_list

def get_customers(g,node):
    c_list = list(g.adj[node])
    for n in c_list[:]:
        if g.__getitem__(node)[n]['rel']!=1:
            c_list.remove(n)
    return c_list

def get_peers(g,node):
    final_list = []
    peer_list = list(g.adj[node])
    for peer in peer_list:
        if g.__getitem__(node)[peer]['rel']==0:
            final_list.append(peer)
    return final_list

def build_node_pr2c(g,node,destination):
    toexplore = deque()
    toexplore.append(node)
    while toexplore:
        node = toexplore[0]
        clist = get_customers(g,node)
        for i in clist:
            if i not in toexplore:
                toexplore.append(i)

        if destination in g.nodes[node].keys():
            pass
        else:
            provider_list = get_providers(g,node)
            compare_p = []
            for pro in provider_list:
                if destination in g.nodes[pro].keys():
                    compare_p.append(pro)
            if len(compare_p)>1:
                #measure which provider has the shortest aslist and choose that as the best provider
                bestp = compare_p[0]
                bestplen = len(g.nodes[bestp][destination])
                for p in compare_p:
                    aslen = len(g.nodes[p][destination])
                    if aslen < bestplen:
                        bestp = p
            elif len(compare_p)==1:
                bestp = compare_p[0]
            else:
                break
            aslist = g.nodes[bestp][destination].copy()
            aslist.append(bestp)
            g.nodes[node][destination] = aslist

        toexplore.popleft()

def check_ifc(g, node, destination):
    route = g.nodes[node][destination]
    if g.__getitem__(node)[route[-1]]['rel']==1:
        return True
    else:
        return False

def build_node_attributes(g, destination):
    toexplore = deque()
    toexplore.append(destination)
    peerexplore = deque()
    while toexplore:
        node = toexplore[0]
        plist = get_providers(g,node)
        for i in plist:
            if i not in toexplore:
                toexplore.append(i)
        peerlist = get_peers(g,node)
        for j in peerlist:
            if j not in peerexplore:
                peerexplore.append(j)
        if node!=destination:
            if destination in get_customers(g,node):
                g.nodes[node][destination] = [destination]
            else:
                #get all customer routes, compare among the many THAT HAVE A ROUTE TO DESTINATION, and choose the smallest one
                aslist = []
                clist = get_customers(g, node)
                if len(clist)!=1:
                    compare_c = []
                    #check if every customer has a route to that destination
                    for c in clist:
                        if destination in g.nodes[c].keys():
                            compare_c.append(c)

                    if len(compare_c)>1:
                        #if all do, check which is the shortest
                        #if equal, add both? but which will it advertise?
                        bestc = compare_c[0]
                        bestclen = len(g.nodes[bestc][destination])
                        for c in compare_c:
                            aslen = len(g.nodes[c][destination])
                            if aslen < bestclen:
                                bestc = c

                    else:
                        bestc = compare_c[0]
                    #after choosing the best
                    aslist = g.nodes[bestc][destination].copy()
                    aslist.append(bestc)
                    g.nodes[node][destination] = aslist
                else:
                    aslist = (g.nodes[clist[0]][destination]).copy()
                    aslist.append(clist[0])
                    g.nodes[node][destination] = aslist

        toexplore.popleft()


    while peerexplore:
        node = peerexplore[0]
        if destination in g.nodes[node].keys() and check_ifc(g, node, destination)==True:
            peerexplore.popleft()
        else:
            #get list of all peers who have a route to the destination
            #TODO: what to do if multiple peers have a route to the destination? pick randomly?
            peerlist = get_peers(g,node)
            compare_p = []
            for p in peerlist:
                if destination in g.nodes[p].keys():
                    compare_p.append(p)
            #DEBUG:
            #print(node, compare_p)
            if len(compare_p)>1:
                #if multiple peers have the destination then we choose the peer which has the shortest AS path
                #Can tweak by random choice if we need variety ---
                #bestp = random.choice(compare_p)

                bestp = compare_p[0]
                bestplen = len(g.nodes[bestp][destination])
                for p in compare_p:
                    aslen = len(g.nodes[p][destination])
                    if aslen < bestplen:
                        bestp = p
            elif len(compare_p)==1:
                bestp = compare_p[0]
            else:
                break
            aslist = g.nodes[bestp][destination].copy()
            aslist.append(bestp)
            g.nodes[node][destination] = aslist


            #do push to customer if customer is not there ---
            #call the function that is going to do it.
            build_node_pr2c(g,node, destination)
        if len(peerexplore)==0:
            break
        peerexplore.popleft()


def get_relationship(g, source, destination):
    return g.__getitem__(source)[destination]['rel']

#TODO: once it reaches topmost provider, add a calling node and a boolean flag which is set to False
#set the flag to true, and if true, don't call peer again.
#first time it will be false
def build_path(g, source, destination):
    '''
    Algorithm
    1. First every item looks at its own neighbors, and if its a neighbor, then send it directly
    2. Then every node looks at it's routing table entry keys -- then the path is already defined
    3. if this doesn't work, then do the following ----
    Every node looks at every entry of its routing table,
    Case A: if the AS is included
        a. If AS exists in only one path, then take that path
        b. If there are multiple paths, check the last AS on that - follow customer > peer > provider
    Case B: if the AS is not included
        a. Forward to provider, add to a global path variable the AS number
    '''
    global peer_flag
    path = [source]
    while path[-1]!=destination:
        if destination in g.adj[source]:
            path.append(destination)
        elif destination in g.nodes[source].keys():
            path.extend(list(reversed(g.nodes[source][destination])))
        else:
            entries = list((key for key, vals in g.nodes[source].items() if destination in vals))
            options = len(entries)
            if options > 0:
                if options == 1:
                    key = entries[0]
                    all_as = list(reversed(g.nodes[source][key][1:]))
                    for a in all_as:
                        if a != destination:
                            path.append(a)
                        else:
                            path.append(a)
                            break
                elif options > 1:
                    #choose the key which is the customer path, over the peer path, over the provider path
                    key = 0
                    customers = []
                    peers = []
                    pro = []
                    for asnum in entries:
                        full_list = list(reversed(g.nodes[source][asnum]))
                        choice = full_list[0]
                        relation = get_relationship(g, source, choice)
                        if relation==1:
                            customers.append(asnum)
                        elif relation==0:
                            peers.append(asnum)
                        elif relation==-1:
                            pro.append(asnum)
                    if customers:
                        key = customers[0]
                    elif peers:
                        key = peers[0]
                    else:
                        key = pro[0]

                    all_as = list(reversed(g.nodes[source][key][1:]))
                    for a in all_as:
                        if a != destination:
                            path.append(a)
                        else:
                            path.append(a)
                            break

            ###################################################################
            #Fixed
            ###################################################################
            elif options == 0:
                providers = get_providers(g,source)
                multiple_paths = []
                peer_paths = []
                if len(providers)!=0:
                    for p in providers:
                        multiple_paths.append(build_path(g,p,destination))

                    if len(multiple_paths)!=0:
                        # print("mult", multiple_paths)
                        multiple_paths = [x for x in multiple_paths if x is not None]
                        if multiple_paths:
                            best_path = min(multiple_paths, key=len)
                            path.extend(best_path)
                        else:
                            return
                ## check if peer has a direct customer route to the node ##
                ## if not, then can pass to the provider ##
                elif (len(providers)==0):
                    if (peer_flag == False):
                        peers = get_peers(g, source)
                        peer_flag = True
                        for pe in peers:
                            #print(peer_flag)
                            peer_paths.append(build_path(g,pe,destination))

                        if len(peer_paths)!=0:
                            # print("peer", peer_paths)
                            peer_paths = [x for x in peer_paths if x is not None]
                            if peer_paths:
                                best_path = min(peer_paths, key=len)
                                path.extend(best_path)
                            else:
                                return

                    else:
                        # return None
                        return

    # print("from source ", source, " the path is", path)
    return path

#function to find the leaf nodes
#TODO: Fix customer_only
def customer_only():
    c_only = []
    for i in g.adjacency():
        node = i[0]
        neighbor = i[1]
        list1 = neighbor.keys()
        all_rel = []
        for j in list1:
            all_rel.append(neighbor[j]['rel'])
        if 1 not in all_rel:
            c_only.append(node)
    return c_only
"""
Read graph from a pickle file
"""
def read_graph(graph_file_name):
    with open(graph_file_name,'rb') as f:
        g = pickle.load(f)
        return g

"""
Save graph to a pickle file
"""
def save_graph(g,file_name):
    with open(file_name,'wb') as f:
        pickle.dump(g,f,pickle.HIGHEST_PROTOCOL)

def build_routing_table(g):
    c = customer_only()
    print(len(c))
    count=0
    for cust in c:
        build_node_attributes(g, cust)
        count+=1
        print(count)

    save_graph(g, "Dataset/BGP_Routing_Table.pickle")

if __name__ == '__main__':
    g = nx.DiGraph()
    g = read_graph("Dataset/BGP_Routing_Table.pickle")
    print("read the graph")
    # build_routing_table(g)

    source = random.choice(customer_only())
    destination = random.choice(list(g.nodes()))
    # source = 13700
    # destination = 3491

    print('source', source, 'dest', destination)
    # print('source', g.adj[source])
    # print()
    # print('destination', g.adj[destination])
    if source!=destination:
       peer_flag = False
       print(build_path(g,source,destination))
