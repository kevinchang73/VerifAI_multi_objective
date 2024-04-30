import numpy as np

from verifai.rulebook import rulebook

class rulebook_multi03(rulebook):
    iteration = 0

    def __init__(self, graph_path, rule_file, save_path=None, single_graph=False, using_sampler=-1):
        rulebook.using_sampler = using_sampler
        super().__init__(graph_path, rule_file, single_graph=single_graph)
        self.save_path = save_path

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
        indices_A = np.empty(0, dtype=int)
        indices_B = np.empty(0, dtype=int)
        indices_C = np.empty(0, dtype=int)
        indices_D = np.empty(0, dtype=int)
        if ego_initial_x > 0 and ego_initial_y > 0:
            #assert(abs(ego_initial_x) > abs(ego_initial_y))
            for i in range(len(positions)):
                ego_x = positions[i][0][0] - intersection_centroid_x
                ego_y = positions[i][0][1] - intersection_centroid_y
                region = ''
                if ego_x > 0 and ego_y > 0:
                    indices_A = np.append(indices_A, i)
                    region = 'A'
                elif ego_x < 0 and ego_y > 0:
                    indices_C = np.append(indices_C, i)
                    region = 'C'
                elif ego_x < 0 and ego_y < 0:
                    indices_D = np.append(indices_D, i)
                    region = 'D'
                elif ego_x > 0 and ego_y < 0:
                    indices_B = np.append(indices_B, i)
                    region = 'B'
                if self.verbosity >= 2:
                    print(i, positions[i][0][0]-intersection_centroid_x, positions[i][0][1]-intersection_centroid_y, egotointersection[i][1], distances_to_adv1[i][0] - 5, distances_to_adv2[i][0] - 5, distances_to_adv3[i][0] - 5, region)
        elif ego_initial_x < 0 and ego_initial_y > 0:
            assert(abs(ego_initial_x) < abs(ego_initial_y))
            for i in range(len(positions)):
                ego_x = positions[i][0][0] - intersection_centroid_x
                ego_y = positions[i][0][1] - intersection_centroid_y
                region = ''
                if ego_x > 0 and ego_y > 0:
                    indices_B = np.append(indices_B, i)
                    region = 'B'
                elif ego_x < 0 and ego_y > 0:
                    indices_A = np.append(indices_A, i)
                    region = 'A'
                elif ego_x < 0 and ego_y < 0:
                    indices_C = np.append(indices_C, i)
                    region = 'C'
                elif ego_x > 0 and ego_y < 0:
                    indices_D = np.append(indices_D, i)
                    region = 'D'
                if self.verbosity >= 2:
                    print(i, positions[i][0][0]-intersection_centroid_x, positions[i][0][1]-intersection_centroid_y, egotointersection[i][1], distances_to_adv1[i][0] - 5, distances_to_adv2[i][0] - 5, distances_to_adv3[i][0] - 5, region)
        elif ego_initial_x < 0 and ego_initial_y < 0:
            #assert(abs(ego_initial_x) > abs(ego_initial_y))
            for i in range(len(positions)):
                ego_x = positions[i][0][0] - intersection_centroid_x
                ego_y = positions[i][0][1] - intersection_centroid_y
                region = ''
                if ego_x > 0 and ego_y > 0:
                    indices_D = np.append(indices_D, i)
                    region = 'D'
                elif ego_x < 0 and ego_y > 0:
                    indices_B = np.append(indices_B, i)
                    region = 'B'
                elif ego_x < 0 and ego_y < 0:
                    indices_A = np.append(indices_A, i)
                    region = 'A'
                elif ego_x > 0 and ego_y < 0:
                    indices_C = np.append(indices_C, i)
                    region = 'C'
                if self.verbosity >= 2:
                    print(i, positions[i][0][0]-intersection_centroid_x, positions[i][0][1]-intersection_centroid_y, egotointersection[i][1], distances_to_adv1[i][0] - 5, distances_to_adv2[i][0] - 5, distances_to_adv3[i][0] - 5, region)
        elif ego_initial_x > 0 and ego_initial_y < 0:
            #assert(abs(ego_initial_x) < abs(ego_initial_y))
            for i in range(len(positions)):
                ego_x = positions[i][0][0] - intersection_centroid_x
                ego_y = positions[i][0][1] - intersection_centroid_y
                region = ''
                if ego_x > 0 and ego_y > 0:
                    indices_C = np.append(indices_C, i)
                    region = 'C'
                elif ego_x < 0 and ego_y > 0:
                    indices_D = np.append(indices_D, i)
                    region = 'D'
                elif ego_x < 0 and ego_y < 0:
                    indices_B = np.append(indices_B, i)
                    region = 'B'
                elif ego_x > 0 and ego_y < 0:
                    indices_A = np.append(indices_A, i)
                    region = 'A'
                if self.verbosity >= 2:
                    print(i, positions[i][0][0]-intersection_centroid_x, positions[i][0][1]-intersection_centroid_y, egotointersection[i][1], distances_to_adv1[i][0] - 5, distances_to_adv2[i][0] - 5, distances_to_adv3[i][0] - 5, region)
        else:
            raise ValueError("Ego initial position is not in any quadrant")

        # Evaluation
        if self.single_graph:
            rho0 = self.evaluate_segment(traj, 0, indices_A)
            rho1 = self.evaluate_segment(traj, 0, indices_B)
            rho2 = self.evaluate_segment(traj, 0, indices_C)
            rho3 = self.evaluate_segment(traj, 0, indices_D)
            print('Actual rho:', rho0, rho1, rho2, rho3)
            rho = self.evaluate_segment(traj, 0, np.arange(0, len(traj.result.trajectory)))
            return np.array([rho])
        rho0 = self.evaluate_segment(traj, 0, indices_A)
        rho1 = self.evaluate_segment(traj, 1, indices_B)
        rho2 = self.evaluate_segment(traj, 2, indices_C)
        rho3 = self.evaluate_segment(traj, 3, indices_D)
        return np.array([rho0, rho1, rho2, rho3])