#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   get_eventdata.py
@Time    :   2023/03/14 15:07:49
@Author  :   Rongfei Pan
@Version :   1.0
@Contact :   rongfei@kth.se 1838863836prf@gmail.com
@Desc    :   function library for event data
'''

# here put the import lib

from openpyxl import *
import datetime


def get_eventdata_byname(path, name):
    """get event data by name

    Parameters
    ----------
    path : string
        path of xlsx file
    name : string
        name, Exp: Pass, Shots, ...

    Returns
    -------
    list[list]
        list of info in row with corresponding name
    """
    wb = load_workbook(path)
    data = wb['Sheet1']
    name_list = []
    for i in range(2, data.max_row):
        if data.cell(i, 1).value == name:
            name_info = []
            for j in range(1, data.max_column):
                name_info.append(data.cell(i, j).value)
            name_list.append(name_info)
    return name_list


def get_eventdata_bytime(path, dtime):
    """get event data by time

    Parameters
    ----------
    path : string
        path of xlsx file
    dtime : datetime.time
        time, Exp: datetime.time(xx, xx, xx)

    Returns
    -------
    list[list]
        list with two sublist with closest time. Sublist: info in row
    """
    wb = load_workbook(path)
    data = wb['Sheet1']

    time_list = []

    for i in range(2, data.max_row):
        if data.cell(i, 2).value >= dtime:
            name_info = []
            for j in range(1, data.max_column):
                name_info.append(data.cell(i - 1, j).value)
            time_list.append(name_info)
            name_info = []
            for j in range(1, data.max_column):
                name_info.append(data.cell(i, j).value)
            time_list.append(name_info)
            break
    return time_list


def get_eventdata_byplayer(path, name):
    """get event data by searching player name

    Parameters
    ----------
    path : string
        path of xlsx file
    name : string
        player's name

    Returns
    -------
    list[list]
        list of info in row with corresponding player's name
    """
    wb = load_workbook(path)
    data = wb['Sheet1']
    name_list = []
    for i in range(2, data.max_row):
        if data.cell(i, 7).value.find(name) != -1:
            name_info = []
            for j in range(1, data.max_column):
                name_info.append(data.cell(i, j).value)
            name_list.append(name_info)
    return name_list


def get_eventdata_byteam(path, teamname):
    """get event data by searching player name

    Parameters
    ----------
    path : string
        path of xlsx file
    name : string
        team name

    Returns
    -------
    list[list]
        list of info in row with corresponding team name
    """
    wb = load_workbook(path)
    data = wb['Sheet1']
    name_list = []
    for i in range(2, data.max_row):
        if data.cell(i, 8).value.find(name) != -1:
            name_info = []
            for j in range(1, data.max_column):
                name_info.append(data.cell(i, j).value)
            name_list.append(name_info)
    return name_list


if __name__ == '__main__':
    path = 'datasets/IK Frej Täby-IF Brommapojkarna(0-1).xlsx'
    # name = 'Shots'
    # out = get_eventdata_byname(path, name)
    # dtime = datetime.time(0, 8, 29)
    # out = get_eventdata_bytime(path, dtime)
    name = 'Christer Gustafsson'
    out = get_eventdata_byplayer(path, name)
    # name = 'IF Brommapojkarna'
    # out = get_eventdata_byteam(path, name)
    print(out)
    print('=============')
    print(out[0])
