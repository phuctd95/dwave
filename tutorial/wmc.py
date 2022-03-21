
from collections import defaultdict

from dwave.system.samplers import DWaveSampler

from dwave.system.composites import EmbeddingComposite

import dwave.inspector

import networkx as nx



#G = [(a,l,4),(a,d,3),(a,i,4),(i,l,-1),(i,g,3),(i,f,3),(f,g,-1),(f,h,3),(h,g,2),(c,f,2),(e,c,2),(e,b,4),(b,c,2),(b,d,-6),(c,d,-1)]
#G = [(1,10,4),(1,4,3),(1,9,4),(9,10,-1),(9,7,3),(9,6,3),(6,7,-1),(6,8,3),(8,7,2),(3,6,2),(5,3,2),(5,2,4),(2,3,2),(2,4,-6),(3,4,-1)]
G = [(1,2,-7),(1,3,2),(2,3,3)]

Q = defaultdict(int)
for u,v,w in G:
    if u > v:
        k = u
        u = v
        v = u
    Q[(u,v)] = Q[(u,v)] - 2 * w
    Q[(u,u)] = Q[(u,u)] + w
    Q[(v,v)] = Q[(v,v)] + w


chainstrength = 8
numruns = 1000
sampler = EmbeddingComposite(DWaveSampler(solver={'topology__type': 'pegasus'}))
#sampler = EmbeddingComposite(DWaveSampler(solver={'topology__type': 'chimera'}))

sampleset = sampler.sample_qubo(Q, chain_strength=chainstrength, num_reads=numruns)
dwave.inspector.show(sampleset)