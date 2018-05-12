import json
import math
import sys
import time

BLOCK_CENTER_DELTA = 0.5
HEAD_HEIGHT = 1.62


def initialize_grid3d(raw_obs_grid, obs_range):
    grid3d = []
    list_size = 2 * obs_range + 1

    for i in range(list_size):
        grid3d.append([])
        for _ in range(list_size):
            grid3d[i].append([])

    raw_obs_grid_to_grid3d(grid3d, raw_obs_grid, obs_range)

    return grid3d


def raw_obs_grid_to_grid3d(grid3d, raw_obs_grid, obs_range):
    list_size = 2 * obs_range + 1

    for idx, element in enumerate(raw_obs_grid):
        index = idx % (list_size * list_size)
        grid3d[index / list_size][index % list_size].append(element)


def distance3d(ax, ay, az, bx, by, bz):
    return math.sqrt(((ax - bx) ** 2) + ((ay - by) ** 2) + ((az - bz) ** 2))


def get_yaw_to_block(ax, ay, az, a_yaw, tx, ty, tz):
    # Calculate angle using tan function
    dx = int(tx) - ax
    dz = int(tz) - az

    target_yaw = (math.atan2(dz, dx) * 180.0 / math.pi) - 90
    difference = target_yaw - a_yaw

    # Final difference should be within -180 and 180 degrees
    while difference < -180:
        difference += 360

    while difference > 180:
        difference -= 360

    # Normalize the difference before returning
    return difference/180


def get_pitch_to_block(ax, ay, az, a_pitch, tx, ty, tz):
    straight_dist = math.sqrt(tx ** 2 + ty ** 2 + tz ** 2)

    target_pitch = math.asin(ty / straight_dist) * 180.0 / math.pi
    difference = target_pitch - a_pitch

    # Normalize the difference before returning
    return difference/180


def find_yaw_difference_to_block(ax, ay, az, a_yaw, tx, ty, tz, obs_range):
    # Round ax, ay, and az down
    block_x = math.floor(ax) + tx - obs_range + BLOCK_CENTER_DELTA
    block_z = math.floor(az) + tz - obs_range + BLOCK_CENTER_DELTA
    block_y = math.floor(ay) + ty - obs_range + BLOCK_CENTER_DELTA

    yaw_difference = get_yaw_to_block(ax, ay, az, a_yaw, block_x, block_y, block_z)

    return yaw_difference


def find_pitch_difference_to_block(ax, ay, az, a_pitch, tx, ty, tz, obs_range):
    block_x = int(tx) - obs_range + BLOCK_CENTER_DELTA
    block_z = int(tz) - obs_range + BLOCK_CENTER_DELTA
    block_y = int(ty) - obs_range + BLOCK_CENTER_DELTA - HEAD_HEIGHT

    pitch_difference = get_pitch_to_block(ax, ay + HEAD_HEIGHT, az, a_pitch, block_x, block_y, block_z)

    return pitch_difference


def find_yaw_difference_to_start(a_yaw, start_yaw):
    difference = start_yaw - a_yaw

    # Final difference should be within -180 and 180 degrees
    while difference < -180:
        difference += 360

    while difference > 180:
        difference -= 360

    # Normalize the difference before returning
    return difference/180


def find_pitch_difference_to_start(a_pitch, start_pitch):
    difference = start_pitch - a_pitch

    # Final difference should be within -180 and 180 degrees
    while difference < -180:
        difference += 360

    while difference > 180:
        difference -= 360

    # Normalize the difference before returning
    return difference/180


def check_for_block_type(grid3d, block_type, obs_range):
    for z in xrange(2 * obs_range + 1):
        for x in xrange(2 * obs_range + 1):
            for y in xrange(2 * obs_range + 1):
                if grid3d[z][x][y] == block_type:
                    return True, z, x, y

    return False, None, None, None
