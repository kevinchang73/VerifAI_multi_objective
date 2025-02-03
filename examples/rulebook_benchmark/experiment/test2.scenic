param map = localPath('../../multi_objective/maps/Town01.xodr')
param carla_map = 'Town01'
model scenic.simulators.carla.model


behavior simple():
    while True:
        take SetThrottleAction(0.8)

behavior do_nothing():
    while True:
        wait

 
ego = Car with behavior simple()
adv = Car with behavior do_nothing(), ahead of ego by 3