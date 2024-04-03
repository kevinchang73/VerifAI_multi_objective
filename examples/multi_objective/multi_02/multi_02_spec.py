import numpy as np

def rule0(simulation, start_idx=0, end_idx=None): # safe distance to adv1
    assert start_idx != end_idx
    positions = np.array(simulation.result.trajectory)
    distances_to_adv1 = positions[start_idx:end_idx, [0], :] - positions[start_idx:end_idx, [1], :]
    distances_to_adv1 = np.linalg.norm(distances_to_adv1, axis=2)
    rho = np.min(distances_to_adv1, axis=0) - 5
    return rho

def rule1(simulation, start_idx=0, end_idx=None): # reach overtaking distance to adv2
    assert start_idx != end_idx
    positions = np.array(simulation.result.trajectory)
    distances_to_adv2 = positions[start_idx:end_idx, [0], :] - positions[start_idx:end_idx, [2], :]
    distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=2)
    rho = np.max(distances_to_adv2, axis=0) - 10
    if rho < 0:
        return rho
    elif end_idx == len(simulation.result.trajectory): # lane change is not actuallly completed
        return -0.1
    return rho

def rule2(simulation, start_idx=0, end_idx=None): # safe distance to adv2 after lane change
    if start_idx == end_idx:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv2 = positions[start_idx:end_idx, [0], :] - positions[start_idx:end_idx, [2], :]
    distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=2)
    rho = np.min(distances_to_adv2, axis=0) - 5
    return rho

def rule3(simulation, start_idx=0, end_idx=None): # safe distance to adv3
    if start_idx == end_idx:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv3 = positions[start_idx:end_idx, [0], :] - positions[start_idx:end_idx, [3], :]
    distances_to_adv3 = np.linalg.norm(distances_to_adv3, axis=2)
    rho = np.min(distances_to_adv3, axis=0) - 5
    return rho
