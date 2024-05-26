model scenic.simulators.hsr.model

from scenic.simulators.hsr.model import *
from scenic.simulators.hsr.behaviors import *
from scenic.simulators.hsr.actions import *
import math
import time
import matplotlib.pyplot as plt

"""
have the HSR travel to a specific region without going through a restricted zone
if blocked, then go to restricted zone
"""

behavior NavTo(dest):
    try:
        while True:
            do GoRel(x=1) # probably do GoRel 0.5?

    interrupt when self.distanceToClosest(KitchenTable) <= 2:
        take CancelGoalAction()
        x = dest[0]
        y = dest[1]
        # TODO specify a time out?
        do GoAbs(x=x, y=y, yaw=0.0)
        terminate


# param TABLE_X = VerifaiRange(5, 6.5)
param TABLE_X = VerifaiRange(3, 6.5)
param TABLE_Y = VerifaiRange(-0.5, 1.5)
param TABLE_YAW = VerifaiRange(0, 180)

param TABLE_2_X = VerifaiRange(3, 6.5)
param TABLE_2_Y = VerifaiRange(-0.5, 1.5)
param TABLE_2_YAW = VerifaiRange(0, 180)

param EGO_Y = VerifaiRange(-0.3, 1) 

'''
Defining necessary regions
'''
z_offset = 0.32
destination = (6, 4, z_offset)
target_orientation = 0

# center_unit_region = RectangularRegion((3, 3, z_offset), 0, 1.5, 1.5)
center_unit_region = RectangularRegion((3, 3, z_offset), 0, 3.0, 3.0)
tree_region = CircularRegion((6.5, 0, z_offset), 0.5)
corridor_shelf_region = RectangularRegion((1.5, -0.84, z_offset), 0, 3, 0.32)

restricted_region = RectangularRegion((1, 5.0, z_offset), 0, 3, 3)

ego = new HSR_Robot on (0, globalParameters.EGO_Y, z_offset), with yaw -90 deg, with behavior NavTo(destination)

# table = new HighTable on (globalParameters.TABLE_X, globalParameters.TABLE_Y, z_offset), with yaw globalParameters.TABLE_YAW deg 
table = new KitchenTable on (globalParameters.TABLE_X, globalParameters.TABLE_Y, z_offset), with yaw globalParameters.TABLE_YAW deg 

table2 = new KitchenTable on (globalParameters.TABLE_2_X, globalParameters.TABLE_2_Y, z_offset), 
                                        with yaw globalParameters.TABLE_2_YAW deg,
                                        with name 'KitchenTable102'

OBSTACLES = [table, table2]


terminate after 800 steps

require not (table intersects center_unit_region.footprint)
require not (table intersects tree_region.footprint)
require not (table intersects corridor_shelf_region.footprint)

require not (table2 intersects center_unit_region.footprint)
require not (table2 intersects tree_region.footprint)
require not (table2 intersects corridor_shelf_region.footprint)

require distance from table to ego >= 2.5
require distance from table2 to ego >= 2.5

record ego intersects restricted_region.footprint as trespass
record max([ego.boundingCircle.intersect(obs.occupiedSpace).size for obs in OBSTACLES]) as ego_too_close
record min([(distance from ego to obs) for obs in OBSTACLES]) as table_dist
record (ego.position - destination).norm() as dist_to_goal

