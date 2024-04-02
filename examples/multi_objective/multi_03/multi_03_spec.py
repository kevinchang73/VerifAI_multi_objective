import numpy as np

def rule0(simulation, start_idx=0, end_idx=None):
    positions = np.array(simulation.result.trajectory)
    distances_to_adv1 = positions[start_idx:end_idx, [0], :] - positions[start_idx:end_idx, [1], :]
    distances_to_adv1 = np.linalg.norm(distances_to_adv1, axis=2)
    rho = np.min(distances_to_adv1, axis=0) - 5
    return rho

def rule1(simulation, start_idx=0, end_idx=None):
    positions = np.array(simulation.result.trajectory)
    distances_to_adv2 = positions[start_idx:end_idx, [0], :] - positions[start_idx:end_idx, [2], :]
    distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=2)
    rho = np.min(distances_to_adv2, axis=0) - 5
    return rho

def rule2(simulation, start_idx=0, end_idx=None):
    positions = np.array(simulation.result.trajectory)
    distances_to_adv3 = positions[start_idx:end_idx, [0], :] - positions[start_idx:end_idx, [3], :]
    distances_to_adv3 = np.linalg.norm(distances_to_adv3, axis=2)
    rho = np.min(distances_to_adv3, axis=0) - 5
    return rho

#rule4 = ["G(speed < 5)"]