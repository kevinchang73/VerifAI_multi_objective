import scenic
from scenic.simulators.carla.simulator import CarlaSimulator
from scenic.syntax.veneer import localPath

MAX_STEPS = 100

realization = {}
realization['max_steps'] = MAX_STEPS



scenario = scenic.scenarioFromFile('test.scenic', params={'use2DMap': True, "realization":realization})
scene, _ = scenario.generate()
print("a")
simulator = CarlaSimulator(carla_map = 'Town01', map_path = localPath('../../multi_objective/maps/Town01.xodr'))
print('b')
simulation = simulator.simulate(scene, maxSteps=100)
