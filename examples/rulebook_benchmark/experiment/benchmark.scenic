import json
behavior benchmark(agent_behavior, network, max_steps):
    traj = []

    while True:
        state = {}
        step = simulation().currentTime
        objects = simulation().objects
        ego = objects[0]




        object_types = [] # ['Car', 'Car', 'Pedestrian', ...]
        positions = []  # [(x1, y1), (x2, y2), ...]
        velocities = [] # [(vx1, vy1), (vx2, vy2), ...]
        on_drivable_area = [] # [True, False, False, ...] True if object is on drivable area
        dist_to_ego = [] # distance from ego to object
        ego_collided_objects_bb = [] # indices of objects that collide with ego based on bounding box intersection
        ego_collided_objects_dist = [] # indices of objects that collide with ego based on distance

        i = 0
        for obj in objects:
            positions.append((obj.position.x, obj.position.y))
            velocities.append((obj.velocity.x, obj.velocity.y))
            
            if obj in network.drivableRegion:
                on_drivable_area.append(True)
            else:
                on_drivable_area.append(False)

            object_types.append(type(obj).__name__)

            dist = distance from ego to obj
            dist_to_ego.append(dist)

            if i > 0:
                collision_bb = ego.boundingBox intersects obj.boundingBox
                if collision_bb: ego_collided_objects_bb.append(i)

                if dist == 0: ego_collided_objects_dist.append(i)

            i += 1


        if on_drivable_area[0] == True:
            state['ego_distance_to_lane_centerline'] = distance from ego to ego.lane.centerline
        else: # if we check ego.lane outside drivable area, the simulation stops, so we need to handle this case
            state['ego_distance_to_lane_centerline'] = None
        


        # keys that start with 'ego_' are ONLY for the ego vehicle, so the value is a singular value; the rest are for all objects and are arrays
        state['object_types'] = object_types
        state['position'] = positions
        state['velocity'] = velocities
        state['on_drivable_area'] = on_drivable_area
        state['ego_dist_to_drivable_region'] = distance from ego to network.drivableRegion
        state['ego_heading'] = ego.heading
        state['ego_speed'] = ego.speed
        state['ego_road_deviation'] = ego.roadDeviation
        state['collided_objects_bb'] = ego_collided_objects_bb
        state['collided_objects_dist'] = ego_collided_objects_dist
        state['dist_to_ego'] = dist_to_ego

        traj.append((step, state))

        if step == max_steps - 1: # current workaround for knowing when the simulation ends. we could also just write to the file every step
            with open(f'benchmark_{step}_steps.json', 'w') as f:
                json.dump(traj, f)






        do agent_behavior() for 1 steps