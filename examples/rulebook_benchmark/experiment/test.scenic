param map = localPath('../../multi_objective/maps/Town03.xodr')
param carla_map = 'Town03'
model scenic.simulators.carla.model
from bench import *

behavior simple():
    take SetThrottleAction(0.8)


ego = new Car with behavior bench(simple)
adv = new Car ahead of ego by 5
