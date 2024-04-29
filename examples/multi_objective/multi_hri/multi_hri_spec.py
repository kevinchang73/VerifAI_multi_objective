import numpy as np

def rule0(simulation, indices):
    """
    corresponds to maintaining distance between spot and fetch
    """
    if indices.size == 0:
        return 1

    desired_bot_dist = 0.5

    bot_dist = np.array(simulation.result.records['bot_dist'])[:, 1][indices]
    rho = np.min(0, np.min(bot_dist) - desired_bot_dist)
    return rho 


def rule1(simulation, indices):
    """
    This rule corresponds to the robot staying away from the human's hand
    """
    if indices.size == 0:
        return 1

    desired_dist = 0.2

    dist = np.array(simulation.result.records['ee_dist'])[:, 1][indices]
    rho = np.min(dist) - desired_dist
    return rho

def rule1(simulation, indices):
    """
    This rule corresponds to the robot staying away from the human's hand
    G(dist(bot hand, human hand) > threshold)
    """
    if indices.size == 0:
        return 1

    desired_dist = 0.2

    dist = np.array(simulation.result.records['ee_dist'])[:, 1][indices]
    rho = np.min(dist) - desired_dist
    return rho

def rule2(simulation, indices):
    """
    F(dist(bot hand, human hand) < threshold)
    """
    if indices.size == 0:
        return 1

    desired_dist = 0.2

    dist = np.array(simulation.result.records['ee_dist'])[:, 1][indices]
    rho = desired_dist - np.min(dist)
    return rho


def rule3(simulation, indices):
    """
    F(dist(box, bot hand) < threshold)
    """
    if indices.size == 0:
        return 1
    desired_dist = 0.25
    dist = np.array(simulation.result.records['box_dist'])[:, 1][indices]
    rho = desired_dist - np.min(dist)
    return rho


