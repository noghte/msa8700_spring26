import networkx as nx

# Example of undirected graph
# G = nx.Graph()
# G.add_edge(1, 2)
# G.add_edge(1, 3)
# G.add_edge(1, 5)
# G.add_edge(2, 3)
# G.add_edge(3, 4)
# G.add_edge(4, 5)

G = nx.DiGraph([(0, 3), (1, 3), (2, 4), (3, 5), (3, 6), (4, 6), (5, 6)])

## PageRank
pr = nx.pagerank(G)
print(pr)

## Degree Centrality
deg = nx.degree_centrality(G)
print(deg)

## 