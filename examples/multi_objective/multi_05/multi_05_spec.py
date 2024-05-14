import numpy as np

def ruleA01(simulation, indices): # A, 0, 1: safe distance from v0 to v1
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances = positions[indices, [0], :] - positions[indices, [1], :]
    distances = np.linalg.norm(distances, axis=1)
    rho = np.min(distances, axis=0) - 8
    return rho

def ruleA02(simulation, indices): # A, 0, 2: safe distance from v0 to v2
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances = positions[indices, [0], :] - positions[indices, [2], :]
    distances = np.linalg.norm(distances, axis=1)
    rho = np.min(distances, axis=0) - 8
    return rho

def ruleA03(simulation, indices): # A, 0, 3: safe distance from v0 to v3
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances = positions[indices, [0], :] - positions[indices, [3], :]
    distances = np.linalg.norm(distances, axis=1)
    rho = np.min(distances, axis=0) - 8
    return rho

def ruleA12(simulation, indices): # A, 1, 2: safe distance from v1 to v2
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances = positions[indices, [1], :] - positions[indices, [2], :]
    distances = np.linalg.norm(distances, axis=1)
    rho = np.min(distances, axis=0) - 8
    return rho

def ruleA13(simulation, indices): # A, 1, 3: safe distance from v1 to v3
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances = positions[indices, [1], :] - positions[indices, [3], :]
    distances = np.linalg.norm(distances, axis=1)
    rho = np.min(distances, axis=0) - 8
    return rho

def ruleA23(simulation, indices): # A, 2, 3: safe distance from v2 to v3
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances = positions[indices, [2], :] - positions[indices, [3], :]
    distances = np.linalg.norm(distances, axis=1)
    rho = np.min(distances, axis=0) - 8
    return rho

def ruleB0(simulation, indices): # B, 0: v0 successfully passes the intersection
    has_passed = simulation.result.records["hasPassed"]
    if has_passed[0]:
        return 1
    return -1 #TODO

def ruleB1(simulation, indices): # B, 1: v1 successfully passes the intersection
    has_passed = simulation.result.records["hasPassed"]
    if has_passed[1]:
        return 1
    return -1 #TODO

def ruleB2(simulation, indices): # B, 2: v2 successfully passes the intersection
    has_passed = simulation.result.records["hasPassed"]
    if has_passed[2]:
        return 1
    return -1 #TODO

def ruleB3(simulation, indices): # B, 3: v3 successfully passes the intersection
    has_passed = simulation.result.records["hasPassed"]
    if has_passed[3]:
        return 1
    return -1 #TODO

def ruleC0(simulation, indices): # C, 0: the first pair of ordering
    arriving_order = simulation.result.records["arrivingOrder"]
    passing_order = simulation.result.records["passingOrder"]
    idx_0 = 10
    idx_1 = 10
    for i in range(len(passing_order)):
        if passing_order[i] == arriving_order[0]:
            idx_0 = i
        elif passing_order[i] == arriving_order[1]:
            idx_1 = i
    if idx_0 < idx_1:
        return 1
    return -1

def ruleC1(simulation, indices): # C, 1: the second pair of ordering
    arriving_order = simulation.result.records["arrivingOrder"]
    passing_order = simulation.result.records["passingOrder"]
    idx_1 = 10
    idx_2 = 10
    for i in range(len(passing_order)):
        if passing_order[i] == arriving_order[1]:
            idx_1 = i
        elif passing_order[i] == arriving_order[2]:
            idx_2 = i
    if idx_1 < idx_2:
        return 1
    return -1

def ruleC2(simulation, indices): # C, 2: the third pair of ordering
    arriving_order = simulation.result.records["arrivingOrder"]
    passing_order = simulation.result.records["passingOrder"]
    idx_2 = 10
    idx_3 = 10
    for i in range(len(passing_order)):
        if passing_order[i] == arriving_order[2]:
            idx_2 = i
        elif passing_order[i] == arriving_order[3]:
            idx_3 = i
    if idx_2 < idx_3:
        return 1
    return -1