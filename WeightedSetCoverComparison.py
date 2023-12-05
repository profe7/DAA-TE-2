# Diadaptasi dari https://github.com/AndreaRubbi/Set-Cover-problem-solution-Python/blob/master/SetCover.pdf

def SetCoverGreedy(Universe, Subsets, Costs):
    cost = 0
    elements = set(e for s in Subsets for e in s)
    if elements != Universe:
        return None
    covered = set()
    cover = []
    while covered != elements:
        subset = max(Subsets, key=lambda s: len(s - covered)/Costs[Subsets.index(s)])
        cover.append(subset)
        cost += Costs[Subsets.index(subset)]
        covered |= subset
    return (cover, cost)

def covers_universe(tset, universe):
    return set(tset) == set(universe)

def SetCoverBranch(universe, sets, costs):
    subset = [1] * len(sets)
    best_cost = sum(costs)
    best_subset = subset
    i = 2

    while i > 0:
        if i < len(sets):
            cost = 0
            tset = []
            for k in range(i):
                cost += subset[k] * costs[k]
                if subset[k] == 1:
                    tset += sets[k]
            if cost > best_cost:
                subset, i = bypassbranch(subset, i)
            else:
                if covers_universe(tset, universe) and cost < best_cost:
                    best_cost = cost
                    best_subset = subset.copy()
                subset, i = nextvertex(subset, i, len(sets))
        else:
            cost = 0
            fset = []
            for k in range(i):
                cost += subset[k] * costs[k]
                if subset[k] == 1:
                    fset += sets[k]
            if cost < best_cost and set(fset) == set(universe):
                best_cost = cost
                best_subset = subset
            subset, i = nextvertex(subset, i, len(sets))

    return best_cost, best_subset

def bypassbranch(subset, i):
    for j in range(i-1, -1, -1):
        if subset[j] == 0:
            subset[j] = 1
            return subset, j + 1
    return subset, 0

def nextvertex(subset, i, m):
    if i < m:
        subset[i] = 0
        return subset, i + 1
    else:
        for j in range(m-1, -1, -1):
            if subset[j] == 0:
                subset[j] = 1
                return subset, j + 1
    return subset, 0

def executeGreedy(inputs):
    print("Now Executing Greedy Algorithm")
    for universe, sets in inputs:
        costs = [2**len(s) for s in sets]
        start_time = time.time()
        start_mem = memory_usage()[0]
        best_sets, best_cost = SetCoverGreedy(universe, sets, costs)
        end_time = time.time()
        end_mem = memory_usage()[0]
        print(f"Input size: {len(sets)}")
        print(f"Cost: {best_cost}")
        print(f"Time taken: {end_time - start_time} seconds")
        print(f"Memory used: {end_mem - start_mem} MiB")
        print()

def executeBranch(inputs):
    print("Now Executing Branch and Bound Algorithm")
    for universe, sets in inputs:
        costs = [2**len(s) for s in sets]
        start_time = time.time()
        start_mem = memory_usage()[0]
        best_cost, best_subset = SetCoverBranch(universe, sets, costs)
        end_time = time.time()
        end_mem = memory_usage()[0]
        print(f"Input size: {len(sets)}")
        print(f"Cost: {best_cost}")
        print(f"Time taken: {end_time - start_time} seconds")
        print(f"Memory used: {end_mem - start_mem} MiB")
        print()

def generate_unique_sets(universe, num_sets, max_set_size):
    unique_sets = []
    universe_list = list(universe)
    while len(unique_sets) < num_sets:
        subset = set(random.sample(universe_list, k=random.randint(1, max_set_size)))
        if subset not in unique_sets:
            unique_sets.append(subset)
    return unique_sets

def generate_inputs():
    universe_small = set(range(1, 21))
    universe_medium = set(range(1, 201))
    universe_large = set(range(1, 2001))

    small_input = generate_unique_sets(universe_small, 20, 20)
    medium_input = generate_unique_sets(universe_medium, 200, 200)
    large_input = generate_unique_sets(universe_large, 2000, 2000)

    return (universe_small, small_input), (universe_medium, medium_input), (universe_large, large_input)

import random
import time
from memory_profiler import memory_usage

def main():
    random.seed(1)

    universe = set(range(1, 11))
    sets = [set(range(1, 6)), set(range(4, 9)), set(range(7, 11))]
    costs = [2**len(s) for s in sets]
    best_sets, best_cost = SetCoverGreedy(universe, sets, costs)

    assert set.union(*best_sets) == universe, "The covering sets do not cover the universe"
    assert sum(costs[sets.index(set_)] for set_ in best_sets) == best_cost, "The cost is not correctly calculated"
    print(f"Covering sets: {best_sets}")
    print(f"Cost: {best_cost}")
    print("Validity check passed")
    print()

    small_input, medium_input, large_input = generate_inputs()

    inputs = [
        small_input,
        medium_input,
        large_input
    ]

    executeGreedy(inputs)
    executeBranch(inputs)

if __name__ == "__main__":
    main()