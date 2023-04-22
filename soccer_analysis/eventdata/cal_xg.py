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

import cv2
import numpy as np


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
        exist = cv2.pointPolygonTest(testContour, defender, True)
        if exist:
            num += 1
    return num


def cal_xg(dis, num_ar, num_goal, header=0):
    xg = (1900 - dis) / 1900 - num_ar / 30 - num_goal / 50
    xg = xg / 100 + (1 - header) * 99 * xg / 100
    return xg


if __name__ == "__main__":
    pass