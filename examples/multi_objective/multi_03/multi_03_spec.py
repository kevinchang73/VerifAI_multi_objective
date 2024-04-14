import numpy as np

def rule0(simulation, indices):
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv1 = positions[indices, [0], :] - positions[indices, [1], :]
    distances_to_adv1 = np.linalg.norm(distances_to_adv1, axis=1)
    rho = np.min(distances_to_adv1, axis=0) - 5
    return rho

def rule1(simulation, indices):
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv2 = positions[indices, [0], :] - positions[indices, [2], :]
    distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=1)
    rho = np.min(distances_to_adv2, axis=0) - 5
    return rho

def rule2(simulation, indices):
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv3 = positions[indices, [0], :] - positions[indices, [3], :]
    distances_to_adv3 = np.linalg.norm(distances_to_adv3, axis=1)
    rho = np.min(distances_to_adv3, axis=0) - 5
    return rho

#rule4 = ["G(speed < 5)"]