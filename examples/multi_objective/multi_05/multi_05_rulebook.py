import numpy as np

from verifai.rulebook import rulebook

class rulebook_multi05(rulebook):
    iteration = 0

    def __init__(self, graph_path, rule_file, save_path=None, single_graph=False, using_sampler=-1):
        rulebook.using_sampler = using_sampler
        super().__init__(graph_path, rule_file, single_graph=single_graph)
        self.save_path = save_path

    def evaluate(self, simulation):
        # Extract trajectory information
        v0_is_in_intersection = np.array(simulation.result.records["v0IsInIntersection"])
        v0_is_in_intersection = v0_is_in_intersection[:, 1]
        v1_is_in_intersection = np.array(simulation.result.records["v1IsInIntersection"])
        v1_is_in_intersection = v1_is_in_intersection[:, 1]
        v2_is_in_intersection = np.array(simulation.result.records["v2IsInIntersection"])
        v2_is_in_intersection = v2_is_in_intersection[:, 1]
        v3_is_in_intersection = np.array(simulation.result.records["v3IsInIntersection"])
        v3_is_in_intersection = v3_is_in_intersection[:, 1]

        # Find indices for each rule
        indices_A01 = np.where(v0_is_in_intersection & v1_is_in_intersection)[0]
        indices_A02 = np.where(v0_is_in_intersection & v2_is_in_intersection)[0]
        indices_A03 = np.where(v0_is_in_intersection & v3_is_in_intersection)[0]
        indices_A12 = np.where(v1_is_in_intersection & v2_is_in_intersection)[0]
        indices_A13 = np.where(v1_is_in_intersection & v3_is_in_intersection)[0]
        indices_A23 = np.where(v2_is_in_intersection & v3_is_in_intersection)[0]

        # Write trajectory to file for visualization
        
        # Evaluation
        rho_A01 = self.evaluate_rule(simulation, rule_id=0, graph_idx=0, indices=indices_A01)
        rho_A02 = self.evaluate_rule(simulation, rule_id=1, graph_idx=0, indices=indices_A02)
        rho_A03 = self.evaluate_rule(simulation, rule_id=2, graph_idx=0, indices=indices_A03)
        rho_A12 = self.evaluate_rule(simulation, rule_id=3, graph_idx=0, indices=indices_A12)
        rho_A13 = self.evaluate_rule(simulation, rule_id=4, graph_idx=0, indices=indices_A13)
        rho_A23 = self.evaluate_rule(simulation, rule_id=5, graph_idx=0, indices=indices_A23)
        rho_B0 = self.evaluate_rule(simulation, rule_id=6, graph_idx=0)
        rho_B1 = self.evaluate_rule(simulation, rule_id=7, graph_idx=0)
        rho_B2 = self.evaluate_rule(simulation, rule_id=8, graph_idx=0)
        rho_B3 = self.evaluate_rule(simulation, rule_id=9, graph_idx=0)
        rho_C0 = self.evaluate_rule(simulation, rule_id=10, graph_idx=0)
        rho_C1 = self.evaluate_rule(simulation, rule_id=11, graph_idx=0)
        rho_C2 = self.evaluate_rule(simulation, rule_id=12, graph_idx=0)
        rho = np.array([rho_A01, rho_A02, rho_A03, rho_A12, rho_A13, rho_A23, rho_B0, rho_B1, rho_B2, rho_B3, rho_C0, rho_C1, rho_C2])
        return np.array([rho])
    