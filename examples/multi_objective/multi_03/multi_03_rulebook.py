import numpy as np

from verifai.rulebook import rulebook

class rulebook_multi03(rulebook):
    iteration = 0

    def __init__(self, graph_path, rule_file, save_path=None, single_graph=False):
        super().__init__(graph_path, rule_file, single_graph=single_graph)
        self.save_path = save_path
    
    def evaluate_segment(self, traj, graph_idx=0, start_idx=0, end_idx=None):
        # Evaluate the result of each rule on the segment (start_idx, end_idx) of the trajectory
        if end_idx is None:
            end_idx = len(traj.result.trajectory)
        priority_graph = self.priority_graphs[graph_idx]
        rho = np.ones(len(priority_graph.nodes))
        idx = 0
        for id in sorted(priority_graph.nodes):
            if self.verbosity >= 2:
                print('Evaluating rule', id)
            rule = priority_graph.nodes[id]['rule']
            if priority_graph.nodes[id]['active']:
                rho[idx] = rule.evaluate(traj, start_idx, end_idx)
            else:
                rho[idx] = 1
            idx += 1
        return rho

    def evaluate(self, traj):
        # Extract trajectory information
        positions = np.array(traj.result.trajectory)
        distances_to_adv1 = positions[:, [0], :] - positions[:, [1], :]
        distances_to_adv1 = np.linalg.norm(distances_to_adv1, axis=2) # compute the distance based on differences on x and y coordinates
        distances_to_adv2 = positions[:, [0], :] - positions[:, [2], :]
        distances_to_adv2 = np.linalg.norm(distances_to_adv2, axis=2)
        distances_to_adv3 = positions[:, [0], :] - positions[:, [3], :]
        distances_to_adv3 = np.linalg.norm(distances_to_adv3, axis=2)
        egotointersection = np.array(traj.result.records["egotoInter"])
        intersection_centroid_x = traj.result.records["interCentroidX"]
        intersection_centroid_y = traj.result.records["interCentroidY"]
        intersection_coords = np.array(traj.result.records["interCoords"])
        ego_start_road_coords = np.array(traj.result.records["startRoadCoords"])
        ego_end_road_coords = np.array(traj.result.records["endRoadCoords"])
        ego_start_lane_group_coords = np.array(traj.result.records["startLaneGroupCoords"])
        ego_end_lane_group_coords = np.array(traj.result.records["endLaneGroupCoords"])
        if self.verbosity >= 2:
            print("Intersection centroid: ", intersection_centroid_x, intersection_centroid_y)
        
        # Write trajectory to file for visualization
        if self.save_path is not None:
            file_name = self.save_path + "/multi_03_traj_" + str(self.iteration) + ".txt"
            print("Writing trajectory to", file_name)
            file = open(file_name, "w")
            file.write(str(intersection_centroid_x) + " " + str(intersection_centroid_y) + "\n")
            file.write(str(len(intersection_coords)) + "\n")
            for x, y in intersection_coords:
                file.write(str(x) + " " + str(y) + "\n")
            file.write(str(len(ego_start_road_coords)) + "\n")
            for x, y in ego_start_road_coords:
                file.write(str(x) + " " + str(y) + "\n")
            file.write(str(len(ego_end_road_coords)) + "\n")
            for x, y in ego_end_road_coords:
                file.write(str(x) + " " + str(y) + "\n")
            file.write(str(len(ego_start_lane_group_coords)) + "\n")
            for x, y in ego_start_lane_group_coords:
                file.write(str(x) + " " + str(y) + "\n")
            file.write(str(len(ego_end_lane_group_coords)) + "\n")
            for x, y in ego_end_lane_group_coords:
                file.write(str(x) + " " + str(y) + "\n")
            for i in range(len(positions)):
                file.write(str(positions[i][0][0]) + " " + str(positions[i][0][1]) + " " + str(positions[i][1][0]) + " " + str(positions[i][1][1]) + " " + str(positions[i][2][0]) + " " + str(positions[i][2][1]) + " " + str(positions[i][3][0]) + " " + str(positions[i][3][1]) + "\n")
            file.close()
            self.iteration += 1
        
        # Find the switching point
        ego_initial_x = positions[0][0][0] - intersection_centroid_x
        ego_initial_y = positions[0][0][1] - intersection_centroid_y
        switch = False
        switch_idx = -1
        if ego_initial_x > 0 and ego_initial_y > 0:
            assert(abs(ego_initial_x) > abs(ego_initial_y))
            for i in range(len(positions)):
                if not switch:
                    if positions[i][0][0]-intersection_centroid_x < 0:
                        switch = True
                        switch_idx = i
                if self.verbosity >= 2:
                    print(i, positions[i][0][0]-intersection_centroid_x, positions[i][0][1]-intersection_centroid_y, egotointersection[i][1], distances_to_adv1[i][0] - 5, distances_to_adv2[i][0] - 5, distances_to_adv3[i][0] - 5, switch)
        elif ego_initial_x < 0 and ego_initial_y > 0:
            assert(abs(ego_initial_x) < abs(ego_initial_y))
            for i in range(len(positions)):
                if not switch:
                    if positions[i][0][1]-intersection_centroid_y < 0:
                        switch = True
                        switch_idx = i
                if self.verbosity >= 2:
                    print(i, positions[i][0][0]-intersection_centroid_x, positions[i][0][1]-intersection_centroid_y, egotointersection[i][1], distances_to_adv1[i][0] - 5, distances_to_adv2[i][0] - 5, distances_to_adv3[i][0] - 5, switch)
        elif ego_initial_x < 0 and ego_initial_y < 0:
            assert(abs(ego_initial_x) > abs(ego_initial_y))
            for i in range(len(positions)):
                if not switch:
                    if positions[i][0][0]-intersection_centroid_x > 0:
                        switch = True
                        switch_idx = i
                if self.verbosity >= 2:
                    print(i, positions[i][0][0]-intersection_centroid_x, positions[i][0][1]-intersection_centroid_y, egotointersection[i][1], distances_to_adv1[i][0] - 5, distances_to_adv2[i][0] - 5, distances_to_adv3[i][0] - 5, switch)
        elif ego_initial_x > 0 and ego_initial_y < 0:
            assert(abs(ego_initial_x) < abs(ego_initial_y))
            for i in range(len(positions)):
                if not switch:
                    if positions[i][0][1]-intersection_centroid_y > 0:
                        switch = True
                        switch_idx = i
                if self.verbosity >= 2:
                    print(i, positions[i][0][0]-intersection_centroid_x, positions[i][0][1]-intersection_centroid_y, egotointersection[i][1], distances_to_adv1[i][0] - 5, distances_to_adv2[i][0] - 5, distances_to_adv3[i][0] - 5, switch)
        else:
            raise ValueError("Ego initial position is not in any quadrant")
        assert(switch)
        assert(switch_idx >= 0)

        # Evaluation
        if self.single_graph:
            rho0 = self.evaluate_segment(traj, 0, 0, switch_idx)
            rho1 = self.evaluate_segment(traj, 0, switch_idx, len(traj.result.trajectory))
            print('Actual rho:', rho0, rho1)
            rho = self.evaluate_segment(traj, 0, 0, len(traj.result.trajectory))
            return np.array([rho])
        rho0 = self.evaluate_segment(traj, 0, 0, switch_idx)
        rho1 = self.evaluate_segment(traj, 1, switch_idx, len(traj.result.trajectory))
        return np.array([rho0, rho1])