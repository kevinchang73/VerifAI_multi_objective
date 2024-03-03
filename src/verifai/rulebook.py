from abc import ABC
import networkx as nx
#import dynetx as dn

class rulebook(ABC):
    priority_graph = nx.DiGraph(edge_removal=True)

    def __init__(self, graph):
        # TODO: rulebook initialization process
        self.set_graph(graph)

    @classmethod
    def set_graph(cls, graph):
        cls.priority_graph = graph
        print(f'Set priority graph =', cls.priority_graph)
