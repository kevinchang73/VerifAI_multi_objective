import numpy as np

from verifai.rulebook import rulebook

class rulebook_multi01(rulebook):
    iteration = 0

    def __init__(self, graph_path, rule_file, save_path=None, single_graph=False, using_sampler=-1):
        rulebook.using_sampler = using_sampler
        super().__init__(graph_path, rule_file, single_graph=single_graph)
        self.save_path = save_path

    def evaluate(self, traj):
        # Extract trajectory information
        positions = np.array(traj.result.trajectory)
        init_lane_coords = np.array(traj.result.records["initLaneCoords"])
        left_lane_coords = np.array(traj.result.records["leftLaneCoords"])
        ego_is_in_init_lane = np.array(traj.result.records["egoIsInInitLane"])
        ego_is_in_left_lane = np.array(traj.result.records["egoIsInLeftLane"])

        # Find switching points
        switch_idx_1 = len(traj.result.trajectory)
        switch_idx_2 = len(traj.result.trajectory)
        distances_to_obs = positions[:, 0, :] - positions[:, 1, :]
        distances_to_obs = np.linalg.norm(distances_to_obs, axis=1)
        for i in range(len(distances_to_obs)):
            if distances_to_obs[i] < 8.5 and switch_idx_1 == len(traj.result.trajectory):
                switch_idx_1 = i
                continue
            if distances_to_obs[i] > 10 and switch_idx_1 < len(traj.result.trajectory) and switch_idx_2 == len(traj.result.trajectory):
                switch_idx_2 = i
                break
        assert switch_idx_1 < len(traj.result.trajectory), "Switching point 1 cannot be found"

        # Write trajectory to file for visualization
        if self.save_path is not None:
            file_name = self.save_path + "/multi_01_traj_" + str(self.iteration) + ".txt"
            print("Writing trajectory to", file_name)
            file = open(file_name, "w")
            file.write(str(len(init_lane_coords)) + "\n")
            for x, y in init_lane_coords:
                file.write(str(x) + " " + str(y) + "\n")
            file.write(str(len(left_lane_coords)) + "\n")
            for x, y in left_lane_coords:
                file.write(str(x) + " " + str(y) + "\n")
            file.write('switch_idx_1 ' + str(switch_idx_1) + ' ' + 'switch_idx_2 ' + str(switch_idx_2) + '\n')
            for i in range(0, len(positions)):
                file.write(str(distances_to_obs[i]) + " " + str(ego_is_in_init_lane[i][1]) + " " + str(ego_is_in_left_lane[i][1]) + "\n")
            #for i in range(0, len(positions)):
            #    file.write(str(positions[i][0][0]) + " " + str(positions[i][0][1]) + " " + str(positions[i][1][0]) + " " + str(positions[i][1][1]) + " " + str(ego_is_in_init_lane[i][1]) + " " + str(ego_is_in_left_lane[i][1]) + "\n")
            file.close()
            self.iteration += 1
        
        # Evaluation
        indices_0 = np.arange(0, switch_idx_1)
        indices_1 = np.arange(switch_idx_1, switch_idx_2)
        indices_2 = np.arange(switch_idx_2, len(traj.result.trajectory))
        if self.single_graph:
            rho0 = self.evaluate_segment(traj, 0, indices_0)
            rho1 = self.evaluate_segment(traj, 0, indices_1)
            rho2 = self.evaluate_segment(traj, 0, indices_2)
            print('Actual rho:')
            print(rho0[0], rho0[1])
            print(rho1[0], rho1[1])
            print(rho2[0], rho2[1])
            rho = self.evaluate_segment(traj, 0, np.arange(0, len(traj.result.trajectory)))
            return np.array([rho])
        rho0 = self.evaluate_segment(traj, 0, indices_0)
        rho1 = self.evaluate_segment(traj, 1, indices_1)
        rho2 = self.evaluate_segment(traj, 2, indices_2)
        return np.array([rho0, rho1, rho2])