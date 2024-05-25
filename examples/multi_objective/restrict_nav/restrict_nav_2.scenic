model scenic.simulators.hsr.model

from scenic.simulators.hsr.model import *
from scenic.simulators.hsr.behaviors import *
from scenic.simulators.hsr.actions import *
import math
import time


"""
have the HSR travel to a specific region without going through a restricted zone
if blocked, then go to restricted zone
"""

behavior NavTo(dest):
    x = dest[0]
    y = dest[1]
    # TODO specify a time out?
    do GoAbs(x=x, y=y, yaw=0.0)
    terminate


param TABLE_X = VerifaiRange(4, 6)
param TABLE_Y = VerifaiRange(5, 7)
param TABLE_YAW = VerifaiRange(0, 180)

param CHAIR_X = VerifaiRange(4, 6)
param CHAIR_Y = VerifaiRange(5, 7)
param CHAIR_YAW = VerifaiRange(0, 180)

param CHAIR_2_X = VerifaiRange(4, 6)
param CHAIR_2_Y = VerifaiRange(5, 7)
param CHAIR_2_YAW = VerifaiRange(0, 180)

# param EGO_Y = VerifaiRange(0, 2) # TODO good for testing retricted area, bad for efficient path planning
param EGO_Y = VerifaiRange(3, 5) 
# param EGO_X = VerifaiRange(0, 0.5)


z_offset = 0.32
destination = (6, 4, z_offset)
target_orientation = 0
center_unit_region = RectangularRegion((3, 3, z_offset), 0, 1.5, 1.5)
tree_region = CircularRegion((1.7, 5, z_offset), 0.5)

stair_region = RectangularRegion((2, 9, z_offset), 1.57, 1, 2.5) # worst case, squaire region centered far away

restricted_region_center = (4, 0, z_offset)
restricted_region = RectangularRegion(restricted_region_center, 1.57, 1.3, 5)

ego = new HSR_Robot on (0, globalParameters.EGO_Y, z_offset), with yaw -90 deg, with behavior NavTo(destination)

table = new KitchenTable on (globalParameters.TABLE_X, globalParameters.TABLE_Y, z_offset), with yaw globalParameters.TABLE_YAW deg 
chair = new Chair on (globalParameters.CHAIR_X, globalParameters.CHAIR_Y, z_offset), with yaw globalParameters.CHAIR_YAW deg 
chair2 = new Chair on (globalParameters.CHAIR_2_X, globalParameters.CHAIR_2_Y, z_offset), with name 'Chair102',
                                                        with yaw globalParameters.CHAIR_2_YAW deg 
OBSTACLES = [table, chair, chair2]

terminate after 600 steps

require not (table intersects center_unit_region.footprint)
require not (table intersects tree_region.footprint)
require not (table intersects stair_region.footprint)

require not (chair intersects center_unit_region.footprint)
require not (chair intersects tree_region.footprint)
require not (chair intersects stair_region.footprint)

require not (chair2 intersects center_unit_region.footprint)
require not (chair2 intersects tree_region.footprint)
require not (chair2 intersects stair_region.footprint)

record ego intersects restricted_region.footprint as trespass
record distance from ego to table as table_dist
record (ego.position - destination).norm() as dist_to_goal
