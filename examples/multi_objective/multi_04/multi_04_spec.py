import numpy as np

def rule0(simulation, indices): # A, 1: safe distance to ped
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_ped = positions[indices, [0], :] - positions[indices, [5], :]
    distances_to_ped = np.linalg.norm(distances_to_ped, axis=1)
    rho = np.min(distances_to_ped, axis=0) - 8
    return rho

def rule1(simulation, indices): # B, 1: safe distance to adv1
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv = positions[indices, [0], :] - positions[indices, [1], :]
    distances_to_adv = np.linalg.norm(distances_to_adv, axis=1)
    rho = np.min(distances_to_adv, axis=0) - 8
    return rho

def rule2(simulation, indices): # B, 2: safe distance to adv2
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv = positions[indices, [0], :] - positions[indices, [2], :]
    distances_to_adv = np.linalg.norm(distances_to_adv, axis=1)
    rho = np.min(distances_to_adv, axis=0) - 8
    return rho

def rule3(simulation, indices): # B, 3: safe distance to adv3
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv = positions[indices, [0], :] - positions[indices, [3], :]
    distances_to_adv = np.linalg.norm(distances_to_adv, axis=1)
    rho = np.min(distances_to_adv, axis=0) - 8
    return rho

def rule4(simulation, indices): # B, 4: safe distance to adv4
    if indices.size == 0:
        return 1
    positions = np.array(simulation.result.trajectory)
    distances_to_adv = positions[indices, [0], :] - positions[indices, [4], :]
    distances_to_adv = np.linalg.norm(distances_to_adv, axis=1)
    rho = np.min(distances_to_adv, axis=0) - 8
    return rho

def rule5(simulation, indices): # C: stay in drivable area
    if indices.size == 0:
        return 1
    distance_to_drivable = np.array(simulation.result.records["egoDistToDrivableRegion"])
    rho = -np.max(distance_to_drivable[indices], axis=0)[1]
    return rho

def rule6(simulation, indices): # D, 1: stay in the correct side of the road, before intersection
    if indices.size == 0:
        return 1
    distance_to_lane_group = np.array(simulation.result.records["egoDistToEgoInitLane"])
    rho = -np.max(distance_to_lane_group[indices], axis=0)[1]
    return rho

def rule7(simulation, indices): # D, 2: stay in the correct side of the road, after intersection
    if indices.size == 0:
        return 1
    distance_to_lane_group = np.array(simulation.result.records["egoDistToEgoEndLane"])
    rho = -np.max(distance_to_lane_group[indices], axis=0)[1]
    return rho

def rule8(simulation, indices): # F: lane keeping
    if indices.size == 0:
        return 1
    distance_to_lane_center = np.array(simulation.result.records["egoDistToEgoLaneCenterline"])
    rho = 0.4 - np.max(distance_to_lane_center[indices], axis=0)[1]
    return rho

def rule9(simulation, indices): # H, 1: reach intersection
    if indices.size == 0:
        return 1
    if max(indices) < len(simulation.result.trajectory) - 1:
        return 1
    ego_dist_to_intersection = np.array(simulation.result.records["egoDistToIntersection"])
    rho = -np.min(ego_dist_to_intersection[indices], axis=0)[1]
    return rho

def rule10(simulation, indices): # H, 2: finish right-turn
    if indices.size == 0:
        return 1
    if max(indices) < len(simulation.result.trajectory) - 1:
        return 1
    ego_dist_to_end_lane = np.array(simulation.result.records["egoDistToEgoEndLane"])
    rho = -np.min(ego_dist_to_end_lane[indices], axis=0)[1]
    return rho