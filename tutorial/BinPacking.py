import numpy as np
num_items = 15
item_weight_range = [3, 7]
weights = list(np.random.randint(*item_weight_range, num_items))
bin_capacity = int(10 * np.mean(weights))
rint("Problem: pack a total weight of {} into bins of capacity {}.".format(
		   sum(weights), bin_capacity))              


from dimod import ConstrainedQuadraticModel
cqm = ConstrainedQuadraticModel()
from dimod import Binary
bin_used = [Binary(f'bin_used_{j}') for j in range(num_items)]
cqm.set_objective(sum(bin_used))
item_in_bin = [[Binary(f'item_{i}_in_bin_{j}') for j in range(num_items)]
		      for i in range(num_items)]
for i in range(num_items):
    one_bin_per_item = cqm.add_constraint(sum(item_in_bin[i]) == 1, label=f'item_placing_{i}')
for j in range(num_items):
    bin_up_to_capacity = cqm.add_constraint(
        sum(weights[i] * item_in_bin[i][j] for i in range(num_items)) - bin_used[j] * bin_capacity <= 0,
        label=f'capacity_bin_{j}')
from dwave.system import LeapHybridCQMSampler
sampler = LeapHybridCQMSampler()
sampleset = sampler.sample_cqm(cqm,
                                time_limit=180,
                                label="SDK Examples - Bin Packing")  
feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
if len(feasible_sampleset):      
    best = feasible_sampleset.first
    print("{} feasible solutions of {}.".format(
        len(feasible_sampleset), len(sampleset)))
selected_bins = [key for key, val in best.sample.items() if 'bin_used' in key and val]
print("{} bins are used.".format(len(selected_bins)))