"""
TITLE: Multi 05
AUTHOR: 
DESCRIPTION: 
SOURCE:
"""

#################################
# MAP AND MODEL                 #
#################################

param map = localPath('../maps/Town05.xodr')
param carla_map = 'Town05'
param N = 13
model scenic.simulators.carla.model

#################################
# CONSTANTS                     #
#################################

MODEL = 'vehicle.lincoln.mkz_2017'

INIT_DIST = [15, 20]
v3_DIST = -10
param VEHICLE_SPEED = VerifaiRange(8, 10)
param VEHICLE_BRAKE = VerifaiRange(0.8, 1.0)

SAFETY_DIST = 8
param ARRIVE_INTERSECTION_DIST = VerifaiRange(2, 5)
TERM_DIST = 50
ARRIVING_ORDER = []
HAS_PASSED = [False, False, False, False]
PASSING_ORDER = []

#################################
# AGENT BEHAVIORS               #
#################################

def CanEnter(id):
    for i in range(len(ARRIVING_ORDER)):
        if ARRIVING_ORDER[i] == id:
            return True
        if HAS_PASSED[ARRIVING_ORDER[i]] == False:
            return False

behavior VehicleBehavior(trajectory, id):
    wait_flag = False # if the vehicle has joined the waiting list
    enter_flag = False # if the vehicle has entered the intersection
    leave_flag = False # if the vehicle has passed the intersection
    if id == 0:
        ARRIVING_ORDER.clear()
        PASSING_ORDER.clear()
    HAS_PASSED[id] = False
    try:
        do FollowTrajectoryBehavior(target_speed=globalParameters.VEHICLE_SPEED, trajectory=trajectory)
        do FollowLaneBehavior(target_speed=globalParameters.VEHICLE_SPEED)
    #interrupt when (distance from self to intersection) < globalParameters.ARRIVE_INTERSECTION_DIST and not CanEnter(id):
    #    take SetBrakeAction(globalParameters.VEHICLE_BRAKE)
    interrupt when (distance from self to intersection) < globalParameters.ARRIVE_INTERSECTION_DIST and not wait_flag:
        ARRIVING_ORDER.append(id)
        #print("Vehicle", id, "is waiting", ARRIVING_ORDER)
        wait_flag = True
    interrupt when (distance from self to intersection) == 0 and wait_flag and not enter_flag:
        #print("Vehicle", id, "is entering")
        enter_flag = True
    interrupt when (distance from self to intersection) > 0 and enter_flag and not leave_flag:
        #print("Vehicle", id, "has passed")
        leave_flag = True
        HAS_PASSED[id] = True
        PASSING_ORDER.append(id)
    interrupt when withinDistanceToAnyObjs(self, SAFETY_DIST):
        take SetBrakeAction(globalParameters.VEHICLE_BRAKE)

behavior FollowBehavior(trajectory, id, front):
    wait_flag = False # if the vehicle has joined the waiting list
    enter_flag = False # if the vehicle has entered the intersection
    leave_flag = False # if the vehicle has passed the intersection
    if id == 0:
        ARRIVING_ORDER.clear()
    HAS_PASSED[id] = False
    try:
        do FollowTrajectoryBehavior(target_speed=globalParameters.VEHICLE_SPEED, trajectory=trajectory)
        do FollowLaneBehavior(target_speed=globalParameters.VEHICLE_SPEED)
    #interrupt when (distance from self to intersection) < globalParameters.ARRIVE_INTERSECTION_DIST and not CanEnter(id):
    #    take SetBrakeAction(globalParameters.VEHICLE_BRAKE)
    interrupt when (distance from self to intersection) < globalParameters.ARRIVE_INTERSECTION_DIST and not wait_flag:
        ARRIVING_ORDER.append(id)
        #print("Vehicle", id, "is waiting", ARRIVING_ORDER)
        wait_flag = True
    interrupt when (distance from self to intersection) == 0 and wait_flag and not enter_flag:
        #print("Vehicle", id, "is entering")
        enter_flag = True
    interrupt when (distance from self to intersection) > 0 and enter_flag and not leave_flag:
        #print("Vehicle", id, "has passed")
        leave_flag = True
        HAS_PASSED[id] = True
        PASSING_ORDER.append(id)
    interrupt when (distance from self to front) < SAFETY_DIST:
        take SetBrakeAction(globalParameters.VEHICLE_BRAKE)
    interrupt when withinDistanceToAnyObjs(self, SAFETY_DIST):
        take SetBrakeAction(globalParameters.VEHICLE_BRAKE)

#################################
# SPATIAL RELATIONS             #
#################################

intersection = Uniform(*filter(lambda i: i.is4Way, network.intersections))

# v0: straight from S to N
v0Maneuver = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, intersection.maneuvers))
v0InitLane = v0Maneuver.startLane
v0Trajectory = [v0InitLane, v0Maneuver.connectingLane, v0Maneuver.endLane]
v0SpawnPt = OrientedPoint in v0InitLane.centerline

# v1: straight from W to E or E to W
v1InitLane = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT,
             Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, v0InitLane.maneuvers)).conflictingManeuvers)).startLane
v1Maneuver = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, v1InitLane.maneuvers))
v1Trajectory = [v1InitLane, v1Maneuver.connectingLane, v1Maneuver.endLane]
v1SpawnPt = OrientedPoint in v1InitLane.centerline

# v2: straight from E to W or W to E (reverse to v1)
v2InitLane = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, v1Maneuver.reverseManeuvers)).startLane
v2Maneuver = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, v2InitLane.maneuvers))
v2Trajectory = [v2InitLane, v2Maneuver.connectingLane, v2Maneuver.endLane]
v2SpawnPt = OrientedPoint in v2InitLane.centerline

# v3: behind v0
v3InitLane = v0InitLane
v3Maneuver = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, v3InitLane.maneuvers))
v3Trajectory = [v3InitLane, v3Maneuver.connectingLane, v3Maneuver.endLane]

#################################
# SCENARIO SPECIFICATION        #
#################################

ego = Car at v0SpawnPt,
    with blueprint MODEL,
    with behavior VehicleBehavior(v0Trajectory, 0)

v1 = Car at v1SpawnPt,
    with blueprint MODEL,
    with behavior VehicleBehavior(v1Trajectory, 1)

v2 = Car at v2SpawnPt,
    with blueprint MODEL,
    with behavior VehicleBehavior(v2Trajectory, 2)

v3 = Car following roadDirection for v3_DIST,
    with blueprint MODEL,
    with behavior FollowBehavior(v3Trajectory, 3, ego)

require INIT_DIST[0] <= (distance from ego to intersection) <= INIT_DIST[1]
require INIT_DIST[0] <= (distance from v1 to intersection) <= INIT_DIST[1]
require INIT_DIST[0] <= (distance from v2 to intersection) <= INIT_DIST[1]
terminate when (distance to v0SpawnPt) > TERM_DIST and HAS_PASSED[0] and HAS_PASSED[1] and HAS_PASSED[2] and HAS_PASSED[3]

#################################
# RECORDING                     #
#################################

record final ARRIVING_ORDER as arrivingOrder
record final PASSING_ORDER as passingOrder
record final HAS_PASSED as hasPassed
record ((distance from ego to intersection) == 0) as v0IsInIntersection
record ((distance from v1 to intersection) == 0)  as v1IsInIntersection
record ((distance from v2 to intersection) == 0)  as v2IsInIntersection
record ((distance from v3 to intersection) == 0)  as v3IsInIntersection
