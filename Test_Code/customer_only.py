import networkx as nx
#demo graph 1

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

def customer_only():
    c_only = []
    for i in g.adjacency():
        node = i[0]
        neighbor = i[1]
        all_rel = []
        list1 = list(neighbor)
        for j in list1:
            all_rel.append(neighbor[j]['rel'])
        if 1 not in all_rel:
            c_only.append(node)

    return c_only

for i in g.adjacency():
    print(i)
c = customer_only()
print(c)
