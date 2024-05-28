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


# param TABLE_X = VerifaiRange(5, 6.5)
# param TABLE_X = VerifaiRange(3, 4)
param TABLE_Y = VerifaiRange(0.2, 0.5)
param TABLE_YAW = VerifaiRange(0, 180)

# param TABLE_2_X = VerifaiRange(5.5, 5.5)
param TABLE_2_Y = VerifaiRange(1.0, 1.5)
param TABLE_2_YAW = VerifaiRange(0, 180)

param EGO_Y = VerifaiRange(-0.3, 1) 

# param WAYPOINT = VerifaiRange(1, 2)
param WAYPOINT = VerifaiRange(0.7, 2)

behavior NavTo(dest):
    try:
        do GoRel(x=2) # probably do GoRel 0.5?
        do GoRel(0.5)
        # do GoRel(0.)
        # do GoRel(x=1)
        # do GoRel(0.5)
        # for _ in range (2):
            # print("NAVING!!!")
            # do GoRel(x=1) # probably do GoRel 0.5?

        x = dest[0]
        y = dest[1]
        # TODO specify a time out?
        do GoAbs(x=x, y=y, yaw=0.0)
        terminate

    interrupt when (self.distanceToClosest(KitchenTable) <= globalParameters.WAYPOINT or \
                     ego.boundingCircle.intersect(self.getClosest(KitchenTable).occupiedSpace).size > 0  ):
        print('CANCELLING!!!')
        take CancelGoalAction()
        x = dest[0]
        y = dest[1]
        # TODO specify a time out?
        do GoAbs(x=x, y=y, yaw=0.0)
        terminate


'''
Defining necessary regions
'''
z_offset = 0.32
destination = (6, 4, z_offset)
target_orientation = 0

# center_unit_region = RectangularRegion((3, 3, z_offset), 0, 1.5, 1.5)
# center_unit_region = RectangularRegion((3, 3, z_offset), 0, 3.0, 3.0)
# tree_region = CircularRegion((6.5, 0, z_offset), 0.5)
corridor_shelf_region = RectangularRegion((1.5, -0.84, z_offset), 0, 3, 0.32)

restricted_region = RectangularRegion((3, 5.0, z_offset), 0, 4, 4)

ego = new HSR_Robot on (0, globalParameters.EGO_Y, z_offset), with yaw -90 deg, with behavior NavTo(destination)

table = new KitchenTable on (3, globalParameters.TABLE_Y, z_offset), with yaw globalParameters.TABLE_YAW deg 
# table = new KitchenTable on (globalParameters.TABLE_X, globalParameters.TABLE_Y, z_offset), with yaw globalParameters.TABLE_YAW deg 
# table = new KitchenTable on (3, 0.7, z_offset), with yaw 90 deg 

table2 = new KitchenTable on (6, globalParameters.TABLE_2_Y, z_offset), 
                                        with yaw globalParameters.TABLE_2_YAW deg,
                                        with name 'KitchenTable102'

OBSTACLES = [table, table2]


terminate after 800 steps

record ego intersects restricted_region.footprint as trespass
record max([ego.boundingCircle.intersect(obs.occupiedSpace).size for obs in OBSTACLES]) as ego_too_close
record min([(distance from ego to obs) for obs in OBSTACLES]) as table_dist
record (ego.position - destination).norm() as dist_to_goal

