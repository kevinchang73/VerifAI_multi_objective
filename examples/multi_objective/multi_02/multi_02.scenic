"""
TITLE: Multi 02
AUTHOR: Kai-Chun Chang, kaichunchang@berkeley.edu
DESCRIPTION: Ego vehicle performs a lane change to bypass a slow 
adversary vehicle but cannot return to its original lane because 
the adversary accelerates. Ego vehicle must then slow down to avoid 
collision with leading vehicle in new lane.
SOURCE: Based on Francis Indaheng's code, NHSTA, #16
"""

#################################
# MAP AND MODEL                 #
#################################

param map = localPath('../maps/Town03.xodr')
param carla_map = 'Town03'
param N = 4
model scenic.domains.driving.model
#model scenic.simulators.carla.model

#################################
# CONSTANTS                     #
#################################

MODEL = 'vehicle.lincoln.mkz_2017'

param EGO_SPEED = VerifaiRange(7, 10)
param EGO_BRAKE = VerifaiRange(0.7, 1.0)

ADV1_DIST = 12
ADV2_DIST = -6
ADV3_DIST = ADV1_DIST + 10
param ADV_SPEED = VerifaiRange(3, 6)

LEAD_SPEED = globalParameters.EGO_SPEED - 4

BYPASS_DIST = 10
SAFE_DIST = 10
INIT_DIST = 40
TERM_DIST = 80

#################################
# AGENT BEHAVIORS               #
#################################

behavior DecelerateBehavior(brake):
    take SetBrakeAction(brake)

behavior EgoBehavior():
    try:
        do FollowLaneBehavior(target_speed=globalParameters.EGO_SPEED)
    interrupt when (distance from adv2 to ego) > BYPASS_DIST:
        fasterLaneSec = self.laneSection.fasterLane
        do LaneChangeBehavior(
                laneSectionToSwitch=fasterLaneSec,
                target_speed=globalParameters.EGO_SPEED)
        try:
            do FollowLaneBehavior(
                    target_speed=globalParameters.EGO_SPEED,
                    laneToFollow=fasterLaneSec.lane)
        interrupt when (distance from adv3 to ego) < SAFE_DIST:
            do DecelerateBehavior(brake=globalParameters.EGO_BRAKE)
    interrupt when (distance from adv1 to ego) < SAFE_DIST:
        do DecelerateBehavior(brake=globalParameters.EGO_BRAKE)

behavior Adv1Behavior():
    do FollowLaneBehavior(target_speed=globalParameters.ADV_SPEED)

behavior Adv2Behavior():
    fasterLaneSec = self.laneSection.fasterLane
    do LaneChangeBehavior(
            laneSectionToSwitch=fasterLaneSec,
            target_speed=globalParameters.ADV_SPEED)
    do FollowLaneBehavior(target_speed=globalParameters.ADV_SPEED)

#################################
# SPATIAL RELATIONS             #
#################################

initLane = Uniform(*network.lanes)
egoSpawnPt = OrientedPoint in initLane.centerline

#################################
# SCENARIO SPECIFICATION        #
#################################

ego = Car at egoSpawnPt,
    with blueprint MODEL,
    with behavior EgoBehavior()

adv1 = Car following roadDirection for ADV1_DIST,
    with blueprint MODEL,
    with behavior Adv1Behavior()

adv2 = Car following roadDirection for ADV2_DIST,
    with blueprint MODEL,
    with behavior Adv2Behavior()

adv3 = Car following roadDirection for ADV3_DIST,
    with blueprint MODEL,
    with behavior Adv2Behavior()

require (distance to intersection) > INIT_DIST
require (distance from adv1 to intersection) > INIT_DIST
require (distance from adv2 to intersection) > INIT_DIST
require (distance from adv3 to intersection) > INIT_DIST
require always (adv1.laneSection._fasterLane is not None)
terminate when (distance to egoSpawnPt) > TERM_DIST

#################################
# RECORDING                     #
#################################

record initial (adv2.lane.polygon.exterior.coords) as egoStartLaneCoords
record final (adv2.lane.polygon.exterior.coords) as egoEndLaneCoords
record (ego.lane is initLane) as egoIsInInitLane
record (adv2.lane is initLane) as adv2IsInInitLane # start evaluation only when adv2 reaches another lane
record (adv3.lane is initLane) as adv3IsInInitLane # start evaluation only when adv3 reaches another lane
