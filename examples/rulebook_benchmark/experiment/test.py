import scenic
from scenic.simulators.newtonian import NewtonianSimulator
import numpy as np
import random

MAX_STEPS = 100

realization = {}
realization['max_steps'] = MAX_STEPS



random.seed(0)
scenario = scenic.scenarioFromFile('test.scenic', model="scenic.simulators.newtonian.driving_model", params={'use2DMap': True, 'realization': realization})
scene, _ = scenario.generate()
simulator = NewtonianSimulator()
simulation = simulator.simulate(scene, maxSteps=MAX_STEPS)


print(realization)