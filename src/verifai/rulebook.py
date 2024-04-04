from abc import ABC
import networkx as nx
import mtl
import ast
import numpy as np
import os

from verifai.monitor import specification_monitor

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node)

class rulebook(ABC):
    priority_graphs = {}
    verbosity = 1
    
    def __init__(self, graph_path, rule_file, single_graph=False):
        print('(rulebook.py) Parsing rules...')
        self._parse_rules(rule_file)
        print('(rulebook.py) Parsing rulebook...')
        if single_graph:
            self._parse_rulebook(graph_path)
        else:
            self._parse_rulebooks(graph_path)
        self.single_graph = single_graph

    def _parse_rules(self, file_path):
        # Parse the input rules (*_spec.py)
        with open(file_path, 'r') as file:
            file_contents = file.read()

        tree = ast.parse(file_contents)

        function_visitor = FunctionVisitor()
        function_visitor.visit(tree)

        self.functions = {}
        for function_node in function_visitor.functions:
            function_name = function_node.name
            function_code = compile(ast.Module(body=[function_node], type_ignores=[]), '<string>', 'exec')
            exec(function_code)
            self.functions[function_name] = locals()[function_name]

        print(f'Parsed functions: {self.functions}')

    def _parse_rulebooks(self, dir):
        if os.path.isdir(dir):
            for root, _, files in os.walk(dir):
                for name in files:
                    fname = os.path.join(root, name)
                    if os.path.splitext(fname)[1] == '.graph':
                        self._parse_rulebook(fname)

    def _parse_rulebook(self, file):
        # TODO: parse the input rulebook
        # 1. construct the priority_graph
        # 2. construct a dictionary mapping from each node_id to corresponding rule object
        priority_graph = nx.DiGraph()
        graph_id = -1
        with open(file, 'r') as f:
            lines = f.readlines()
            node_section = False
            edge_section = False
            for line in lines:
                line = line.strip()
                if line.startswith('# ID'):
                    graph_id = int(line.split(' ')[-1])
                    if self.verbosity >= 1:
                        print(f'Parsing graph {graph_id}')
                if line == '# Node list':
                    node_section = True
                    continue
                elif line == '# Edge list':
                    node_section = False
                    edge_section = True
                    continue
                
                # Node
                if node_section:
                    node_info = line.split(' ')
                    node_id = int(node_info[0])
                    node_active = True if node_info[1] == 'on' else False
                    rule_name = node_info[2]
                    rule_type = node_info[3]
                    if rule_type == 'monitor':
                        ru = rule(node_id, self.functions[rule_name], rule_type)
                        priority_graph.add_node(node_id, rule=ru, active=node_active, name=rule_name)
                        if self.verbosity >= 2:
                            print(f'Add node {node_id} with rule {rule_name}')
                    #TODO: mtl type
                
                # Edge
                if edge_section:
                    edge_info = line.split(' ')
                    src = int(edge_info[0])
                    dst = int(edge_info[1])
                    priority_graph.add_edge(src, dst)
                    if self.verbosity >= 2:
                        print(f'Add edge from {src} to {dst}')

                # TODO: process the graph, e.g., merge the same level nodes
                
        self.priority_graphs[graph_id] = priority_graph

    def evaluate(self, traj):
        raise NotImplementedError('evaluate() is not implemented')

    def update_graph(self):
        pass

class rule(specification_monitor):
    def __init__(self, node_id, spec, spec_type='monitor'):
        self.node_id = node_id
        if spec_type == 'monitor': # spec is a function
            super().__init__(spec)
        else: # spec is MTL
            mtl_specs = [mtl.parse(sp) for sp in spec]
            mtl_spec = mtl_specs[0]
            if len(mtl_specs) > 1:
                for sp in mtl_specs[1:]:
                    mtl_spec = (mtl_spec & sp)
            super().__init__(mtl_spec)
    
    def evaluate(self, traj, start_idx=0, end_idx=None):
        if end_idx is None:
            end_idx = len(traj.result.trajectory)
        return self.specification(traj, start_idx, end_idx)
