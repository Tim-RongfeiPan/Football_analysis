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
    video_path = 'datasets/test//ifsylvia-tabyfk.mp4'
    event_path = 'datasets/test/IF Sylvia - Täby FK (1-2).xlsx'
    info_path = 'datasets/test/IF Sylvia - Täby FK.txt'

    time_shot = datetime.time(0, 45, 55)
    test_type = 'Shots'
    time_offset = 0.65
    xlsx = Get_Eventdata(event_path)
    video = Get_Videodata(video_path, time_offset)

    test_list = xlsx.get_eventdata_byevent(test_type)

    weight_path = Path('datasets/best.pt')
    model = Analysis(weight_path)

    # save screen shot
    for index, event in enumerate(test_list):
        time_shot = event[1]
        pos_shot = event[8]
        # out = video.get_videodata_bytime(5, time_shot)
        # jpg_name = 'runs/temp/testing_temp_' + str(index) + '.jpg'
        # cv2.imwrite(jpg_name, out)
        # source = jpg_name
        # im0, seg_map, model_image, retrieved_image, pers_point = model.test_analysis_image(
        #     source, show_team=info_path)

        pos_shot = pos_shot.split(';')
        pers_point = [(990, 184, 'Blue'), (723, 194, 'Blue'),
                      (667, 233, 'Blue'), (133, 651, 'Blue'),
                      (578, 68, 'Blue'), (823, 68, 'Blue'), (812, 58, 'Blue'),
                      (890, 9, 'White'), (812, 0, 'Blue'), (790, -19, 'Blue'),
                      (378, 19, 'White'), (734, 0, 'Blue'), (467, 9, 'Blue')]

        pos_shot = [int(pos_shot[0]), int(pos_shot[1])]
        pos_shot = [
            int(pos_shot[0] * 1280 / 100),
            int(pos_shot[1] * 720 / 100)
        ]

        logger.info(pos_shot)
        # logger.info(pers_point)

        num = cal_numdef_around(pos_shot, pers_point, threshold=400)
        #TODO: method to handle goal position
        goal_pos = [[1280, 330], [1280, 390]]
        num1 = cal_numdef_2goal(pos_shot, pers_point, goal_pos)
        logger.info(num)
        logger.info(num1)

        # if not os.path.exists('runs/save/' + str(index)):
        #     os.makedirs('runs/save/' + str(index))

        # cv2.imwrite('runs/save/' + str(index) + '/test_im0.jpg', im0)
        # cv2.imwrite('runs/save/' + str(index) + '/test_retrieved_image.jpg',
        #             retrieved_image)
        # cv2.imwrite('runs/save/' + str(index) + '/test_seg_map.jpg', seg_map)
        # cv2.imwrite('runs/save/' + str(index) + '/test_model_image.jpg',
        #             model_image)
