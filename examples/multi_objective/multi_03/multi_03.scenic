"""
TITLE: Multi 03
AUTHOR: Kai-Chun Chang, kaichunchang@berkeley.edu
DESCRIPTION: Ego vehicle makes a left turn at a 4-way intersection while 
one adversary vehicle from opposite lane goes straight and two adversary
vehicles from lateral lane (they are on opposite lanes to each other) go straight.
SOURCE: 
"""

#################################
# MAP AND MODEL                 #
#################################

param map = localPath('../maps/Town05.xodr')
param carla_map = 'Town05'
param verifaiSamplerType = 'halton'
param N = 3
model scenic.domains.driving.model
#model scenic.simulators.carla.model

#################################
# CONSTANTS                     #
#################################

MODEL = 'vehicle.lincoln.mkz_2017'

EGO_INIT_DIST = [15, 25] #[20, 25]
param EGO_SPEED = VerifaiRange(7, 10)
param EGO_BRAKE = VerifaiRange(0.5, 1.0)

ADV_INIT_DIST = [10, 20] #[10, 15]
param ADV_SPEED = VerifaiRange(7, 10)

param SAFETY_DIST = VerifaiRange(10, 20) #15
CRASH_DIST = 5
TERM_DIST = 50 #70

#################################
# AGENT BEHAVIORS               #
#################################

behavior EgoBehavior(trajectory):
    try:
        do FollowTrajectoryBehavior(target_speed=globalParameters.EGO_SPEED, trajectory=trajectory)
    interrupt when withinDistanceToAnyObjs(self, globalParameters.SAFETY_DIST):
        take SetBrakeAction(globalParameters.EGO_BRAKE)
    #interrupt when withinDistanceToAnyObjs(self, CRASH_DIST):
    #    terminate

#################################
# SPATIAL RELATIONS             #
#################################

intersection = Uniform(*filter(lambda i: i.is4Way, network.intersections))

# ego: left turn
egoInitLane = Uniform(*intersection.incomingLanes)
egoManeuver = Uniform(*filter(lambda m: m.type is ManeuverType.LEFT_TURN, egoInitLane.maneuvers))
egoTrajectory = [egoInitLane, egoManeuver.connectingLane, egoManeuver.endLane]
egoSpawnPt = OrientedPoint in egoInitLane.centerline

# adv 1: conflicting maneuver of ego, go straight
adv1InitLane = Uniform(*filter(lambda m:
        m.type is ManeuverType.STRAIGHT,
        Uniform(*filter(lambda m: 
            m.type is ManeuverType.STRAIGHT, 
            egoInitLane.maneuvers)
        ).conflictingManeuvers)
    ).startLane
adv1Maneuver = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, adv1InitLane.maneuvers))
adv1Trajectory = [adv1InitLane, adv1Maneuver.connectingLane, adv1Maneuver.endLane]
adv1SpawnPt = OrientedPoint in adv1InitLane.centerline

# adv 2: reverse maneuver of adv 1, go straight
adv2InitLane = Uniform(*filter(lambda m:
		m.type is ManeuverType.STRAIGHT,
		adv1Maneuver.reverseManeuvers)
	).startLane
adv2Maneuver = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, adv2InitLane.maneuvers))
adv2Trajectory = [adv2InitLane, adv2Maneuver.connectingLane, adv2Maneuver.endLane]
adv2SpawnPt = OrientedPoint in adv2InitLane.centerline

# adv 3: reverse maneuver of ego, go straight
adv3InitLane = Uniform(*filter(lambda m:
        m.type is ManeuverType.STRAIGHT,
        Uniform(*filter(lambda m: 
            m.type is ManeuverType.STRAIGHT, 
            egoInitLane.maneuvers)
        ).reverseManeuvers)
    ).startLane
adv3Maneuver = Uniform(*filter(lambda m: m.type is ManeuverType.STRAIGHT, adv3InitLane.maneuvers))
adv3Trajectory = [adv3InitLane, adv3Maneuver.connectingLane, adv3Maneuver.endLane]
adv3SpawnPt = OrientedPoint in adv3InitLane.centerline

#################################
# SCENARIO SPECIFICATION        #
#################################

ego = Car at egoSpawnPt,
    with blueprint MODEL,
    with behavior EgoBehavior(egoTrajectory)

adversary1 = Car at adv1SpawnPt,
    with blueprint MODEL,
    with behavior FollowTrajectoryBehavior(target_speed=globalParameters.ADV_SPEED, trajectory=adv1Trajectory)

adversary2 = Car at adv2SpawnPt,
    with blueprint MODEL,
    with behavior FollowTrajectoryBehavior(target_speed=globalParameters.ADV_SPEED, trajectory=adv2Trajectory)

adversary3 = Car at adv3SpawnPt,
    with blueprint MODEL,
    with behavior FollowTrajectoryBehavior(target_speed=globalParameters.ADV_SPEED, trajectory=adv3Trajectory)

require EGO_INIT_DIST[0] <= (distance to intersection) <= EGO_INIT_DIST[1]
require ADV_INIT_DIST[0] <= (distance from adversary1 to intersection) <= ADV_INIT_DIST[1]
require ADV_INIT_DIST[0] <= (distance from adversary2 to intersection) <= ADV_INIT_DIST[1]
require ADV_INIT_DIST[0] <= (distance from adversary3 to intersection) <= ADV_INIT_DIST[1]
require adv1InitLane.road is egoManeuver.endLane.road
require egoManeuver.endLane is adv2Maneuver.endLane

#################################
# RECORDING                     #
#################################

centroidX = intersection.polygon.centroid.x
centroidY = intersection.polygon.centroid.y
interCoords = intersection.polygon.exterior.coords
startRoadCoords = egoInitLane.road.polygon.exterior.coords
endRoadCoords = egoManeuver.endLane.road.polygon.exterior.coords
startLaneGroupCoords = egoInitLane.group.polygon.exterior.coords
endLaneGroupCoords = egoManeuver.endLane.group.polygon.exterior.coords
record (distance to intersection) as egotoInter
record initial (centroidX) as interCentroidX
record initial (centroidY) as interCentroidY
record initial (interCoords) as interCoords
record initial (startRoadCoords) as startRoadCoords
record initial (endRoadCoords) as endRoadCoords
record initial (startLaneGroupCoords) as startLaneGroupCoords
record initial (endLaneGroupCoords) as endLaneGroupCoords

terminate when (distance to egoSpawnPt) > TERM_DIST
