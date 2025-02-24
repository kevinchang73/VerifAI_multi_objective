import sys 
import os
sys.path.append(os.path.abspath("."))
import random
import numpy as np

from multi import *
from multi_02_rulebook import rulebook_multi02

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenic-path', '-sp', type=str, default='uberCrashNewton.scenic',
    help='Path to Scenic script')
    parser.add_argument('--graph-path', '-gp', type=str, default=None,
    help='Path to graph file')
    parser.add_argument('--rule-path', '-rp', type=str, default=None,
    help='Path to rule file')
    parser.add_argument('--output-dir', '-o', type=str, default=None,
    help='Directory to save output trajectories')
    parser.add_argument('--output-csv-dir', '-co', type=str, default=None,
    help='Directory to save output error tables (csv files)')
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
    parser.add_argument('--single-graph', action='store_true', help='Only a unified priority graph')
    parser.add_argument('--seed', type=int, default=0, help='Random seed')
    parser.add_argument('--using-sampler', type=int, default=-1, help='Assigning sampler to use')
    parser.add_argument('--exploration-ratio', type=float, default=2.0, help='Exploration ratio')
    parser.add_argument('--use-dependency', action='store_true', help='Use dependency')
    parser.add_argument('--using-continuous', action='store_true', help='Using continuous')
    args = parser.parse_args()
    if args.n_iters is None and args.max_time is None:
        raise ValueError('At least one of --n-iters or --max-time must be set')
    
    random.seed(args.seed)
    np.random.seed(args.seed)
    
    rb = rulebook_multi02(args.graph_path, args.rule_path, save_path=args.output_dir, single_graph=args.single_graph, using_sampler=args.using_sampler, 
                          exploration_ratio=args.exploration_ratio, use_dependency=args.use_dependency, using_continuous=args.using_continuous)
    run_experiments(args.scenic_path, rulebook=rb,
    parallel=args.parallel, model=args.model,
    sampler_type=args.sampler_type, headless=args.headless,
    num_workers=args.num_workers, output_dir=args.output_csv_dir, experiment_name=args.experiment_name,
    max_time=args.max_time, n_iters=args.n_iters)
    