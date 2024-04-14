import numpy as np

def rule0(simulation, indices): # safe distance to adv1
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv1 = positions[indices, [0], :] - positions[indices, [1], :]
    distances_to_adv1 = np.linalg.norm(distances_to_adv1, axis=1)
    rho = np.min(distances_to_adv1, axis=0) - 10
    return rho

def rule1(simulation, indices): # reach overtaking distance to adv2
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv2 = positions[indices, [0], :] - positions[indices, [2], :]
    distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=1)
    rho = np.max(distances_to_adv2, axis=0) - 11
    if rho < 0:
        return rho
    elif np.max(indices) == len(simulation.result.trajectory) - 1: # lane change is not actually completed
        return -0.1
    return rho

def rule2(simulation, indices): # safe distance to adv2 after lane change
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv2 = positions[indices, [0], :] - positions[indices, [2], :]
    distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=1)
    rho = np.min(distances_to_adv2, axis=0) - 10
    return rho

def rule3(simulation, indices): # safe distance to adv3
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv3 = positions[indices, [0], :] - positions[indices, [3], :]
    distances_to_adv3 = np.linalg.norm(distances_to_adv3, axis=1)
    rho = np.min(distances_to_adv3, axis=0) - 10
    return rho
