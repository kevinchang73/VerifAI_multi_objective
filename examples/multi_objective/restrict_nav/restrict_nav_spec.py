import numpy as np

def rule0(simulation, indices):
    """
    reaching destination
    F(dist(ego, goal) < desired_dist)
    """
    if indices.size == 0:
        return 1
    desired_dist = 0.5
    dist_to_goal = np.array(simulation.result.records['dist_to_goal'])[:, 1][indices]
    rho = desired_dist - np.abs(np.min(dist_to_goal)) 
    return rho

def rule1(simulation, indices):
    """
    safe distance
    G(dist(ego, table) > d_safe)
    """
    if indices.size == 0:
        return 1
    ego_too_close = np.array(simulation.result.records['ego_too_close'])[:, 1][indices]
    overalap = np.max(ego_too_close)
    return -1 * overlap


def rule2(simulation, indices):
    """
    don't go thorugh restricted area
    G(Not in restricted area)
    """
    if indices.size == 0:
        return 1
    trespass = np.array(simulation.result.records['trespass'])[:, 1][indices]

    if np.any(trespass):
        return -1
    else:
        return 1

