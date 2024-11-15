import json
behavior benchmark(agent_behavior, network, max_steps):
    traj = []

    while True:
        state = {}
        step = simulation().currentTime
        objects = simulation().objects
        ego = objects[0]




        object_types = []
        positions = []
        velocities = []
        on_drivable_area = []
        dist_to_ego = []
        ego_collided_objects_bb = []
        ego_collided_objects_dist = []

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
        else:
            state['ego_distance_to_lane_centerline'] = None
        
        state['object_types'] = object_types
        state['position'] = positions
        state['velocity'] = velocities
        state['on_drivable_area'] = on_drivable_area
        state['ego_dist_to_drivable_region'] = distance from ego to network.drivableRegion
        state['ego_heading'] = ego.heading
        state['ego_speed'] = ego.speed
        state['ego_road_deviation'] = ego.roadDeviation
        state['ego_collided_objects_bb'] = ego_collided_objects_bb
        state['ego_collided_objects_dist'] = ego_collided_objects_dist
        state['dist_to_ego'] = dist_to_ego

        traj.append((step, state))

        if step == max_steps - 1:
            with open(f'benchmark_{step}_steps.json', 'w') as f:
                json.dump(traj, f)






        do agent_behavior() for 1 steps