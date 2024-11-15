
import scenic
from scenic.simulators.newtonian import NewtonianSimulator
import numpy as np
import random



random.seed(0)
scenario = scenic.scenarioFromFile('experiment.scenic', model="scenic.simulators.newtonian.driving_model", params={'max_steps': 10, 'use2DMap': True})
scene, _ = scenario.generate()
simulator = NewtonianSimulator()
simulation = simulator.simulate(scene, maxSteps = 10)


#print(simulation.result.trajectory)

