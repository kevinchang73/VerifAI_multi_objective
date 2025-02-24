
"""Samplers generating points in a feature space, possibly subject to
specifications.
"""

import random

import dill
from dotmap import DotMap
import numpy as np

from verifai.features import FilteredDomain
from verifai.samplers.domain_sampler import SplitSampler, TerminationException
from verifai.samplers.rejection import RejectionSampler
from verifai.samplers.halton import HaltonSampler
from verifai.samplers.cross_entropy import CrossEntropySampler
from verifai.samplers.random_sampler import RandomSampler
from verifai.samplers.multi_armed_bandit import MultiArmedBanditSampler
from verifai.samplers.eg_sampler import EpsilonGreedySampler
from verifai.samplers.bayesian_optimization import BayesOptSampler
from verifai.samplers.simulated_annealing import SimulatedAnnealingSampler
from verifai.samplers.grid_sampler import GridSampler
from verifai.samplers.extended_multi_armed_bandit import ExtendedMultiArmedBanditSampler
from verifai.samplers.dynamic_emab import DynamicExtendedMultiArmedBanditSampler
from verifai.samplers.dynamic_mab import DynamicMultiArmedBanditSampler
from verifai.samplers.dynamic_ce import DynamicCrossEntropySampler
from verifai.samplers.dynamic_unified_emab import DynamicUnifiedExtendedMultiArmedBanditSampler

### Samplers defined over FeatureSpaces

class FeatureSampler:
    """Abstract class for samplers over FeatureSpaces."""

    def __init__(self, space):
        self.space = space
        self.last_sample = None

    @classmethod
    def samplerFor(cls, space):
        """Convenience function choosing a default sampler for a space."""
        return cls.randomSamplerFor(space)

    @staticmethod
    def randomSamplerFor(space):
        """Creates a random sampler for a given space"""
        return LateFeatureSampler(space, RandomSampler, RandomSampler)

    @staticmethod
    def haltonSamplerFor(space, halton_params=None):
        """Creates a Halton sampler for a given space.

        Uses random sampling for lengths of feature lists and any
        Domains that are not continous and standardizable.
        """
        if halton_params is None:
            halton_params = default_sampler_params('halton')
        def makeDomainSampler(domain):
            return SplitSampler.fromPredicate(
                domain,
                lambda d: d.standardizedDimension > 0,
                lambda domain: HaltonSampler(domain=domain,
                                             halton_params=halton_params),
                makeRandomSampler)
        return LateFeatureSampler(space, RandomSampler, makeDomainSampler)

    @staticmethod
    def crossEntropySamplerFor(space, ce_params=None):
        """Creates a cross-entropy sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable.
        """
        if ce_params is None:
            ce_params = default_sampler_params('ce')
        return LateFeatureSampler(space, RandomSampler,
            lambda domain: CrossEntropySampler(domain=domain,
                                               ce_params=ce_params))

    @staticmethod
    def epsilonGreedySamplerFor(space, eg_params=None):
        """Creates an epsilon-greedy sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable.
        """
        if eg_params is None:
            eg_params = default_sampler_params('eg')
        return LateFeatureSampler(space, RandomSampler,
            lambda domain: EpsilonGreedySampler(domain=domain,
                                                eg_params=eg_params))

    @staticmethod
    def multiArmedBanditSamplerFor(space, mab_params=None):
        """Creates a multi-armed bandit sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable.
        """
        print('(feature_sampler.py) Using mab sampler')
        if mab_params is None:
            mab_params = default_sampler_params('mab')
        print('(feature_sampler.py) mab_params =', mab_params)
        return LateFeatureSampler(space, RandomSampler,
            lambda domain: MultiArmedBanditSampler(domain=domain,
                                                   mab_params=mab_params))

    @staticmethod
    def extendedMultiArmedBanditSamplerFor(space, emab_params=None):
        """Creates an extended multi-armed bandit sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable.
        """
        print('(feature_sampler.py) Using emab sampler')
        if emab_params is None:
            emab_params = default_sampler_params('emab')
        print('(feature_sampler.py) emab_params =', emab_params)
        return LateFeatureSampler(space, RandomSampler,
            lambda domain: ExtendedMultiArmedBanditSampler(domain=domain,
                                                   emab_params=emab_params))
    
    @staticmethod
    def dynamicExtendedMultiArmedBanditSamplerFor(space, demab_params=None):
        """Creates a dynamic extended multi-armed bandit sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable.
        """
        print('(feature_sampler.py) Using demab sampler')
        if demab_params is None:
            demab_params = default_sampler_params('demab')
        print('(feature_sampler.py) demab_params =', demab_params)
        return LateFeatureSampler(space, RandomSampler,
            lambda domain: DynamicExtendedMultiArmedBanditSampler(domain=domain,
                                                                  demab_params=demab_params))
    
    @staticmethod
    def dynamicMultiArmedBanditSamplerFor(space, dmab_params=None):
        """Creates a dynamic multi-armed bandit sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable.
        """
        print('(feature_sampler.py) Using dmab sampler')
        if dmab_params is None:
            dmab_params = default_sampler_params('dmab')
        print('(feature_sampler.py) dmab_params =', dmab_params)
        return LateFeatureSampler(space, RandomSampler,
            lambda domain: DynamicMultiArmedBanditSampler(domain=domain,
                                                          dmab_params=dmab_params))
    
    @staticmethod
    def dynamicCrossEntropySamplerFor(space, dce_params=None):
        """Creates a dynamic cross-entropy sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable.
        """
        print('(feature_sampler.py) Using dce sampler')
        if dce_params is None:
            dce_params = default_sampler_params('dce')
        print('(feature_sampler.py) dce_params =', dce_params)
        return LateFeatureSampler(space, RandomSampler,
            lambda domain: DynamicCrossEntropySampler(domain=domain,
                                                      dce_params=dce_params))

    @staticmethod
    def dynamicUnifiedExtendedMultiArmedBanditSamplerFor(space, udemab_params=None):
        """Creates a dynamic unified extended multi-armed bandit sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable.
        """
        print('(feature_sampler.py) Using udemab sampler')
        if udemab_params is None:
            udemab_params = default_sampler_params('udemab')
        print('(feature_sampler.py) udemab_params =', udemab_params)
        return LateFeatureSampler(space, RandomSampler,
            lambda domain: DynamicUnifiedExtendedMultiArmedBanditSampler(domain=domain,
                                                                         udemab_params=udemab_params))
    
    @staticmethod
    def gridSamplerFor(space, grid_params=None):
        """Creates a grid sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not standardizable."""

        def makeDomainSampler(domain):
            return SplitSampler.fromPredicate(
                domain,
                lambda d: d.isStandardizable,
                lambda domain: GridSampler(domain=domain,
                                           grid_params=grid_params),
                makeRandomSampler)
        return LateFeatureSampler(space, RandomSampler, makeDomainSampler)

    @staticmethod
    def simulatedAnnealingSamplerFor(space, sa_params=None):
        """Creates a cross-entropy sampler for a given space.

        Uses random sampling for lengths of feature lists and any Domains
        that are not continuous and standardizable.
        """
        if sa_params is None:
            sa_params = default_sampler_params('sa')
        def makeDomainSampler(domain):
            return SplitSampler.fromPredicate(
                domain,
                lambda d: d.standardizedDimension > 0,
                lambda domain: SimulatedAnnealingSampler(domain=domain,
                                                         sa_params=sa_params),
                makeRandomSampler)
        return LateFeatureSampler(space, RandomSampler, makeDomainSampler)

    @staticmethod
    def bayesianOptimizationSamplerFor(space, BO_params=None):
        """Creates a Bayesian Optimization sampler for a given space.

        Uses random sampling for lengths of feature lists and any
        Domains that are not continous and standardizable.
        """
        if BO_params is None:
            BO_params = default_sampler_params('bo')
        def makeDomainSampler(domain):
            return SplitSampler.fromPredicate(
                domain,
                lambda d: d.standardizedDimension > 0,
                lambda domain: BayesOptSampler(domain=domain,
                                               BO_params=BO_params),
                makeRandomSampler)
        return LateFeatureSampler(space, RandomSampler, makeDomainSampler)

    def getSample(self):
        """Generate a sample, along with any sampler-specific info.

        Must return a pair consisting of the sample and arbitrary
        sampler-specific info, which will be passed to the `update`
        method after the sample is evaluated.
        """
        raise NotImplementedError('tried to use abstract FeatureSampler')
    
    def update(self, sample, info, rho):
        """Update the state of the sampler after evaluating a sample."""
        pass

    def nextSample(self, feedback=None):
        """Generate the next sample, given feedback from the last sample.

        This function exists only for backwards compatibility. It has been
        superceded by the `getSample` and `update` APIs.
        """
        if self.last_sample is not None:
            self.update(self.last_sample, self.last_info, feedback)
        self.last_sample, self.last_info = self.getSample()
        return self.last_sample

    def set_graph(self, graph):
        self.scenario.set_graph(graph)

    def saveToFile(self, path):
        with open(path, 'wb') as outfile:
            randState = random.getstate()
            numpyRandState = np.random.get_state()
            allState = (randState, numpyRandState, self)
            dill.dump(allState, outfile)

    @staticmethod
    def restoreFromFile(path):
        with open(path, 'rb') as infile:
            allState = dill.load(infile)
            randState, numpyRandState, sampler = allState
            random.setstate(randState)
            np.random.set_state(numpyRandState)
            return sampler

    def __iter__(self):
        try:
            feedback = None
            while True:
                feedback = yield self.nextSample(feedback)
        except TerminationException:
            return

class LateFeatureSampler(FeatureSampler):
    """FeatureSampler that works by first sampling only lengths of feature
    lists, then sampling from the resulting fixed-dimensional Domain.

    e.g. LateFeatureSampler(space, RandomSampler, HaltonSampler) creates a
    FeatureSampler which picks lengths uniformly at random and applies
    Halton sampling to each fixed-length space.
    """

    def __init__(self, space, makeLengthSampler, makeDomainSampler):
        super().__init__(space)
        lengthDomain, fixedDomains = space.domains
        if lengthDomain is None:    # space has no feature lists
            self.lengthSampler = None
            self.domainSampler = makeDomainSampler(fixedDomains)
        else:
            self.lengthDomain = lengthDomain
            self.lengthSampler = makeLengthSampler(lengthDomain)
            self.domainSamplers = {
                point: makeDomainSampler(domain)
                for point, domain in fixedDomains.items()
            }
            self.lastLength = None

    def getSample(self):
        if self.lengthSampler is None:
            domainPoint, info = self.domainSampler.getSample()
        else:
            length, info1 = self.lengthSampler.getSample()
            self.lastLength = length
            domainPoint, info2 = self.domainSamplers[length].getSample()
            info = (info1, info2)
        return self.space.makePoint(*domainPoint), info
    
    def update(self, sample, info, rho):
        if self.lengthSampler is None:
            self.domainSampler.update(sample, info, rho)
        else:
            self.lengthSampler.update(sample, info[0], rho)
            lengths = []
            for name, feature in self.space.namedFeatures:
                if feature.lengthDomain:
                    lengths.append((len(getattr(sample, name)),))
            lengthPoint = self.lengthDomain.makePoint(*lengths)
            self.domainSamplers[lengthPoint].update(sample, info[1], rho)

### Utilities

def makeRandomSampler(domain):
    """Utility function making a random sampler for a domain."""
    sampler = RandomSampler(domain)
    if domain.requiresRejection:
        sampler = RejectionSampler(sampler)
    return sampler

def default_sampler_params(sampler_type):
    if sampler_type == 'halton':
        return DotMap(sample_index=0, bases_skipped=0)
    elif sampler_type in ('ce', 'eg', 'mab', 'emab'):
        cont = DotMap(buckets=5, dist=None)
        disc = DotMap(dist=None)
        return DotMap(alpha=0.9, thres=0.0, cont=cont, disc=disc)
    elif sampler_type in ('demab', 'dmab', 'dce', 'udemab'):
        cont = DotMap(buckets=5, dist=None)
        disc = DotMap(dist=None)
        return DotMap(alpha=0.9, thres=0.0, cont=cont, disc=disc)
    elif sampler_type == 'bo':
        return DotMap(init_num=5)
    return DotMap()
