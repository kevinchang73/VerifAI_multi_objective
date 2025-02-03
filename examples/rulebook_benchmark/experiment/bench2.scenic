from scenic.domains.driving.roads import Network
model scenic.simulators.carla.model
behavior bench():

    realization = globalParameters['realization']
    realization['network'] = Network.fromFile(globalParameters['map'])
    max_steps = realization['max_steps']
    objects = simulation().objects[:-1]

    realization['object_type'] = [type(obj).__name__ for obj in objects]
    realization['trajectory'] = []
    realization['ego'] = objects[0]
    step = 0


    while step < max_steps:
        objects = simulation().objects[:-1]
        state = {} 
        state['position'] = []
        state['orientation'] = []
        state['orientation_trimesh'] = []
        state['velocity'] = []
        for obj in objects:
            state['position'].append((obj.position.x, obj.position.y))
            state['velocity'].append((obj.velocity.x, obj.velocity.y))
            state['step'] = step
        realization['trajectory'].append(state)

        
        step += 1
        if step == max_steps:
            break
        
        wait


BENCH_OBJ = Bench with behavior bench()