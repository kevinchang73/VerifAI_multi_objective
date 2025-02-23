from scenic.domains.driving.roads import Network
model scenic.simulators.carla.model
behavior bench():

    realization = globalParameters['realization']
    realization['network'] = Network.fromFile(globalParameters['map'])
    max_steps = realization['max_steps']
    objects = simulation().objects[:-1]
    realization['mesh'] = [obj.shape.mesh.copy() for obj in objects]
    realization['object_type'] = [type(obj).__name__ for obj in objects]
    realization['trajectory'] = []
    realization['ego'] = objects[0]
    realization['dimensions'] = [obj.occupiedSpace.dimensions for obj in objects]
    step = 0
    realization['convex'] = [obj.shape.isConvex for obj in objects]


    while step < max_steps:
        objects = simulation().objects[:-1]
        state = {} 
        state['position'] = []
        state['orientation'] = []
        state['orientation_trimesh'] = []
        state['velocity'] = []

        for obj in objects:
            state['position'].append((obj.position.x, obj.position.y, obj.position.z))
            state['orientation'].append(obj.orientation)
            state['orientation_trimesh'].append(obj.orientation._trimeshEulerAngles())
            state['velocity'].append((obj.velocity.x, obj.velocity.y, obj.velocity.z))
            state['step'] = step
        realization['trajectory'].append(state)
        step += 1
        if step == max_steps:
            break
        
        wait


BENCH_OBJ = new Bench with behavior bench()