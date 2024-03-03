"""
Framework for experimentation of parallel and multi-objective falsification.
Scenario: multi_03.scenic

Author: Kai-Chun Chang. Based on Kesav Viswanadha's code.
"""

import time
import os
import numpy as np
from dotmap import DotMap
import traceback
import argparse
import importlib

from verifai.samplers.scenic_sampler import ScenicSampler
from verifai.scenic_server import ScenicServer
from verifai.falsifier import generic_falsifier, generic_parallel_falsifier
from verifai.monitor import multi_objective_monitor, specification_monitor
from verifai.rulebook import rulebook

import networkx as nx
import pandas as pd

def announce(message):
    lines = message.split('\n')
    size = max([len(p) for p in lines]) + 4
    def pad(line):
        ret = '* ' + line
        ret += ' ' * (size - len(ret) - 1) + '*'
        return ret
    lines = list(map(pad, lines))
    m = '\n'.join(lines)
    border = '*' * size
    print(border)
    print(m)
    print(border)

"""
Example of multi-objective specification. This monitor specifies that the ego vehicle
must stay at least 5 meters away from each other vehicle in the scenario.
"""
class distance_multi(multi_objective_monitor):
    def __init__(self, num_objectives=1, to_print=False):
        self.num_objectives = num_objectives
        self.to_print = to_print
        # TODO: rulebook initialization process
        priority_graph = nx.DiGraph(edge_removal=True)
        priority_graph.add_edge(0, 1)
        priority_graph.add_edge(1, 2)
        rb = rulebook(priority_graph)
        assert(self.num_objectives == priority_graph.number_of_nodes()) # for static rulebook
        print(f'Initialized priority graph with {self.num_objectives} objectives')
        def specification(simulation):
            positions = np.array(simulation.result.trajectory)
            distances_to_adv1 = positions[:, [0], :] - positions[:, [1], :]
            distances_to_adv1 = np.linalg.norm(distances_to_adv1, axis=2) # compute the distance based on differences on x and y coordinates
            distances_to_adv2 = positions[:, [0], :] - positions[:, [2], :]
            distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=2)
            distances_to_adv3 = positions[:, [0], :] - positions[:, [3], :]
            distances_to_adv3 = np.linalg.norm(distances_to_adv3, axis=2)
            actions = np.array(simulation.result.actions)
            egotointersection = np.array(simulation.result.records["egotointersection"])
            # In every timestep, the distance between the ego and each adversary vehicle should be larger than 5
            if self.to_print:
                adv1_falsify = False
                adv2_falsify = False
                adv3_falsify = False
                #print(positions.shape)
                #print(actions.shape)
                for t in range(len(positions)):
                    #print(t, distances_to_adv1[t][0], distances_to_adv2[t][0], distances_to_adv3[t][0], egotointersection[t][1], distances_to_adv1[t][0] < 5, distances_to_adv2[t][0] < 5, distances_to_adv3[t][0] < 5)
                    if distances_to_adv1[t][0] < 5:
                        adv1_falsify = True
                    if distances_to_adv2[t][0] < 5:
                        adv2_falsify = True
                    if distances_to_adv3[t][0] < 5:
                        adv3_falsify = True
                    #print(t, positions[t][0][0], positions[t][0][1], positions[t][1][0], positions[t][1][1], positions[t][2][0], positions[t][2][1], positions[t][3][0], positions[t][3][1], distances_to_adv1[t][0], distances_to_adv2[t][0], distances_to_adv3[t][0])
                print("Result =", adv1_falsify, adv2_falsify, adv3_falsify)
            rho = np.concatenate((np.min(distances_to_adv1, axis=0) - 5, np.min(distances_to_adv2, axis=0) - 5, np.min(distances_to_adv3, axis=0) - 5), axis=0)
            return rho
        
        super().__init__(specification, priority_graph=rb.priority_graph, linearize=False)

"""
Single-objective specification. This monitor is similar to the one above, but takes a
minimum over the distances from each vehicle. If the ego vehicle is less than 5 meters
away from any vehicle at any point, a counterexample is returned.
"""
class distance(specification_monitor):
    def __init__(self):
        def specification(simulation):
            positions = np.array(simulation.result.trajectory)
            distances = positions[:, [0], :] - positions[:, 1:, :]
            distances = np.linalg.norm(distances, axis=2)
            rho = np.min(distances) - 5
            return rho
        
        super().__init__(specification)

"""
Runs all experiments in a directory.
"""
def run_experiments(path, parallel=False, model=None,
                   sampler_type=None, headless=False, num_workers=5, output_dir='outputs',
                   experiment_name=None, max_time=None, n_iters=None):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    paths = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for name in files:
                fname = os.path.join(root, name)
                if os.path.splitext(fname)[1] == '.scenic':
                    paths.append(fname)
    else:
        paths = [path]
    for p in paths:
        falsifier = run_experiment(p, parallel=parallel,
        model=model, sampler_type=sampler_type, headless=headless,
        num_workers=num_workers, max_time=max_time, n_iters=n_iters)
        df = pd.concat([falsifier.error_table.table, falsifier.safe_table.table])
        if experiment_name is not None:
            outfile = experiment_name
        else:
            root, _ = os.path.splitext(p)
            outfile = root.split('/')[-1]
            if parallel:
                outfile += '_parallel'
            if model:
                outfile += f'_{model}'
            if sampler_type:
                outfile += f'_{sampler_type}'
        outfile += '.csv'
        outpath = os.path.join(output_dir, outfile)
        announce(f'SAVING OUTPUT TO {outpath}')
        df.to_csv(outpath)

"""
Runs a single falsification experiment.

Arguments:
    path: Path to Scenic script to be run.
    parallel: Whether or not to enable parallelism.
    model: Which simulator model to use (e.g. scenic.simulators.newtonian.driving_model)
    sampler_type: Which VerifAI sampelr to use (e.g. halton, scenic, ce, mab, etc.)
    headless: Whether or not to display each simulation.
    num_workers: Number of parallel workers. Only used if parallel is true.
"""
def run_experiment(path, parallel=False, model=None,
                   sampler_type=None, headless=False, num_workers=5, max_time=None,
                   n_iters=5):
    # Construct rulebook
    monitor = distance_multi(3, True) # TODO: generalize

    # Construct sampler (scenic_sampler.py)
    announce(f'RUNNING SCENIC SCRIPT {path}')
    params = {'verifaiSamplerType': sampler_type} if sampler_type else {}
    params['render'] = not headless
    sampler = ScenicSampler.fromScenario(path, maxIterations=10000, params=params, model=model)
    num_objectives = sampler.scenario.params.get('N', 1)
    s_type = sampler.scenario.params.get('verifaiSamplerType', None)
    announce(f'num_objectives: {num_objectives}, sampler_type: {s_type}')

    # Construct falsifier (falsifier.py)
    multi = num_objectives > 1
    falsifier_params = DotMap(
        n_iters=n_iters,
        save_error_table=True,
        save_safe_table=True,
        max_time=max_time,
        verbosity=1,
    )
    server_options = DotMap(maxSteps=300, verbosity=1,
                            scenic_path=path, scenario_params=params, scenario_model=model,
                            num_workers=num_workers)
    falsifier_class = generic_parallel_falsifier if parallel else generic_falsifier
    falsifier = falsifier_class(monitor=monitor,
                                sampler_type=s_type, 
                                sampler=sampler, 
                                falsifier_params=falsifier_params,
                                server_options=server_options,
                                server_class=ScenicServer)
    announce(f'sampler_type: {falsifier.sampler_type}')
    
    # Run falsification
    t0 = time.time()
    print('Running falsifier')
    falsifier.run_falsifier()
    t = time.time() - t0
    print()
    print(f'Generated {len(falsifier.samples)} samples in {t} seconds with {falsifier.num_workers} workers')
    print(f'Number of counterexamples: {len(falsifier.error_table.table)}')
    if not parallel:
        print(f'Sampling time: {falsifier.total_sample_time}')
        print(f'Simulation time: {falsifier.total_simulate_time}')
    print(f'Confidence interval: {falsifier.get_confidence_interval()}')
    return falsifier

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', type=str, default='uberCrashNewton.scenic',
    help='Path to Scenic script')
    parser.add_argument('--parallel', action='store_true')
    parser.add_argument('--num-workers', type=int, default=5, help='Number of parallel workers')
    parser.add_argument('--sampler-type', '-s', type=str, default=None,
    help='verifaiSamplerType to use')
    parser.add_argument('--experiment-name', '-e', type=str, default=None,
    help='verifaiSamplerType to use')
    parser.add_argument('--model', '-m', type=str, default='scenic.simulators.newtonian.driving_model')
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--n-iters', '-n', type=int, default=None, help='Number of simulations to run')
    parser.add_argument('--max-time', type=int, default=None, help='Maximum amount of time to run simulations')
    args = parser.parse_args()
    if args.n_iters is None and args.max_time is None:
        raise ValueError('At least one of --n-iters or --max-time must be set')
    run_experiments(args.path, args.parallel,model=args.model,
    sampler_type=args.sampler_type, headless=args.headless,
    num_workers=args.num_workers, experiment_name=args.experiment_name,
    max_time=args.max_time, n_iters=args.n_iters)
