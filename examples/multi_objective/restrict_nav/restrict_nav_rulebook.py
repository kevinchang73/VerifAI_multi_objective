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
        trespass = traj.result.records["trespass"]
        table_dist = np.array(traj.result.records["table_dist"])
        ego_too_close = traj.result.records["ego_too_close"]
        dist_to_goal = np.array(traj.result.records["dist_to_goal"])
        
        # Find switching points
        switch_index = len(trespass)

        start_index = 0
        for i in range(start_index, len(trespass)):
            if table_dist[i][1] <=2:
                switch_index = i

        if self.save_path is not None:
            file_name = f"{self.save_path}/restrict_nav_{self.iteration}.txt"
            print("Writing trajectory to ", file_name)
            file = open(file_name, 'w')

            file.write('trespass\n')
            for did_trespass in trespass:
                file.write(f"{did_trespass[0]}, {did_trespass[1]}\n")

            file.write("table_dist\n")
            for dist in table_dist:
                file.write(f"{dist[0]}, {dist[1]}\n")

            file.write("ego_too_close\n")
            for too_close in ego_too_close:
                file.write(f"{too_close[0]}, {too_close[1]}\n")

            file.write("dist_to_goal\n")
            for dist in dist_to_goal:
                file.write(f"{dist[0]}, {dist[1]}\n")
            file.close()
            self.iteration += 1

        indices_0 = np.arange(start_index, switch_index)
        indices_1 = np.arange(switch_index, len(ego_too_close))
        rho0 = self.evaluate_segment(traj, 0, indices_0)
        rho1 = self.evaluate_segment(traj, 1, indices_1)
        return np.array([rho0, rho1])
