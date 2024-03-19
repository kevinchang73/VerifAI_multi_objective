import numpy as np

def rule0(simulation):
    positions = np.array(simulation.result.trajectory)
    distances_to_adv1 = positions[:, [0], :] - positions[:, [1], :]
    distances_to_adv1 = np.linalg.norm(distances_to_adv1, axis=2)
    rho = np.min(distances_to_adv1, axis=0) - 5
    return rho

def rule1(simulation):
    positions = np.array(simulation.result.trajectory)
    distances_to_adv2 = positions[:, [0], :] - positions[:, [2], :]
    distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=2)
    rho = np.min(distances_to_adv2, axis=0) - 5
    return rho

def rule2(simulation):
    positions = np.array(simulation.result.trajectory)
    distances_to_adv3 = positions[:, [0], :] - positions[:, [3], :]
    distances_to_adv3 = np.linalg.norm(distances_to_adv3, axis=2)
    rho = np.min(distances_to_adv3, axis=0) - 5
    return rho

#rule4 = ["G(speed < 5)"]