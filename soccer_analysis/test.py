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
from event_data.get_eventdata import Get_Eventdata, Get_Videodata
from demo_test import run
import cv2
from pathlib import Path

if __name__ == "__main__":
    video_path = 'datasets/test//ifsylvia-tabyfk.mp4'
    event_path = 'datasets/test/IF Sylvia - Täby FK (1-2).xlsx'
    info_path = 'datasets/test/IF Sylvia - Täby FK.txt'

    time_shot = datetime.time(0, 45, 55)

    xlsx = Get_Eventdata(event_path)
    video = Get_Videodata(video_path, 0)

    out = video.get_videodata_bytime(5, time_shot)
    cv2.imwrite('runs/temp/testing_temp.jpg', out)
    source = 'runs/temp/testing_temp.jpg'
    weight_path = Path('datasets/best.pt')
    run(source=source,
        yolo_weights=weight_path,
        show_team=info_path,
        no_strongSort=True,
        show_perstrans=True,
        save_vid=True,
        save_crop=True)
