# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 15:13:12 2019

@author: prach
"""

import networkx as nx
from collections import deque
#import random

#demo graph
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
peer_flag = False

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
            else:
                bestp = compare_p[0]
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

def build_node_attributes_5(g, destination):
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
            else:
                bestp = compare_p[0]
            aslist = g.nodes[bestp][destination].copy()
            aslist.append(bestp)
            g.nodes[node][destination] = aslist

            #do push to customer if customer is not there ---
            #call the function that is going to do it.
            build_node_pr2c(g,node, destination)

        peerexplore.popleft()

#Node attributes should be built for every single customer AS
build_node_attributes_5(g,1)
build_node_attributes_5(g,2)
build_node_attributes_5(g,3)
build_node_attributes_5(g,4)

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
            #TODO: later change to calling peer first, and then provider if
            #there is no path
            ###################################################################
            elif options == 0:
                providers = get_providers(g,source)
                multiple_paths = []
                if len(providers)!=0:
                    for p in providers:
                        multiple_paths.append(build_path(g,p,destination))

                ## check if peer has a direct customer route to the node ##
                ## if not, then can pass to the provider ##
                elif (len(providers)==0):
                    if (peer_flag == False):
                        peers = get_peers(g, source)
                        peer_flag = True
                        for pe in peers:
                            multiple_paths.append(build_path(g,pe,destination))
                elif(len(providers)==0 and peer_flag==True):
                    return None

                if len(multiple_paths)!=0:
                    multiple_paths = [x for x in multiple_paths if x is not None]
                    best_path = min(multiple_paths, key=len)
                    path.extend(best_path)



                """
                #TODO: FIND FOR THE TOPMOST CLIQUE A PEER PATH ---
                else:
                    peers = get_peers(g,source)
                    multiple_paths = []
                    for peer in peers:
                        multiple_paths.append(build_path(g,peer,destination))
                    if len(multiple_paths)!=0:
                        best_path = min(multiple_paths, key=len)
                        path.extend(best_path)
                """
    print(path)
    return path

#for i in range(1,12):
#    print(i, g.node[i])
print(build_path(g, 1, 9))
'''
for i in range(2,12):
    print('to node', i, build_path(g, 1, i))
'''
