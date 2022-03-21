import networkx as nx

graph_nodes = 16
G = nx.random_geometric_graph(n=graph_nodes, radius=.5, dim=2)

from collections import defaultdict
from itertools import combinations

gamma = 60

Q = defaultdict(int)

# Fill in Q matrix
for u, v in G.edges:
    Q[(u,u)] += 1
    Q[(v,v)] += 1
    Q[(u,v)] += -2

for i in G.nodes:
    Q[(i,i)] += gamma*(1-len(G.nodes))

for i, j in combinations(G.nodes, 2):
    Q[(i,j)] += 2*gamma

import numpy as np
from dwave.system import DWaveSampler, EmbeddingComposite

# Import the problem inspector to begin data capture
import dwave.inspector

sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))

num_reads = 1000
sampleset = sampler.sample_qubo(Q, num_reads=num_reads, \
                                label='SDK Examples - Inspector')

dwave.inspector.show(sampleset)