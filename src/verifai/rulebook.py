from abc import ABC
import networkx as nx
import mtl
import ast
import numpy as np

from verifai.monitor import specification_monitor

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node)

class rulebook(ABC):
    priority_graph = nx.DiGraph()

    """
    ### temporary workaround start ###
    def __init__(self, graph):
        self.set_graph(graph)

    @classmethod
    def set_graph(cls, graph):
        cls.priority_graph = graph
        print(f'Set priority graph =', cls.priority_graph)
    ### temporary workaround end ###
    """
        
    def __init__(self, graph_file, rule_file):
        print('(rulebook.py) Parsing rules...')
        self._parse_rules(rule_file)
        print('(rulebook.py) Parsing rulebook...')
        self._parse_rulebook(graph_file)

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

    def _parse_rulebook(self, file):
        # TODO: parse the input rulebook
        # 1. construct the priority_graph
        # 2. construct a dictionary mapping from each node_id to corresponding rule object
        self.priority_graph.clear()
        with open(file, 'r') as f:
            lines = f.readlines()
            node_section = False
            edge_section = False
            update_section = False
            for line in lines:
                line = line.strip()
                if line == '## Node list':
                    node_section = True
                    continue
                elif line == '## Edge list':
                    node_section = False
                    edge_section = True
                    continue
                elif line == '# Graph update':
                    edge_section = False
                    update_section = True
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
                        self.priority_graph.add_node(node_id, rule=ru, active=node_active, name=rule_name)
                        print(f'Add node {node_id} with rule {rule_name}')
                    #TODO: mtl type
                
                # Edge
                if edge_section:
                    edge_info = line.split(' ')
                    src = int(edge_info[0])
                    dst = int(edge_info[1])
                    self.priority_graph.add_edge(src, dst)
                    print(f'Add edge from {src} to {dst}')

                # TODO: process the graph, e.g., merge the same level nodes

                # Graph update
                if update_section:
                    graph_update = line.split(' ')
                    #TODO: update the graph
        

    def evaluate(self, traj):
        # TODO:
        # 1. Use rule.evaluate() to evaluate the result of each rule
        # 2. Use update_graph() to update the structure of priority_graph
        # Return a vector of vectors
        rho = np.ones(len(self.priority_graph.nodes))
        idx = 0
        for id in self.priority_graph.nodes:
            rule = self.priority_graph.nodes[id]['rule']
            if self.priority_graph.nodes[id]['active']:
                rho[idx] = rule.evaluate(traj)
            else:
                rho[idx] = 1
            idx += 1
        return rho

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
    
    def evaluate(self, traj):
        return self.specification(traj)
