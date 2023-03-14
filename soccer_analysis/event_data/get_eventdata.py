#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   get_eventdata.py
@Time    :   2023/03/14 15:07:49
@Author  :   Rongfei Pan
@Version :   1.0
@Contact :   rongfei@kth.se 1838863836prf@gmail.com
@Desc    :   None
'''

# here put the import lib

from cv2 import getVersionRevision
import openpyxl
import sys
import re
from openpyxl import load_workbook


def get_eventdata(path):
    wb = load_workbook(path)
    data = wb['Sheet1']
    # value = data['A2']
    value = data.cell(1, 2)
    print(value.value)
    for i in range(1, data.max_row):
        if data.cell(i, 1).value == 'Shots':
            for j in range(1, data.max_column):
                print(data.cell(i, j).value)
    return


if __name__ == '__main__':
    path = 'datasets/IK Frej Täby-IF Brommapojkarna(0-1).xlsx'
    get_eventdata(path)
