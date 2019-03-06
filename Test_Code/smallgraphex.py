#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:34:20 2019

@author: pracheta
"""

import networkx as nx
from collections import defaultdict

g = nx.DiGraph()
g.add_edge(1, 4, rel=1)
g.add_edge(4,1,rel=-1)
g.add_edge(2,4,rel=1)
g.add_edge(4,2,rel=-1)
g.add_edge(4,7,rel=1)
g.add_edge(4,8,rel=1)
g.add_edge(8,4,rel=-1)
g.add_edge(7,4,rel=-1)
g.add_edge(7,8,rel=0)
g.add_edge(8,7,rel=0)
nx.draw(g, with_labels=True)

#function to find the "Customer only" nodes in the graph
def customer_only():
    c_only = []
    for i in g.adjacency():
        node = i[0]
        neighbor = i[1]
        all_rel = []
        list1 = list(neighbor)
        for j in list1:
            all_rel.append(neighbor[j]['rel'])
        if -1 not in all_rel:
            c_only.append(node)
    
    print(c_only)
        
def traverse_from(g,node):
    return g.__getitem__(node)
    
def find_frontier(g,s):
    full_frontier = defaultdict(list)
    remaining_nodes = list()
    
    remaining_nodes.append(s)
    while(len(remaining_nodes)!=0):
        neigh = traverse_from(g,s)
        for n in neigh:
            if(neigh[n]['rel']==1):
                if(n not in full_frontier[s]):
                    full_frontier[s].append(n)
                remaining_nodes.append(n)
        remaining_nodes.remove(s)
        if(len(remaining_nodes)!=0):
            s = remaining_nodes[0]
        else:
            break
     
    
    return full_frontier

def find_valley_path(g,s):
    #find source frontier, print individual ases in the frontier
    source_frontier = find_frontier(g,s)
    source_as = list()
    for i in source_frontier:
        if(i not in source_as):
            source_as.append(i)
        for j in source_frontier[i]:
            if(j not in source_as):
                source_as.append(j)
    print(source_as)
pr_1 = find_frontier(g,1)
find_valley_path(g,1)
print(dict(pr_1))
pr_2 = find_frontier(g,2)
print(dict(pr_2))