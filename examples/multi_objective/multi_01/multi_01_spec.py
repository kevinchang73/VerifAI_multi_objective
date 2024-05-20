import numpy as np

def rule0(simulation, indices): # safe distance to obstacle
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv1 = positions[indices, [0], :] - positions[indices, [1], :]
    distances_to_adv1 = np.linalg.norm(distances_to_adv1, axis=1)
    rho = np.min(distances_to_adv1, axis=0) - 3
    return rho

def rule1(simulation, indices): # ego is in the left lane
    if indices.size == 0:
        return 1
    ego_is_in_left_lane = np.array(simulation.result.records["egoIsInLeftLane"], dtype=bool)
    for i in indices:
        if ego_is_in_left_lane[i][1]:
            return -1
    return 1