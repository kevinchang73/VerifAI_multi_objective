from trimesh.transformations import compose_matrix

"""
keys of realization: 
network: scenic object for road network
max_steps
mesh: meshes for each object in the scene (trimesh)
object_type: type of each object in the scene ('Person', 'Car'...)
trajectory: list of dictionaries, where each dictionary contains the state information

keys of each state in trajectory:
position: list of positions of each object [(x, y, z), (x, y, z)...]
orientation: list of orientations of each object [(yaw, pitch, roll, w), (yaw, pitch, roll, w)...]
orientation_trimesh: " " [(yaw, pitch, roll), (yaw, pitch, roll)...]
velocity: list of velocities of each object [(x, y, z), (x, y, z)...]
step: corresponding timestep
"""
CAR_KG = 1670


def rule2_spec(realization):  # check if ego collides with adv, if so, calculate the kinetic energy and add to result
    trajectory = realization["trajectory"]
    max_steps = realization["max_steps"]
    object_types = realization["object_type"]
    num_objects = len(object_types)
    ego_mesh = realization["mesh"][0]

    result = 0

    for i in range(max_steps):
        ego_mesh_copy = ego_mesh.copy()
        state = trajectory[i]
        ego_pos = state["position"][0]
        ego_trimesh_orient = state["orientation_trimesh"][0]
        ego_matrix = compose_matrix(angles=ego_trimesh_orient, translate=ego_pos)
        ego_mesh_copy.apply_transform(ego_matrix)
        for j in range(1, num_objects):
            adv_mesh = realization["mesh"][j]
            adv_mesh_copy = adv_mesh.copy()
            adv_pos = state["position"][j]
            adv_trimesh_orient = state["orientation_trimesh"][j]
            adv_matrix = compose_matrix(angles=adv_trimesh_orient, translate=adv_pos)
            adv_mesh_copy.apply_transform(adv_matrix)
            intersection_region = ego_mesh_copy.bounding_box.intersection(
                adv_mesh_copy.bounding_box
            )
            if intersection_region.volume > 0:
                ego_velocity = state["velocity"][0]
                adv_velocity = state["velocity"][j]
                relative_velocity = [
                    ego_velocity[i] - adv_velocity[i] for i in range(3)
                ]
                result += CAR_KG * sum([v**2 for v in relative_velocity])/2
    
    return result