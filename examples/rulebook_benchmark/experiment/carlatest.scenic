param map = localPath('../../multi_objective/maps/Town03.xodr')
param carla_map = 'Town03'
model scenic.simulators.carla.model

ego = new Car with behavior FollowLaneBehavior()