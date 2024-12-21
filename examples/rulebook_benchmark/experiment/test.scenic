param map = localPath('../../multi_objective/maps/Town03.xodr')
param carla_map = 'Town03'
model scenic.simulators.carla.model


behavior simple():
    take SetThrottleAction(0.8)

 
ego = new Car with behavior FollowLaneBehavior()
adv = new Car ahead of ego by 5

import bench