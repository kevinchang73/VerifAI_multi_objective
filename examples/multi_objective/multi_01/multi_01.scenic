"""
TITLE: Multi 01
AUTHOR: Kai-Chun Chang, kaichunchang@berkeley.edu
DESCRIPTION: 
SOURCE: CARLA Challenge Scenario 6: https://carlachallenge.org/challenge/nhtsa/
"""

#################################
# MAP AND MODEL                 #
#################################

param map = localPath('../maps/Town07.xodr')
param carla_map = 'Town07'
param N = 2
model scenic.simulators.carla.model
#model scenic.simulators.newtonian.driving_model

#################################
# CONSTANTS                     #
#################################

MODEL = 'vehicle.lincoln.mkz_2017'

param EGO_SPEED = VerifaiRange(6, 9) #7
param DIST_THRESHOLD = VerifaiRange(12, 14) #13
param BLOCKING_CAR_DIST = VerifaiRange(15, 20)
param BYPASS_DIST = VerifaiRange(4, 6) #5

DIST_TO_INTERSECTION = 15
TERM_DIST = 40

#################################
# AGENT BEHAVIORS               #
#################################

behavior EgoBehavior(path):
    current_lane = network.laneAt(self)
    laneChangeCompleted = False
    bypassed = False
    try:
        do FollowLaneBehavior(globalParameters.EGO_SPEED, laneToFollow=current_lane)
    interrupt when (distance to blockingCar) < globalParameters.DIST_THRESHOLD and not laneChangeCompleted:
        do LaneChangeBehavior(path, is_oppositeTraffic=True, target_speed=globalParameters.EGO_SPEED)
        do FollowLaneBehavior(globalParameters.EGO_SPEED, is_oppositeTraffic=True) until (distance to blockingCar) > globalParameters.BYPASS_DIST
        laneChangeCompleted = True
    interrupt when (blockingCar can see ego) and (distance to blockingCar) > globalParameters.BYPASS_DIST and not bypassed:
        current_laneSection = network.laneSectionAt(self)
        rightLaneSec = current_laneSection._laneToLeft
        do LaneChangeBehavior(rightLaneSec, is_oppositeTraffic=False, target_speed=globalParameters.EGO_SPEED)
        bypassed = True

#################################
# SPATIAL RELATIONS             #
#################################

#Find lanes that have a lane to their left in the opposite direction
laneSecsWithLeftLane = []
for lane in network.lanes:
    for laneSec in lane.sections:
        if laneSec._laneToLeft is not None:
            if laneSec._laneToLeft.isForward is not laneSec.isForward:
                laneSecsWithLeftLane.append(laneSec)

assert len(laneSecsWithLeftLane) > 0, \
    'No lane sections with adjacent left lane with opposing \
    traffic direction in network.'

initLaneSec = Uniform(*laneSecsWithLeftLane)
leftLaneSec = initLaneSec._laneToLeft

spawnPt = OrientedPoint on initLaneSec.centerline

#################################
# SCENARIO SPECIFICATION        #
#################################

ego = Car at spawnPt,
    with blueprint MODEL,
    with behavior EgoBehavior(leftLaneSec)
    
blockingCar = Car following roadDirection from ego for globalParameters.BLOCKING_CAR_DIST,
            with blueprint MODEL,
            with viewAngle 90 deg

require (distance from blockingCar to intersection) > DIST_TO_INTERSECTION
terminate when (distance to spawnPt) > TERM_DIST

#################################
# RECORDING                     #
#################################

record initial (initLaneSec.polygon.exterior.coords) as initLaneCoords
record initial (leftLaneSec.polygon.exterior.coords) as leftLaneCoords
record (ego.lane is initLaneSec.lane) as egoIsInInitLane
record (ego.lane is leftLaneSec.lane) as egoIsInLeftLane
