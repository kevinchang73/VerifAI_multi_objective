from benchmark import *
param map = localPath('../../multi_objective/maps/Town03.xodr')
param carla_map = 'Town03'
model scenic.domains.driving.model
max_steps = globalParameters['max_steps']

behavior simple():
    take SetThrottleAction(throttle=0.8)



ego = new Car with behavior benchmark(simple, network, max_steps)

adv = new Car ahead of ego by 10

ped = new Pedestrian visible