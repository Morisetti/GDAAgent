# A simple agent that maneuvers around a more complex obstacle course.

import MalmoPython
import os
import sys
import time
import json
import math

import GDAUtilities as GDAU

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # Flush print output immediately

# Agent specific constants
OBS_RANGE = 1
GRID_NAME = 'nearbyBlocks'

missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>

              <ServerSection>
        <ServerInitialConditions>
            <Time>
                <StartTime>12000</StartTime>
                <AllowPassageOfTime>false</AllowPassageOfTime>
            </Time>
            <Weather>clear</Weather>
        </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;,biome_1"/>
                    <DrawingDecorator>
                        <DrawCuboid x1="-6" y1="55" z1="1" x2="4" y2="55" z2="1" type="lava"/> 
                        <DrawCuboid x1="-6" y1="55" z1="4" x2="4" y2="55" z2="4" type="lava"/> 
                        <DrawCuboid x1="-6" y1="55" z1="7" x2="4" y2="55" z2="7" type="lava"/> 
                        <DrawCuboid x1="-6" y1="56" z1="11" x2="4" y2="56" z2="11" type="stone"/>
                        <DrawCuboid x1="-3" y1="56" z1="15" x2="0" y2="56" z2="15" type="stone"/>
                        <DrawCuboid x1="-1" y1="57" z1="15" x2="0" y2="57" z2="15" type="stone"/>
                        <DrawCuboid x1="-3" y1="56" z1="19" x2="0" y2="56" z2="19" type="stone"/>
                        <DrawCuboid x1="-3" y1="57" z1="19" x2="-2" y2="57" z2="19" type="stone"/>
                        <DrawCuboid x1="-5" y1="56" z1="23" x2="3" y2="57" z2="30" type="stone"/>
                        <DrawCuboid x1="-6" y1="56" z1="24" x2="4" y2="57" z2="29" type="diamond_block"/>
                        <DrawCuboid x1="-6" y1="56" z1="23" x2="-6" y2="66" z2="23" type="quartz_block"/>
                        <DrawCuboid x1="4" y1="56" z1="23" x2="4" y2="66" z2="23" type="quartz_block"/>
                        <DrawCuboid x1="-6" y1="66" z1="23" x2="4" y2="66" z2="23" type="quartz_block"/>
                        <DrawCuboid x1="-6" y1="56" z1="30" x2="-6" y2="66" z2="30" type="quartz_block"/>
                        <DrawCuboid x1="4" y1="56" z1="30" x2="4" y2="66" z2="30" type="quartz_block"/>
                        <DrawCuboid x1="-6" y1="66" z1="30" x2="4" y2="66" z2="30" type="quartz_block"/>
                        <DrawCuboid x1="-6" y1="66" z1="23" x2="-6" y2="66" z2="30" type="quartz_block"/>
                        <DrawCuboid x1="4" y1="66" z1="23" x2="4" y2="66" z2="30" type="quartz_block"/>
                        <DrawCuboid x1="-5" y1="66" z1="24" x2="3" y2="66" z2="29" type="quartz_block"/>
                        <DrawCuboid x1="-5" y1="58" z1="23" x2="-5" y2="58" z2="23" type="torch"/>
                        <DrawCuboid x1="-5" y1="58" z1="29" x2="-5" y2="58" z2="29" type="torch"/>
                        <DrawCuboid x1="3" y1="58" z1="23" x2="3" y2="58" z2="23" type="torch"/>
                        <DrawCuboid x1="3" y1="58" z1="29" x2="3" y2="58" z2="29" type="torch"/>
                        <DrawCuboid x1="-6" y1="58" z1="24" x2="-6" y2="65" z2="29" type="stained_glass"/>
                        <DrawCuboid x1="4" y1="58" z1="24" x2="4" y2="65" z2="29" type="stained_glass"/>
                        <DrawCuboid x1="-5" y1="58" z1="30" x2="3" y2="65" z2="30" type="stained_glass"/>
                        <DrawCuboid x1="-3" y1="63" z1="29" x2="1" y2="63" z2="29" type="glowstone"/>
                        <DrawCuboid x1="-3" y1="59" z1="29" x2="1" y2="59" z2="29" type="glowstone"/>
                        <DrawCuboid x1="-3" y1="61" z1="29" x2="-1" y2="61" z2="29" type="glowstone"/>
                        <DrawCuboid x1="-3" y1="59" z1="29" x2="-3" y2="61" z2="29" type="glowstone"/>
                        <DrawCuboid x1="1" y1="59" z1="29" x2="1" y2="63" z2="29" type="glowstone"/>
                    </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="30000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="-1" y="56" z="-3" yaw="0"/>
                    <Inventory>
                        <InventoryItem slot = "0" type = "diamond_pickaxe"/>
                        <InventoryItem slot = "1" type = "diamond_axe"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <ObservationFromFullStats/>
                    <ObservationFromNearbyEntities>
                        <Range name="nearby" xrange="10" yrange="10" zrange="10" update_frequency="1" />
                    </ObservationFromNearbyEntities>
                    <ObservationFromGrid>
                        <Grid name="''' + GRID_NAME + '''">
                            <min x="-'''+str(OBS_RANGE)+'''" y="-'''+str(OBS_RANGE)+'''" z="-'''+str(OBS_RANGE)+'''"/>
                            <max x="'''+str(OBS_RANGE)+'''" y="'''+str(OBS_RANGE)+'''" z="'''+str(OBS_RANGE)+'''"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ObservationFromRay/>
                    <ContinuousMovementCommands turnSpeedDegs="180"/>
                    <AgentQuitFromReachingPosition>
                        <Marker x="-1.0" y="58.0" z="30.0" tolerance="4.0" description="Goal_found"/>
                    </AgentQuitFromReachingPosition>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print 'ERROR:', e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:", e
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text

print
print "Mission running ",

# Location of old position
ox = 0
oy = 0
oz = 0

# Location of targeted block
tx = 0
ty = 0
tz = 0

# Holds the initial yaw and pitch
start_yaw = None
start_pitch = None

# Initialize flags
strafe_flag = 0     # Strafe in a direction
attack_flag = 0     # Attack target block
turn_flag = 0       # Turn to target block
reset_flag = 0      # Reset to original pitch/yaw
lava_flag = 0       # Avoid lava
back_flag = 0       # Back up
mine_flag = 0       # Check conditions of attack
jump_flag = 0       # Jump over lava

agent_host.sendCommand("move 1")
time.sleep(0.5)

# Loop until mission ends:
while world_state.is_mission_running:
    # sys.stdout.write(".")
    time.sleep(0.05)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text

        # Get the necessary data from the observation
        observations = json.loads(msg)
        ax = observations.get(u'XPos')
        az = observations.get(u'ZPos')
        ay = observations.get(u'YPos')
        a_yaw = observations.get(u'Yaw')
        a_pitch = observations.get(u'Pitch')
        raw_obs_grid = observations.get(GRID_NAME)

        grid3d = GDAU.initialize_grid3d(raw_obs_grid, OBS_RANGE)

        # line_of_sight = None

        # if u'LineOfSight' in observations:
        # line_of_sight = observations[u'LineOfSight']

        # At initialization, save the starting yaw and pitch
        if start_yaw is None and start_pitch is None:
            start_yaw = a_yaw
            start_pitch = a_pitch

        # Low level actions
        if strafe_flag == 1:
            if lava_flag == 1:
                if grid3d[OBS_RANGE + 1][OBS_RANGE][OBS_RANGE - 1] != 'lava':
                    agent_host.sendCommand("strafe 0")
                    agent_host.sendCommand("move 1")
                    strafe_flag = 0
                    lava_flag = 0
                    continue
            elif grid3d[OBS_RANGE + 1][OBS_RANGE][OBS_RANGE + 1] == 'air':
                agent_host.sendCommand("strafe 0")
                agent_host.sendCommand("move 1")
                strafe_flag = 0
                continue

        if attack_flag == 1:
            if grid3d[tz][tx][ty] == 'air':
                # The target block was destroyed
                if mine_flag == 1:
                    # Return to moving forward
                    print 'test'
                    agent_host.sendCommand("attack 0")
                    attack_flag = 0
                    reset_flag = 1
                    continue
                elif tx == OBS_RANGE + 1:
                    # The block on the agent's left was destroyed
                    agent_host.sendCommand("attack 0")
                    attack_flag = 0
                    reset_flag = 1
                    continue
                elif tx == OBS_RANGE - 1:
                    # The block on the agent's right was destroyed
                    agent_host.sendCommand("attack 0")
                    tx = OBS_RANGE + 1
                    ty = OBS_RANGE + 1
                    tz = OBS_RANGE + 1
                    attack_flag = 0
                    turn_flag = 1
                    continue
                elif tx == OBS_RANGE:
                    # The block in front of the agent was destroyed
                    agent_host.sendCommand("attack 0")
                    tx = OBS_RANGE - 1
                    ty = OBS_RANGE + 1
                    tz = OBS_RANGE + 1
                    attack_flag = 0
                    turn_flag = 1
                    continue
            else:
                continue

        if turn_flag == 1:
            if mine_flag == 1:
                if grid3d[tz][tx][ty] == 'air':
                    agent_host.sendCommand("turn 0")
                    agent_host.sendCommand("pitch 0")
                    turn_flag = 0
                    mine_flag = 0
                    continue

            yaw_difference = GDAU.find_yaw_difference_to_block(ax, ay, az, a_yaw, tx, ty, tz, OBS_RANGE)
            pitch_difference = GDAU.find_pitch_difference_to_block(ax, ay, az, a_pitch, tx, ty, tz, OBS_RANGE)

            if abs(yaw_difference) < 0.01 and abs(pitch_difference) < 0.01:
                agent_host.sendCommand("turn 0")
                agent_host.sendCommand("pitch 0")
                agent_host.sendCommand("attack 1")
                turn_flag = 0
                attack_flag = 1
                continue

            agent_host.sendCommand("turn " + str(yaw_difference))
            agent_host.sendCommand("pitch " + str(pitch_difference))
            continue

        if reset_flag == 1:
            yaw_difference = GDAU.find_yaw_difference_to_start(a_yaw, start_yaw)
            pitch_difference = GDAU.find_pitch_difference_to_start(a_pitch, start_pitch)

            # print yaw_difference

            if abs(yaw_difference) < 0.005 and abs(pitch_difference) < 0.005:
                agent_host.sendCommand("turn 0")
                agent_host.sendCommand("pitch 0")
                agent_host.sendCommand("move 1")
                reset_flag = 0
                continue

            agent_host.sendCommand("turn " + str(yaw_difference))
            agent_host.sendCommand("pitch " + str(pitch_difference))
            continue

        if back_flag == 1:
            if grid3d[OBS_RANGE][OBS_RANGE - 1][OBS_RANGE - 1] != 'lava' and grid3d[OBS_RANGE][OBS_RANGE - 2][OBS_RANGE - 1] != 'lava':
                # Strafe right to avoid lava
                agent_host.sendCommand("move 0")
                agent_host.sendCommand("strafe 1")
                strafe_flag = 1
                lava_flag = 1
                continue
            elif grid3d[OBS_RANGE][OBS_RANGE + 1][OBS_RANGE - 1] != 'lava' and grid3d[OBS_RANGE][OBS_RANGE + 2][OBS_RANGE - 1] != 'lava':
                # Strafe left to avoid lava
                agent_host.sendCommand("move 0")
                agent_host.sendCommand("strafe -1")
                strafe_flag = 1
                lava_flag = 1
                continue

        if jump_flag == 1:
            agent_host.sendCommand("jump 0")
            jump_flag = 0
            continue

        # Discrepancy Detection
        # Check the nearby area for lava blocks
        # TODO Increase observation range to 2 and check for lava behind the lava tile
        if grid3d[OBS_RANGE + 1][OBS_RANGE][OBS_RANGE - 1] == 'lava':
            agent_host.sendCommand("jump 1")
            jump_flag = 1
            continue

            if grid3d[OBS_RANGE][OBS_RANGE - 1][OBS_RANGE - 1] != 'lava':
                # Strafe left to avoid lava
                agent_host.sendCommand("move 0")
                agent_host.sendCommand("strafe 1")
                strafe_flag = 1
                lava_flag = 1
                continue
            elif grid3d[OBS_RANGE][OBS_RANGE + 1][OBS_RANGE - 1] != 'lava':
                # Strafe right to avoid lava
                agent_host.sendCommand("move 0")
                agent_host.sendCommand("strafe -1")
                strafe_flag = 1
                lava_flag = 1
                continue
            else:
                agent_host.sendCommand("move -1")
                back_flag == 1
                continue

        # Check for the distance moved discrepancy
        distTraveled = math.sqrt((ax - ox) ** 2 + (az - oz) ** 2)

        if distTraveled < 0.1:
            if grid3d[OBS_RANGE + 1][OBS_RANGE][OBS_RANGE] != 'air':
                if grid3d[OBS_RANGE + 1][OBS_RANGE][OBS_RANGE + 1] == 'air':
                    # Jump over the obstacle
                    agent_host.sendCommand("jump 1")
                    time.sleep(0.1)
                    agent_host.sendCommand("jump 0")
                    continue
                elif grid3d[OBS_RANGE + 1][OBS_RANGE + 1][OBS_RANGE + 1] == 'air':
                    # Strafe left to go around the obstacle
                    agent_host.sendCommand("move 0")
                    agent_host.sendCommand("strafe -1")
                    strafe_flag = 1
                    continue
                elif grid3d[OBS_RANGE + 1][OBS_RANGE - 1][OBS_RANGE + 1] == 'air':
                    #  Strafe right to go around the obstacle
                    agent_host.sendCommand("move 0")
                    agent_host.sendCommand("strafe 1")
                    strafe_flag = 1
                    continue
                else:
                    # Mine the block in the way
                    agent_host.sendCommand("move 0")
                    agent_host.sendCommand("attack 1")
                    tx = OBS_RANGE
                    ty = OBS_RANGE + 1
                    tz = OBS_RANGE + 1
                    attack_flag = 1
                    continue
            elif grid3d[OBS_RANGE + 1][OBS_RANGE + 1][OBS_RANGE] != 'air':
                # Strafe right to go around the obstacle
                agent_host.sendCommand("move 0")
                agent_host.sendCommand("strafe 1")
                strafe_flag = 1
                continue
            elif grid3d[OBS_RANGE + 1][OBS_RANGE - 1][OBS_RANGE] != 'air':
                # Strafe left to go around the obstacle
                agent_host.sendCommand("move 0")
                agent_host.sendCommand("strafe -1")
                strafe_flag = 1
                continue

        # TODO Check for nearby wood, and if there is nearby wood start the low level action
        nearbyBlock, block_z, block_x, block_y = GDAU.check_for_block_type(grid3d, 'log', OBS_RANGE)

        if nearbyBlock:
            print block_z, block_x, block_y, grid3d[block_z][block_x][block_y]
            agent_host.sendCommand("move 0")
            turn_flag = 1
            mine_flag = 1
            tz = block_z
            tx = block_x
            ty = block_y

        ox = ax
        oy = ay
        oz = az

print
print "Mission ended"
# Mission has ended.
