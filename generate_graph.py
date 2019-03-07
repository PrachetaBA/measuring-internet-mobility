#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 23:52:37 2019

@author: pracheta
"""

"""
Program to generate a smaller connected graph of ~2000 nodes from CAIDA dataset
"""
import networkx as nx
import pickle

"""
Function reads from the file, separates by | and builds a graph from the relationships defined
"""
def build_smaller_graph(text_file_name):
    g = nx.DiGraph()
    try:
        f = open(text_file_name,"r")
        for line in f:
            line = line.rstrip('\n')
            a = line.split(sep="|")
            from_node = int(a[0])
            to_node = int(a[1])
            rel = int(a[2])
            if from_node in nodes_new_g and to_node in nodes_new_g:
                if from_node not in g:
                    g.add_node(from_node)
                if to_node not in g:
                    g.add_node(to_node)
                g.add_edge(from_node, to_node, rel=rel)
                if(rel==-1):
                    g.add_edge(to_node, from_node,rel=1)
                if(rel==0):
                    g.add_edge(to_node,from_node,rel=0)

        f.close()
    except IndexError as error:
        print(error)

    return g
"""
Save graph to a pickle file
"""
def save_graph(g,file_name):
    with open(file_name,'wb') as f:
        pickle.dump(g,f,pickle.HIGHEST_PROTOCOL)

"""
Read graph from pickle file
"""
def read_graph(graph_file_name):
    with open(graph_file_name,'rb') as f:
        g = pickle.load(f)
        return g
"""
Depth First Search of the full graph to determine the children nodes
"""
def dfs_tree(source):
    all_children = list(nx.dfs_tree(g,source=source, depth_limit=5))
    return all_children[:700]

"""
Take the entire dataset and build a smaller graph from it
"""
def build_small_graph():
    tree = list()
    for node in clique_nodes:
        tree = dfs_tree(node)
        for each in tree:
            if each not in nodes_new_g:
                nodes_new_g.append(each)
    return nodes_new_g

if __name__ == "__main__":
    """
    Inferred clique from the CAIDA dataset
    """
    clique_nodes = [174,209,286,701,1239,1299,2828,2914,3257,3320,3356,3491,5511,6453,6461,6762,6830,7018,12956]
    #read the full graph and select nodes that form the smaller graph
    g = read_graph('Dataset\BGPDatasetSmall.pickle')
    nodes_new_g = list()
    nodes_new_g = build_small_graph()
    #build new graph to contain connected component
    new_g = nx.DiGraph()
    new_g = build_smaller_graph("Dataset\copy-as-rel.txt")
    #Run to build the graph and save the graph in a pickle file
    save_graph(new_g,'Dataset\BGPGraph.pickle')
    print(len(new_g.nodes()))
