"""
Framework for experimentation of multi-objective and dynamic falsification.

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
Runs all experiments in a directory.
"""
def run_experiments(path, rulebook=None, parallel=False, model=None,
                   sampler_type=None, headless=False, num_workers=5, output_dir='outputs',
                   experiment_name=None, max_time=None, n_iters=None, max_steps=300):
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
        falsifier = run_experiment(p, rulebook=rulebook, 
        parallel=parallel, model=model, sampler_type=sampler_type, headless=headless,
        num_workers=num_workers, max_time=max_time, n_iters=n_iters, max_steps=max_steps)
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
        print(f'(multi.py) Saving output to {outpath}')
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
def run_experiment(scenic_path, rulebook=None, parallel=False, model=None,
                   sampler_type=None, headless=False, num_workers=5, max_time=None,
                   n_iters=5, max_steps=300):
    # Construct rulebook
    rb = rulebook

    # Construct sampler (scenic_sampler.py)
    print(f'(multi.py) Running Scenic script {scenic_path}')
    params = {'verifaiSamplerType': sampler_type} if sampler_type else {}
    params['render'] = not headless
    params['seed'] = 0
    sampler = ScenicSampler.fromScenario(scenic_path, maxIterations=40000, params=params, model=model)
    num_objectives = sampler.scenario.params.get('N', 1)
    s_type = sampler.scenario.params.get('verifaiSamplerType', None)
    print(f'(multi.py) num_objectives: {num_objectives}')

    # Construct falsifier (falsifier.py)
    multi = num_objectives > 1
    falsifier_params = DotMap(
        n_iters=n_iters,
        save_error_table=True,
        save_safe_table=True,
        max_time=max_time,
        verbosity=1,
    )
    server_options = DotMap(maxSteps=max_steps, verbosity=1,
                            scenic_path=scenic_path, scenario_params=params, scenario_model=model,
                            num_workers=num_workers)
    falsifier_class = generic_parallel_falsifier if parallel else generic_falsifier
    falsifier = falsifier_class(monitor=rb, ## modified
                                sampler_type=s_type, 
                                sampler=sampler, 
                                falsifier_params=falsifier_params,
                                server_options=server_options,
                                server_class=ScenicServer)
    print(f'(multi.py) sampler_type: {falsifier.sampler_type}')
    
    # Run falsification
    t0 = time.time()
    print('(multi.py) Running falsifier')
    falsifier.run_falsifier()
    t = time.time() - t0
    print()
    print(f'(multi.py) Generated {len(falsifier.samples)} samples in {t} seconds with {falsifier.num_workers} workers')
    print(f'(multi.py) Number of counterexamples: {len(falsifier.error_table.table)}')
    if not parallel:
        print(f'(multi.py) Sampling time: {falsifier.total_sample_time}')
        print(f'(multi.py) Simulation time: {falsifier.total_simulate_time}')
    print(f'(multi.py) Confidence interval: {falsifier.get_confidence_interval()}')
    return falsifier

if __name__ == '__main__':
    pass
