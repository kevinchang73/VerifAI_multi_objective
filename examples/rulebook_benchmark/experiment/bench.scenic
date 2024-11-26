from scenic.domains.driving.roads import Network
import copy

behavior bench(agent_behavior):

    realization = globalParameters['realization']
    realization['network'] = Network.fromFile(globalParameters['map'])
    max_steps = realization['max_steps']
    objects = simulation().objects
    realization['mesh'] = [obj.shape.mesh.copy() for obj in objects]
    realization['object_type'] = [type(obj).__name__ for obj in objects]
    realization['trajectory'] = []
    step = 0


    while step < max_steps:
        objects = simulation().objects
        state = {} 
        state['position'] = []
        state['orientation'] = []
        state['orientation_trimesh'] = []
        state['velocity'] = []
        for obj in objects:
            state['position'].append((obj.position.x, obj.position.y, obj.position.z))
            state['orientation'].append(obj.orientation.eulerAngles)
            state['orientation_trimesh'].append(obj.orientation._trimeshEulerAngles())
            state['velocity'].append((obj.velocity.x, obj.velocity.y, obj.velocity.z))
            state['step'] = step
        realization['trajectory'].append(state)

        
        step += 1
        if step == max_steps:
            break
        
        do agent_behavior() for 1 steps   
