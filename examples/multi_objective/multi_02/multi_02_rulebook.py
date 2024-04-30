import numpy as np

from verifai.rulebook import rulebook

class rulebook_multi02(rulebook):
    iteration = 0

    def __init__(self, graph_path, rule_file, save_path=None, single_graph=False, using_sampler=-1):
        rulebook.using_sampler = using_sampler
        super().__init__(graph_path, rule_file, single_graph=single_graph)
        self.save_path = save_path

    def evaluate(self, traj):
        # Extract trajectory information
        positions = np.array(traj.result.trajectory)
        ego_start_lane_coords = np.array(traj.result.records["egoStartLaneCoords"])
        ego_end_lane_coords = np.array(traj.result.records["egoEndLaneCoords"])
        ego_is_in_init_lane = np.array(traj.result.records["egoIsInInitLane"])
        adv2_is_in_init_lane = np.array(traj.result.records["adv2IsInInitLane"])
        adv3_is_in_init_lane = np.array(traj.result.records["adv3IsInInitLane"])

        # Find starting point, i.e., adv2 and adv3 have reached the new lane
        start_idx = -1
        for i in range(len(adv2_is_in_init_lane)):
            if adv2_is_in_init_lane[i][1] == 0 and adv3_is_in_init_lane[i][1] == 0:
                start_idx = i
                break
        assert start_idx != -1, "Starting point not found"

        # Find switching point, i.e., ego has reached the new lane
        switch_idx = len(traj.result.trajectory)
        for i in range(start_idx, len(ego_is_in_init_lane)):
            if ego_is_in_init_lane[i][1] == 0:
                switch_idx = i
                break
        assert switch_idx > start_idx, "Switching point should be larger than starting point"

        # Write trajectory to file for visualization
        if self.save_path is not None:
            file_name = self.save_path + "/multi_02_traj_" + str(self.iteration) + ".txt"
            print("Writing trajectory to", file_name)
            file = open(file_name, "w")
            file.write(str(len(ego_start_lane_coords)) + "\n")
            for x, y in ego_start_lane_coords:
                file.write(str(x) + " " + str(y) + "\n")
            file.write(str(len(ego_end_lane_coords)) + "\n")
            for x, y in ego_end_lane_coords:
                file.write(str(x) + " " + str(y) + "\n")
            for i in range(start_idx, len(positions)):
                file.write(str(positions[i][0][0]) + " " + str(positions[i][0][1]) + " " + str(positions[i][1][0]) + " " + str(positions[i][1][1]) + " " + str(positions[i][2][0]) + " " + str(positions[i][2][1]) + " " + str(positions[i][3][0]) + " " + str(positions[i][3][1]) + "\n")
            file.close()
            self.iteration += 1
        
        # Evaluation
        indices_0 = np.arange(start_idx, switch_idx)
        indices_1 = np.arange(switch_idx, len(traj.result.trajectory))
        if self.single_graph:
            rho0 = self.evaluate_segment(traj, 0, indices_0)
            rho1 = self.evaluate_segment(traj, 0, indices_1)
            print('Actual rho:', rho0, rho1)           
            rho = self.evaluate_segment(traj, 0, np.arange(0, len(traj.result.trajectory)))
            return np.array([rho])
        rho0 = self.evaluate_segment(traj, 0, indices_0)
        rho1 = self.evaluate_segment(traj, 1, indices_1)
        return np.array([rho0, rho1])