import numpy as np

from verifai.rulebook import rulebook

class rulebook_multi04(rulebook):
    iteration = 0

    def __init__(self, graph_path, rule_file, save_path=None, single_graph=False, using_sampler=-1, exploration_ratio=2.0):
        rulebook.using_sampler = using_sampler
        rulebook.exploration_ratio = exploration_ratio
        super().__init__(graph_path, rule_file, single_graph=single_graph)
        self.save_path = save_path

    def evaluate(self, simulation):
        # Extract trajectory information
        positions = np.array(simulation.result.trajectory)
        ego_dist_to_intersection = np.array(simulation.result.records["egoDistToIntersection"])
        
        # Find switching points, i.e., ego has reached the intersection / ego has finished the right turn
        switch_idx_1 = len(simulation.result.trajectory)
        switch_idx_2 = len(simulation.result.trajectory)
        for i in range(len(ego_dist_to_intersection)):
            if ego_dist_to_intersection[i][1] == 0 and switch_idx_1 == len(simulation.result.trajectory):
                switch_idx_1 = i
                break
        if switch_idx_1 < len(simulation.result.trajectory):
            for i in reversed(range(switch_idx_1, len(ego_dist_to_intersection))):
                if ego_dist_to_intersection[i][1] == 0:
                    switch_idx_2 = i + 1
                    break
        assert switch_idx_1 <= switch_idx_2

        # Write trajectory to file for visualization
        intersection_coords = np.array(simulation.result.records["interCoords"])
        ego_start_road_coords = np.array(simulation.result.records["startRoadCoords"])
        ego_end_road_coords = np.array(simulation.result.records["endRoadCoords"])
        ego_start_lane_group_coords = np.array(simulation.result.records["startLaneGroupCoords"])
        ego_end_lane_group_coords = np.array(simulation.result.records["endLaneGroupCoords"])
        ego_dist_to_adv1 = np.array(simulation.result.records["egoDistToAdv1"])
        ego_dist_to_ego_spawn_pt = np.array(simulation.result.records["egoDistToEgoSpawnPt"])
        if self.save_path is not None:
            file_name = self.save_path + "/multi_04_traj_" + str(self.iteration) + ".txt"
            print("Writing trajectory to", file_name)
            file = open(file_name, "w")
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
            for i in range(0, len(positions)):
                file.write(str(positions[i][0][0]) + " " + str(positions[i][0][1]) + " " + str(positions[i][1][0]) + " " + str(positions[i][1][1]) + " " + str(positions[i][2][0]) + " " + str(positions[i][2][1]) + " " + str(positions[i][3][0]) + " " + str(positions[i][3][1]) + " " + str(positions[i][4][0]) + " " + str(positions[i][4][1]) + " " + str(positions[i][5][0]) + " " + str(positions[i][5][1]) + " " + str(ego_dist_to_adv1[i][1]) + " " + str(ego_dist_to_ego_spawn_pt[i][1]) + "\n")
            file.close()
            self.iteration += 1
        
        # Evaluation
        indices_0 = np.arange(0, switch_idx_1)
        indices_1 = np.arange(switch_idx_1, switch_idx_2)
        indices_2 = np.arange(switch_idx_2, len(simulation.result.trajectory))
        #print('Indices:', indices_0, indices_1, indices_2)
        if self.single_graph:
            rho0 = self.evaluate_segment(simulation, 0, indices_0)
            rho1 = self.evaluate_segment(simulation, 0, indices_1)
            rho2 = self.evaluate_segment(simulation, 0, indices_2)
            print('Actual rho:')
            for r in rho0:
                print(r, end=' ')
            print()
            for r in rho1:
                print(r, end=' ')
            print()
            for r in rho2:
                print(r, end=' ')
            print()
            rho = self.evaluate_segment(simulation, 0, np.arange(0, len(simulation.result.trajectory)))
            return np.array([rho])
        rho0 = self.evaluate_segment(simulation, 0, indices_0)
        rho1 = self.evaluate_segment(simulation, 1, indices_1)
        rho2 = self.evaluate_segment(simulation, 2, indices_2)
        return np.array([rho0, rho1, rho2])
    