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
    do GoAbs(x=x, y=y, yaw=0.0)
    terminate


TABLE_X = Range(5, 6.5)
TABLE_Y = Range(0, 1.5)
TABLE_YAW = Range(0, 180)

CHAIR_X = Range(5, 6.5)
CHAIR_Y = Range(0, 3)
CHAIR_YAW = Range(0, 180)

CHAIR_2_X = Range(5, 6.5)
CHAIR_2_Y = Range(0, 3)
CHAIR_2_YAW = Range(0, 180)

EGO_Y = Range(-2, 0)
EGO_X = Range(0, 0.5)

HSR_Y = Range(-2, 0)
HSR_X = Range(0, 0.5)

z_offset = 0.32
destination = (6, 4, z_offset)
target_orientation = 0
center_unit_region = RectangularRegion((3, 3, z_offset), 0, 1.5, 1.5)
tree_region = CircularRegion((6.5, 0, z_offset), 0.5)

region_center = (1, 4.5, z_offset)

restricted_region = RectangularRegion(region_center, 0, 1.5, 1.5)

# ego = new HSR_Robot on (1, 1, z_offset), with yaw -90 deg, with behavior NavTo(destination)
ego = new HSR_Robot on (HSR_X, HSR_Y, z_offset), 
                                with yaw -90 deg, with behavior NavTo(destination),
                                with sampled_EGO_X EGO_X,
                                with sampled_EGO_Y EGO_Y

# TODO add some horizontal distributions to the table. 
# could try to force errors in restriction zone, 'hesitation', and collision
# table = new KitchenTable on (5, TABLE_Y, z_offset), with yaw TABLE_YAW deg 
table = new KitchenTable on (TABLE_X, TABLE_Y, z_offset), with yaw TABLE_YAW deg 
chair = new Chair on (CHAIR_X, CHAIR_Y, z_offset), with yaw CHAIR_YAW deg 
chair2 = new Chair on (CHAIR_2_X, CHAIR_2_Y, z_offset), with name 'Chair102',
                                                        with yaw CHAIR_2_YAW deg 
OBSTACLES = [table, chair, chair2]


terminate after 600 steps

require not (table intersects center_unit_region.footprint)
require not (table intersects tree_region.footprint)
require not (chair intersects center_unit_region.footprint)
require not (chair intersects tree_region.footprint)
require not (chair2 intersects center_unit_region.footprint)
require not (chair2 intersects tree_region.footprint)

record ego intersects restricted_region.footprint as trespass
record distance from ego to table as table_dist
# record ego intersects table as ego_too_close
record max([ego.boundingCircle.intersect(obs.occupiedSpace).size for obs in OBSTACLES]) as ego_too_close

record (ego.position - destination).norm() as dist_to_goal
