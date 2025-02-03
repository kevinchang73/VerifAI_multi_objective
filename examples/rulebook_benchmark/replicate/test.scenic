param map = localPath('../../multi_objective/maps/Town01.xodr')
param carla_map = 'Town01'
model scenic.simulators.carla.model


behavior simple():
    while True:
        take SetThrottleAction(0.8)

behavior do_nothing():
    while True:
        wait

 
ego = new Car with behavior simple()
adv = new Car with behavior do_nothing(), ahead of ego by 5


#import bench2