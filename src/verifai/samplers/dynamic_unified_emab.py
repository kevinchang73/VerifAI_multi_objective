import numpy as np
import networkx as nx
from itertools import product
from verifai.samplers.domain_sampler import BoxSampler, DiscreteBoxSampler, \
    DomainSampler, SplitSampler
from verifai.samplers.random_sampler import RandomSampler
from verifai.samplers.cross_entropy import DiscreteCrossEntropySampler
from verifai.samplers.multi_objective import MultiObjectiveSampler
from verifai.rulebook import rulebook

class DynamicUnifiedExtendedMultiArmedBanditSampler(DomainSampler):
    def __init__(self, domain, udemab_params):
        print('(dynamic_unified_emab.py) Initializing!!!')
        print('(dynamic_unified_emab.py) udemab_params =', udemab_params)
        super().__init__(domain)
        self.alpha = udemab_params.alpha
        self.thres = udemab_params.thres
        self.cont_buckets = udemab_params.cont.buckets
        self.cont_dist = udemab_params.cont.dist
        self.disc_dist = udemab_params.disc.dist
        self.cont_ce = lambda domain: ContinuousDynamicUnifiedEMABSampler(domain=domain,
                                                     buckets=self.cont_buckets,
                                                     dist=self.cont_dist,
                                                     alpha=self.alpha,
                                                     thres=self.thres)
        self.disc_ce = lambda domain: DiscreteDynamicUnifiedEMABSampler(domain=domain,
                                                   dist=self.disc_dist,
                                                   alpha=self.alpha,
                                                   thres=self.thres)
        partition = (
            (lambda d: d.standardizedDimension > 0, self.cont_ce),
            (lambda d: d.standardizedIntervals, self.disc_ce)
        )
        self.split_sampler = SplitSampler.fromPartition(domain, partition, RandomSampler)

    def getSample(self):
        return self.split_sampler.getSample()
    
    def update(self, sample, info, rhos):
        # Update each sampler based on the corresponding segment
        try:
            iter(rhos)
        except:
            self.split_sampler.update(sample, info, rhos)
            return
        for subsampler in self.split_sampler.samplers:
            if isinstance(subsampler, ContinuousDynamicUnifiedEMABSampler):
                subsampler.set_priority_graphs(rulebook.priority_graphs)
        self.split_sampler.update(sample, info, rhos)

class ContinuousDynamicUnifiedEMABSampler(BoxSampler, MultiObjectiveSampler):
    verbosity = 2

    def __init__(self, domain, alpha, thres,
                 buckets=10, dist=None, restart_every=100):
        super().__init__(domain)
        if isinstance(buckets, int):
            buckets = np.ones(self.dimension) * buckets
        elif len(buckets) > 1:
            assert len(buckets) == self.dimension
        else:
            buckets = np.ones(self.dimension) * buckets[0]
        if dist is not None:
            assert (len(dist) == len(buckets))
        if dist is None:
            dist = np.array([np.ones(int(b))/b for b in buckets])
        self.buckets = buckets # 1*d, each element specifies the number of buckets in that dimension
        self.dist = dist # N*d, ???
        self.alpha = alpha
        self.thres = thres
        self.current_sample = None
        self.counts = np.array([np.ones(int(b)) for b in buckets]) # N*d, T (visit times)
        self.errors = np.array([np.zeros(int(b)) for b in buckets]) # N*d, total times resulting in maximal counterexample
        self.t = 1 # time, used in Q
        self.is_multi = True #False
        self.invalid = np.array([np.zeros(int(b)) for b in buckets]) # N*d, ???
        self.monitor = None
        self.rho_values = []
        self.restart_every = restart_every

    def set_priority_graphs(self, graphs):
        self.priority_graphs = graphs
        for id, graph in self.priority_graphs.items():
            node_ids = list(nx.dfs_preorder_nodes(graph))
            if not sorted(node_ids) == list(range(len(node_ids))):
                raise ValueError('Node IDs should be in order and start from 0')

    def getVector(self):
        return self.generateSample()
    
    def generateSample(self):
        proportions = self.errors / self.counts
        Q = proportions + np.sqrt(2 / self.counts * np.log(self.t))
        # choose the bucket with the highest "goodness" value, breaking ties randomly.
        bucket_samples = np.array([np.random.choice(np.flatnonzero(np.isclose(Q[i], Q[i].max())))
            for i in range(len(self.buckets))])
        self.current_sample = bucket_samples
        ret = tuple(np.random.uniform(bs, bs+1.)/b for b, bs
              in zip(self.buckets, bucket_samples)) # uniform randomly sample from the range of the bucket
        return ret, bucket_samples
    
    def updateVector(self, vector, info, rhos):
        assert rhos is not None
        assert self.is_multi is True
        if self.is_multi:
            self.update_dist_from_multi(vector, info, rhos)
            return
    
    def update_dist_from_multi(self, sample, info, rhos):
        try:
            iter(rhos)
        except:
            for i, b in enumerate(info):
                self.invalid[i][b] += 1.
            return
        if len(rhos) != len(self.priority_graphs):
            for i, b in enumerate(info):
                self.invalid[i][b] += 1.
            return
        
        error_values = []
        for i, rho in enumerate(rhos):
            print('Evaluate segment ', i, ' with rho =', rho)
            assert len(rho) == len(self.priority_graphs[i].nodes)
            print('sorted(self.priority_graphs[i].nodes) =', sorted(self.priority_graphs[i].nodes))
            print('self.thres =', self.thres)
            counter_ex = tuple(rho[node] < self.thres for node in sorted(self.priority_graphs[i].nodes))
            error_value = self._compute_error_value(counter_ex, i)
            print('error_value =', error_value)
            error_values.append(error_value)
        for i, b in enumerate(info):
            self.counts[i][b] += 1
            self.errors[i][b] += sum(error_values) / len(error_values)
        print('average error_value =', sum(error_values) / len(error_values))
        self.t += 1
        if self.verbosity >= 1:
            proportions = self.errors / self.counts
            print('self.errors[0] =', self.errors[0])
            print('self.counts[0] =', self.counts[0])
            Q = proportions + np.sqrt(2 / self.counts * np.log(self.t))
            print('Q[0] =', Q[0], '\nfirst_term[0] =', proportions[0], '\nsecond_term[0] =', np.sqrt(2 / self.counts * np.log(self.t))[0], '\nratio[0] =', proportions[0]/(proportions+np.sqrt(2 / self.counts * np.log(self.t)))[0])

    def _compute_error_value(self, counter_ex, graph_idx=None):
        assert graph_idx is not None
        self.compute_error_weight(graph_idx)
        error_value = 0
        for i in range(len(counter_ex)):
            error_value += 2**(self.error_weight[i]) * counter_ex[i]
        return float(error_value/self.sum_error_weight)
    
    def compute_error_weight(self, graph_idx=None):
        assert graph_idx is not None
        self.priority_graph = self.priority_graphs[graph_idx]

        level = {}
        for node in nx.topological_sort(self.priority_graph):
            if self.priority_graph.in_degree(node) == 0:
                level[node] = 0
            else:
                level[node] = max([level[p] for p in self.priority_graph.predecessors(node)]) + 1
        
        ranking_map = {}
        ranking_count = {}
        for rank in sorted(level.values()):
            if rank not in ranking_count:
                ranking_count[rank] = 1
            else:
                ranking_count[rank] += 1
        count = 0
        for key, value in reversed(ranking_count.items()):
            ranking_map[key] = count
            count += value
        
        self.error_weight = {} #node_id -> weight
        self.sum_error_weight = 0
        for node in level:
            if self.priority_graph.nodes[node]['active']:
                self.error_weight[node] = ranking_map[level[node]]
                self.sum_error_weight += 2**self.error_weight[node]
            else:
                self.error_weight[node] = -1
        for key, value in sorted(self.error_weight.items()):
            if self.verbosity >= 2:
                print(f"Node {key}: {value}")

class DiscreteDynamicUnifiedEMABSampler(DiscreteCrossEntropySampler):
    pass
