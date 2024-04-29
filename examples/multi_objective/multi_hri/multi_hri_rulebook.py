import numpy as np
from verifai.rulebook import rulebook

class rulebook_multi_hri(rulebook):
    iteration = 0

    def __init__(self, graph_path, rule_file, save_path=None, single_graph=False):
        super().__init__(graph_path, rule_file, single_graph=single_graph)
        self.save_path = save_path

    def evaluate(self, traj): # traj here is actually the SimulationResultClass
        bot_dist = np.array(traj.result.records['bot_dist'])
        ee_dist = np.array(traj.result.records['ee_dist'])
        box_dist = np.array(traj.result.records['box_dist'])
        spot_hold = np.array(traj.result.records['spot_hold'])
        human_in_pos = np.array([traj.result.records['human_in_pos']])
        
        start_idx = -1

        for i in range(len(bot_dist)):
            if bot_dist[i][1] != 0:
                start_idx = i
                break

        assert start_idx != -1, "Starting point not found"
        switch_idx = len(spot_hold)
        for i in range(start_idx, len(human_in_pos)):
            if type(human_in_pos[i]) == bool and human_in_pos[i] == True:
                switch_idx = i
        print(f"SWITCH_IDX: {switch_idx}\nRUNNING LEN: {len(spot_hold)}")
        assert switch_idx > start_idx, "Switching point should be larger than starting point"
        
        if self.save_path is not None:
            file_name = f"{self.save_path}/multi_hri_traj_{self.iteration}.txt"
            print("Writing trajectory to ", file_name)
            file = open(file_name, 'w')

            file.write('bot_dist\n')
            for dist in bot_dist:
                file.write(f"{dist[0]}, {dist[1]}\n")

            file.write("ee_dist\n")
            for dist in ee_dist:
                file.write(f"{dist[0]}, {dist[1]}\n")

            file.write("ee_box_dist\n")
            for dist in box_dist:
                file.write(f"{dist[0]}, {dist[1]}\n")

            file.write("spot_hold\n")
            for hold in spot_hold:
                file.write(f"{hold[0]}, {hold[1]}\n")
            file.close()
            self.iteration += 1


        indices_0 = np.arange(start_idx, switch_idx)
        indices_1 = np.arange(switch_idx, len(spot_hold))
        print(f"Indices: {indices_0}, {indices_1}")
        if self.single_graph: 
            rho0 = self.evaluate_segment(traj, 0, indices_0)
            rho0 = self.evaluate_segment(traj, 0, indices_1)
            print(f"Actual rho: {rho0}, {rho1}")
            rho = self.evaluate_segment(traj, 0, np.arange(0, len(spot_hold)))
            return np.array([rho])

        rho0 = self.evaluate_segment(traj, 0, indices_0)
        rho1 = self.evaluate_segment(traj, 1, indices_1)
        return np.array([rho0, rho1])
