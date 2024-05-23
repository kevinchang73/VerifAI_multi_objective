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


z_offset = 0.32
destination = (6, 4, z_offset)
target_orientation = 0

param TABLE_YAW = VerifaiRange(0, 180)
param TABLE_Y = VerifaiRange(0, 1.5)

region_center = (1, 4.5, z_offset)

restricted_region = RectangularRegion(region_center, 0, 1.5, 1.5)

ego = new HSR_Robot on (0, 0, z_offset), with yaw -90 deg, with behavior NavTo(destination)

# TODO add some horizontal distributions to the table. 
# could try to force errors in restriction zone, 'hesitation', and collision
table = new KitchenTable on (5, globalParameters.TABLE_Y, z_offset), with yaw globalParameters.TABLE_YAW deg 

terminate after 500 steps

record ego intersects restricted_region.footprint as trespass
record distance from ego to table as table_dist
record ego.boundingCircle.intersection(table).size as ego_too_close
# record ego intersects table as ego_too_close
record (ego.position - destination).norm() as dist_to_goal
