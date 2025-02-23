from trimesh.transformations import compose_matrix
from scenic.core.regions import MeshVolumeRegion, EmptyRegion
import shapely
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


def rule_vehicle_collision(realization):
    return max(rule_collision(realization, "Car"), rule_collision(realization, "Truck"))

def rule_vru_collision(realization):
    return max(rule_collision(realization, "Pedestrian"), rule_collision(realization, "Bicycle"))


def rule_collision(realization, object_type="Pedestrian"):
    trajectory = realization["trajectory"]
    max_steps = realization["max_steps"]
    object_types = realization["object_type"]
    num_objects = len(object_types)
    ego_mesh = realization["mesh"][0]
    ego_dimension = realization["dimensions"][0]
    max_violation = 0
    
    for i in range(max_steps-1):
        ego_pos = trajectory[i]["position"][0]
        ego_orientation = trajectory[i]["orientation"][0]
        ego_region = MeshVolumeRegion(mesh=ego_mesh, dimensions=ego_dimension, position=ego_pos, rotation=ego_orientation)
        ego_velocity = trajectory[i+1]["velocity"][0]
        ego_velocity_before = trajectory[i]["velocity"][0]
        for j in range(1, num_objects):
            if object_types[j] != object_type:
                continue
            adv_mesh = realization["mesh"][j]
            adv_dimension = realization["dimensions"][j]
            adv_pos = trajectory[i]["position"][j]
            adv_orientation = trajectory[i]["orientation"][j]
            adv_region = MeshVolumeRegion(mesh=adv_mesh, dimensions=adv_dimension, position=adv_pos, rotation=adv_orientation)
            adv_velocity = trajectory[i+1]["velocity"][j]
            adv_velocity_before = trajectory[i]["velocity"][j]
            if ego_region.intersects(adv_region):
                
                v_ego_delta = [ego_velocity[i] - ego_velocity_before[i] for i in range(3)]
                v_adv_delta = [adv_velocity[i] - adv_velocity_before[i] for i in range(3)]
                v_ego_delta_norm = sum([v**2 for v in v_ego_delta])**0.5
                v_adv_delta_norm = sum([v**2 for v in v_adv_delta])**0.5
                max_violation = max(max_violation, v_ego_delta_norm, v_adv_delta_norm)
    return max_violation
    
    
    
    
def rule_stay_in_drivable_area(realization):
    network = realization["network"]
    drivable_region = network.drivableRegion
    trajectory = realization["trajectory"]
    max_steps = realization["max_steps"]
    ego_mesh = realization["mesh"][0]
    ego_dimension = realization["dimensions"][0]
    max_violation = 0
    
    for i in range(max_steps):
        ego_pos = trajectory[i]["position"][0]
        ego_orientation = trajectory[i]["orientation"][0]
        ego_region = MeshVolumeRegion(mesh=ego_mesh, dimensions=ego_dimension, position=ego_pos, rotation=ego_orientation)
        ego_polygon = ego_region.boundingPolygon
        difference = ego_polygon.difference(drivable_region)
        if not isinstance(difference, EmptyRegion):
            max_violation = max(max_violation, difference.area)

    return max_violation



def rule_stay_in_drivable_area_distance(realization):
    network = realization["network"]
    drivable_region = network.drivableRegion
    trajectory = realization["trajectory"]
    max_steps = realization["max_steps"]
    ego_mesh = realization["mesh"][0]
    ego_dimension = realization["dimensions"][0]
    max_violation = 0
    
    for i in range(max_steps):
        ego_pos = trajectory[i]["position"][0]
        ego_orientation = trajectory[i]["orientation"][0]
        ego_region = MeshVolumeRegion(mesh=ego_mesh, dimensions=ego_dimension, position=ego_pos, rotation=ego_orientation)
        ego_polygon = ego_region.boundingPolygon.polygons
        drivable_polygon = drivable_region.polygons
        distance = shapely.hausdorff_distance(ego_polygon, drivable_polygon)
        max_violation = max(max_violation, distance)

    return max_violation



def vru_clearance(realization, on_road=False):
    threshold = 2
    network = realization["network"]
    trajectory = realization["trajectory"]
    max_steps = realization["max_steps"]
    object_types = realization["object_type"]
    num_objects = len(object_types)
    ego_mesh = realization["mesh"][0]
    ego_dimension = realization["dimensions"][0]
    drivable_region = network.drivableRegion
    max_violation = 0
    
    for i in range(max_steps):
        ego_pos = trajectory[i]["position"][0]
        ego_orientation = trajectory[i]["orientation"][0]
        ego_region = MeshVolumeRegion(mesh=ego_mesh, dimensions=ego_dimension, position=ego_pos, rotation=ego_orientation)
        for j in range(1, num_objects):
            if object_types[j] != "Pedestrian" and object_types[j] != "Bicycle":
                continue
            
            
            adv_mesh = realization["mesh"][j]
            adv_dimension = realization["dimensions"][j]
            adv_pos = trajectory[i]["position"][j]
            adv_orientation = trajectory[i]["orientation"][j]
            adv_region = MeshVolumeRegion(mesh=adv_mesh, dimensions=adv_dimension, position=adv_pos, rotation=adv_orientation)
                        
            ego_polygon = ego_region.boundingPolygon.polygons
            adv_polygon = adv_region.boundingPolygon.polygons
            distance = ego_polygon.distance(adv_polygon)
            violation = threshold - distance
            
            if (on_road and drivable_region.intersects(adv_region)) or (not on_road and not drivable_region.intersects(adv_region)):
                max_violation = max(max_violation, violation)
            
    return max_violation



def vru_clearance_on_road(realization):
    return vru_clearance(realization, on_road=True)


def vru_clearance_off_road(realization):
    return vru_clearance(realization, on_road=False)


def vru_acknowledgement(realization, proximity=5, deceleration=0.2,  timesteps=10):

    trajectory = realization["trajectory"]
    max_steps = realization["max_steps"]
    object_types = realization["object_type"]
    num_objects = len(object_types)
    ego_mesh = realization["mesh"][0]
    ego_dimension = realization["dimensions"][0]
    max_violation = 0
    
    for i in range(max_steps - timesteps):
        ego_pos = trajectory[i]['position'][0]
        ego_velocity = trajectory[i]['velocity'][0]
        ego_next_velocity = trajectory[i+1]['velocity'][0]
        
        ego_future_pos = trajectory[i+timesteps]['position'][0]
        adv_future_pos = trajectory[i+timesteps]['position'][1]
        
        distance = sum([(ego_future_pos[j] - adv_future_pos[j])**2 for j in range(3)])**0.5
        if distance < proximity:
            ego_velocity_norm = sum([v**2 for v in ego_velocity])**0.5
            ego_next_velocity_norm = sum([v**2 for v in ego_next_velocity])**0.5
            violation = deceleration - (ego_velocity_norm - ego_next_velocity_norm)
            max_violation = max(max_violation, violation)
            
    return max_violation
                

        
                

        
        
    
    