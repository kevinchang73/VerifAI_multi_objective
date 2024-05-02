import magnum as mn
import numpy as np
model scenic.simulators.habitat.model
from scenic.simulators.habitat.actions import *
from scenic.simulators.habitat.behaviors import *
from scenic.simulators.habitat.model import *
from scenic.simulators.habitat.utils import scenic_to_habitat_map
from scenic.core.vectors import Vector
import math
import time


behavior SpotHandOver():
    # raise_pos = np.array([0.0, -3.14, 0.00, 3.14, 0.0, 0.0, 0.0]) # initial pos
    raise_pos = np.array([0.0, -3.14, 0.00, 1.57, 0.0, 0.0, 0.0]) # forarm raise
    do MoveToJointAngles(raise_pos)

    raise_pos = [0.0, -1.3, 0.0, 1.8, 0.0, 0.0, 0.0] # shoulder raise
    do MoveToJointAngles(raise_pos)
    


behavior SpotPickUp():
    raise_pos = np.array([0.0, -3.14, 0.00, 1.57, 0.0, 0.0, 0.0]) # forarm raise
    do MoveToJointAngles(raise_pos)
    
    raise_pos = [0.0, -1.0, 0.0, 1.57, 0.0, 0.0, 0.0] # shoulder raise
    do MoveToJointAngles(raise_pos)
    
    # spot_ee_pos = self.ee_pos
    box_pos = box.position
    # diff_pos = box_pos - spot_ee_pos
    diff_pos = box_pos - self.ee_pos
    diff_norm = np.linalg.norm(np.array([diff_pos[0], diff_pos[1], diff_pos[2]]))  
    print(f"pos_difference norm: {diff_norm}")
    if diff_norm < 0.25:
        take SnapToObjectAction(box)

    self._holding_object = True

    raise_pos = np.array([0.0, -3.14, 0.00, 3.14, 0.0, 0.0, 0.0]) # retract_arm
    do MoveToJointAngles(raise_pos, steps=50)



behavior NavToHuman():
    position = ego.position
    x, y, z = position[0], position[1], position[2]
    do RobotNav(x, y, z)

behavior GrabAndNav():
    do SpotPickUp()
    # for _ in range(50):
        # wait
    try:
        while True:
            wait
    interrupt when ego._in_position:
        do NavToHuman()
        do SpotHandOver()
        terminate

behavior MoveToJointAngles(joint_angles, steps=20):
    start_pos = np.array(self._articulated_agent.arm_joint_pos)
    delta_pos = (joint_angles - start_pos)/steps
    for _ in range(steps):
        new_pos = list(start_pos + delta_pos)
        take SpotMoveArmAction(arm_ctrl_angles=new_pos)
        start_pos = np.array(self._articulated_agent.arm_joint_pos)
        
behavior ReachHandAndWalk(walk_position, reach_position):
    try:
        reach_x = reach_position[0]
        reach_y = reach_position[1]
        reach_z = reach_position[2]
        print('Reaching')
        do HumanReach(x=reach_x, y=reach_y, z=reach_z, index_hand=0)
        while True:
            wait

    interrupt when spot._holding_object:
        take HumanStopAction()
        walk_x = walk_position[0]
        walk_y = walk_position[1]
        walk_z = walk_position[2]

        do HumanNav(x=walk_x, y=walk_y, z=walk_z)
        self._in_position = True
        # terminate
        while True:
            wait
    

behavior Traverse():
    while True:
        # x, y, z = point1
        # do RobotNav(x=x, y=y, z=z)
        do GoRel(y=1.0)
        do TurnAround()
        do GoRel(y=-1.0)
        do TurnAround()
        



# ego = new Female_0 at (-0.5, -4.8, 0), with yaw -90 deg,
                                # with behavior ReachHandAndWalk((-4.5, -3.0, 0), (-0.5, -0.5, 0.5))

param EGO_DEST_X = VerifaiRange(-4.5, -4.0)

param EGO_SPAWN_X = VerifaiRange(-0.5, 0.5)
param FETCH_SPAWN_Y = VerifaiRange(-2.5, -5.0)
param BOX_X = VerifaiRange(0.12, 0.42) # make the lower bound the original center so it does not fall off of bed
param BOX_Y = VerifaiRange(-5.8, 5.2) 

ego = new Female_0 at (globalParameters.EGO_SPAWN_X, -4.8, 0), with yaw -90 deg,
                                with behavior ReachHandAndWalk((globalParameters.EGO_DEST_X, -3.0, 0), (-0.5, -0.5, 0.5))

# box_region = RectangularRegion((0.12, -5.5, 0.61), 0, 0.2, 0.2)
# box = new GelatinBox on box_region
box = new GelatinBox on (globalParameters.BOX_X, globalParameters.BOX_Y, 0.61)
spot = new SpotRobot at (-0.9, -5.5, 0), with behavior GrabAndNav()
fetch = new FetchRobot at (-3.7, globalParameters.FETCH_SPAWN_Y, 0), with yaw 90 deg, with behavior Traverse()

record distance from spot to fetch as bot_dist
record (ego.ee_pos - spot.ee_pos).norm() as ee_dist
record (spot.ee_pos - box.position).norm() as box_dist
record spot._holding_object as spot_hold
record ego._in_position as human_in_pos
