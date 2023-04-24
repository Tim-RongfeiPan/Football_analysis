#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   cal_xg.py
@Time    :   2023/04/02 19:17:27
@Author  :   Rongfei Pan
@Version :   1.0
@Contact :   rongfei@kth.se 1838863836prf@gmail.com
@Desc    :   None
'''

# here put the import lib

from asyncio.log import logger
import cv2
import numpy as np
from loguru import logger
import math


def cal_eurdistance(pos1, pos2):
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    return np.sqrt(sum(np.power((pos1 - pos2), 2)))


def cal_numdef_around(pos, poslist, threshold):
    num = 0
    for defender in poslist:
        defender = [defender[0], defender[1]]
        dis = cal_eurdistance(pos, defender)
        if dis <= threshold:
            num += 1
    return num


def cal_numdef_2goal(pos, poslist, goal_pos):
    num = 0
    for defender in poslist:
        defender = [defender[0], defender[1]]
        testContour = np.array(
            [np.array(goal_pos[0]),
             np.array(pos),
             np.array(goal_pos[1])])
        exist = cv2.pointPolygonTest(testContour, defender, False)
        if exist == 1:
            num += 1
    return num


def cal_angle(pos_shot, goal_mid):
    x = abs(goal_mid[0] - pos_shot[0])
    y = abs(goal_mid[1] - pos_shot[1])
    degree = math.atan2(y, x) / math.pi * 180
    return degree


# xg = cal_xg(pos_shot, pers_point, goal_pos, goal_mid, header=0)
def cal_xg(pos_shot, pers_point, goal_pos, goal_mid, header=0):

    threshold = 100
    num_ar = cal_numdef_around(pos_shot, pers_point, threshold)
    num_goal = cal_numdef_2goal(pos_shot, pers_point, goal_pos)
    dis = cal_eurdistance(pos_shot, goal_mid)

    angle = cal_angle(pos_shot, goal_mid)

    # logger.info(num_ar)
    # logger.info(num_goal)
    # logger.info(dis)

    # xg = (1900 - dis) / 1900 - num_ar / 20 - num_goal / 10 - angle / 90 * 0.5
    # xg = xg / 15 + (1 - header) * 14 * xg / 15

    xg = 2 * (1 - 1 / (1 + math.e**(-0.01 * dis)))

    if angle <= 15 and angle >= 0:
        xg = xg
    elif angle > 15 and angle <= 90:
        d = -1 / (1 + math.e**(-0.18 * (angle - 45))) + 1
        xg = xg * d
    else:
        raise RuntimeError(f'wrong angle value {angle}')

    xg = xg * (0.95 - num_goal / 10)
    xg = xg * (1 - num_ar / 20)

    xg = xg / 15 + (1 - header) * 14 * xg / 15
    return xg


if __name__ == "__main__":
    pass