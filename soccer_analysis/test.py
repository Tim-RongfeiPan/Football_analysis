#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2023/03/22 08:45:57
@Author  :   Rongfei Pan
@Version :   1.0
@Contact :   rongfei@kth.se 1838863836prf@gmail.com
@Desc    :   test for preprocessing of xg model
'''

# here put the import lib
import datetime
from eventdata.get_eventdata import Get_Eventdata, Get_Videodata, Get_xGdata
from demo_test import Analysis
import cv2
import os
from pathlib import Path
from eventdata.cal_xg import *

from loguru import logger

if __name__ == "__main__":
    video_path = 'datasets/test2/assyriska-taby.mp4'
    event_path = 'datasets/test2/Assyriska FF - Täby FK (2-7).xlsx'
    info_path = 'datasets/test2/Assyriska FF - Täby FK.txt'
    json_path = 'datasets/test2/ettan, 2021786157109941299-AssyriskaFF-TäbyFK.json'
    test_type = 'Shots'
    time_offset = 4.8
    xlsx = Get_Eventdata(event_path)
    video = Get_Videodata(video_path, time_offset)
    xgdata = Get_xGdata(json_path)

    shot_list = xgdata.get_jsondata_shot()
    test_list = xlsx.get_eventdata_byevent(test_type)

    weight_path = Path('datasets/best.pt')
    model = Analysis(weight_path)

    # save screen shot
    for index, event in enumerate(test_list):
        print('=============================================')
        # logger.info(event)
        time_shot = event[1]
        team_name = event[7]
        pos_shot = event[8]
        out = video.get_videodata_bytime(5, time_shot)
        jpg_name = 'runs/temp/testing_temp_' + str(index) + '.jpg'
        cv2.imwrite(jpg_name, out)
        source = jpg_name
        im0, seg_map, model_image, retrieved_image, pers_point = model.test_analysis_image(
            source, show_team=info_path)

        pos_shot = pos_shot.split(';')

        # pers_point = [(1291, 0, 'Blue'), (1313, 48, 'White'),
        #               (1224, -155, 'Blue'), (1280, 116, 'Blue'),
        #               (1246, -175, 'Blue'), (1280, 58, 'White'),
        #               (1369, -145, 'White'), (1380, 0, 'Blue'),
        #               (1335, -9, 'White'), (1346, -145, 'White'),
        #               (1324, -58, 'White'), (1280, -58, 'White'),
        #               (1324, 38, 'Blue'), (1291, -126, 'Blue'),
        #               (1324, -136, 'Blue'), (1313, -145, 'White'),
        #               (1435, 9, 'White'), (1469, -262, 'Blue'),
        #               (1747, -992, 'White')]

        pos_shot = [int(pos_shot[0]), int(pos_shot[1])]
        pos_shot = [
            int(pos_shot[0] * 1280 / 100),
            int(pos_shot[1] * 720 / 100)
        ]

        # logger.info(pos_shot)
        # logger.info(pers_point)

        #TODO: method to handle goal position

        direction = xlsx.get_direction_byteam(time_shot, team_name)
        half = xlsx.get_half(time_shot)

        if half == 'second half':
            pos_shot = [1280 - pos_shot[0], 720 - pos_shot[1]]
        print(pos_shot)

        print(direction, team_name)
        goal_pos1 = [[1280, 320], [1280, 400]]
        goal_mid1 = [1280, 360]
        goal_pos2 = [[0, 320], [0, 400]]
        goal_mid2 = [0, 360]

        if direction == 'left':
            goal_mid = goal_mid2
            goal_pos = goal_pos2
        else:
            goal_mid = goal_mid1
            goal_pos = goal_pos1

        pts = np.array([goal_pos[0], goal_pos[1], pos_shot, goal_pos[0]])
        cv2.polylines(model_image, [pts], True, (255, 255, 0), 3)

        # logger.info(dis)
        xg = cal_xg(pos_shot, pers_point, goal_pos, goal_mid, header=0)
        logger.info(xg)

        real_xg = shot_list[index]['xg']
        logger.info(real_xg)
        print('=============================================')

        if not os.path.exists('runs/save/' + str(index)):
            os.makedirs('runs/save/' + str(index))

        cv2.imwrite('runs/save/' + str(index) + '/test_im0.jpg', im0)
        cv2.imwrite('runs/save/' + str(index) + '/test_retrieved_image.jpg',
                    retrieved_image)
        cv2.imwrite('runs/save/' + str(index) + '/test_seg_map.jpg', seg_map)
        cv2.imwrite('runs/save/' + str(index) + '/test_model_image.jpg',
                    model_image)
