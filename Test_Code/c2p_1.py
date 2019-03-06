# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 17:55:15 2019

@author: prach
"""
import networkx as nx
from collections import deque


g = nx.DiGraph()
g.add_edge(1,2,rel=-1)
g.add_edge(2,1,rel=1)
g.add_edge(1,3,rel=-1)
g.add_edge(3,1,rel=1)
g.add_edge(2,4,rel=-1)
g.add_edge(4,2,rel=1)
g.add_edge(2,5,rel=-1)
g.add_edge(5,2,rel=1)
g.add_edge(3,6,rel=-1)
g.add_edge(6,3,rel=1)
g.add_edge(4,7,rel=-1)
g.add_edge(7,4,rel=1)
g.add_edge(6,7,rel=-1)
g.add_edge(7,6,rel=1)
g.add_edge(7,9,rel=-1)
g.add_edge(9,7,rel=1)
g.add_edge(10,3,rel=-1)
g.add_edge(3,10,rel=1)
g.add_edge(8,9,rel=0)
g.add_edge(9,8,rel=0)
g.add_edge(5,6,rel=0)
g.add_edge(6,5,rel=0)
g.add_edge(11,4,rel=-1)
g.add_edge(4,11,rel=1)
g.add_edge(12,4,rel=1)
g.add_edge(4,12,rel=-1)
g.add_edge(7,12,rel=0)
g.add_edge(12,7,rel=0)
g.add_edge(12,8,rel=-1)
g.add_edge(8,12,rel=1)
g.add_edge(5,7,rel=-1)
g.add_edge(7,5,rel=1)
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
'''
for node in g.node():
    print(node, g.adj[node])
nx.draw(g, with_labels=True)
'''
###############################################################################
#   First rev - only gets customer routes 
###############################################################################
def build_node_attributes_3(g, destination):
    toexplore = deque()
    toexplore.append(destination)
    while toexplore:
        node = toexplore[0]
        plist = get_providers(g,node)
        for i in plist:
            if i not in toexplore:
                toexplore.append(i)
        if node==destination: 
            print('first')
        else:
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
                        bestc = clist[0]
                        bestclen = len(g.nodes[bestc][destination])
                        for c in clist:
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
        print(node, g.node[node])
        
###############################################################################
#   Second rev - get peer routes as well
###############################################################################
#testing to add peer routes, after all provider routes have been traversed 
def build_node_attributes_4(g, destination):
    toexplore = deque()
    toexplore.append(destination)
    peerexplore = deque()
    expdone = []
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
                        bestc = clist[0]
                        bestclen = len(g.nodes[bestc][destination])
                        for c in clist:
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
        
        expdone.append(node)
        toexplore.popleft()
        
    while peerexplore:
        node = peerexplore[0]
        #get list of all peers who have a route to the destination
        #TODO: what to do if multiple peers have a route to the destination? pick randomly? 
        peerlist = get_peers(g,node)
        compare_p = []
        for p in peerlist:
            if destination in g.nodes[p].keys():
                compare_p.append(p)
        if len(compare_p)>1:
            #if multiple peers have the destination then what do we do? 
            pass
        else:
            #add the destination only if the destination does not exist already or the new one is shorter 
            if destination in g.nodes[node].keys():
                #if already present then when must we actually change it? 
                pass 
            else:
                bestp = compare_p[0]
                aslist = g.nodes[bestp][destination].copy()
                aslist.append(bestp)
                g.nodes[node][destination] = aslist
        
        #do push to customer if customer is not there --- 
        peerexplore.popleft()
    
#write the logic for choosing customer over peer over provider 
#there can be no duplicate routes, if a customer route exists, that route is present
        #peer routes are only added if a customer route is not present 
        #provider routes will be added only if a customer and a peer route is not present. 

###############################################################################
#   Third revision - after peer, send it to your customer. 
###############################################################################
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
#            print()
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
#    expdone = []
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
                        bestc = clist[0]
                        bestclen = len(g.nodes[bestc][destination])
                        for c in clist:
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
        
#        expdone.append(node)
        toexplore.popleft()
    
#    print(peerexplore)
    
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
            if len(compare_p)>1:
                #if multiple peers have the destination then what do we do? 
                pass
            else:
                bestp = compare_p[0]
                aslist = g.nodes[bestp][destination].copy()
                aslist.append(bestp)
                g.nodes[node][destination] = aslist
        
            #do push to customer if customer is not there --- 
            #call the function that is going to do it. 
            build_node_pr2c(g,node, destination)
        
        peerexplore.popleft()
    
'''
Node attributes should be built for every single customer AS
'''
build_node_attributes_5(g,1)
build_node_attributes_5(g,10)
build_node_attributes_5(g,11)
for i in range(1,13):
    print(i, g.node[i])

#it works?? Test with other graphs! 
#check this later 
    
#selection of the path 
#source, destination = random.sample(g.nodes().keys(), 2)
#f = (key for key, vals in g.nodes[5].items() if 2 in vals)
#print(list(f))
# i dont have to do this because I can literally build a path for every destination that I have chosen. 
    
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
                    pass
            
            elif options == 0:
                providers = get_providers(g,source)
                different_paths = []
                for p in providers: 
                    different_paths.append(build_path(g,p,destination))
#                print('source',source, different_paths)
                best_path = min(different_paths, key=len) 
                path.extend(best_path)
            
    return path
print(build_path(g, 4, 10))

'''
            elif options == 0:
            providers = get_providers(g, source)
            #this random choice will give longer paths - eliminate, find all paths, and pick the shortest one 
            chosen_p = random.choice(providers)
            if chosen_p not in path:
                path.append(chosen_p)
            source = chosen_p
'''   