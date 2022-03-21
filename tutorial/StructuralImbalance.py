import networkx as nx
import random
problem_node_count = 300
G = nx.random_geometric_graph(problem_node_count, radius=0.0005*problem_node_count)
G.add_edges_from([(u, v, {'sign': random.choice((-1, 1))}) for u, v in G.edges])
from dwave.system import LeapHybridSampler
sampler = LeapHybridSampler()     
import dwave_networkx as dnx
imbalance, bicoloring = dnx.structural_imbalance(G, sampler)    
set1 = int(sum(list(bicoloring.values())))        
print("One set has {} nodes; the other has {} nodes.".format(set1, problem_node_count-set1))  
print("The network has {} frustrated relationships.".format(len(list(imbalance.keys()))))    
