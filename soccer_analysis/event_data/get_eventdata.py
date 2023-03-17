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

from msilib.schema import Class
from matplotlib import docstring
from openpyxl import *
import datetime


class Get_Eventdata:

    def __init__(self, path):
        """initialized by path

        Args:
            path (string): path of xlsx file
        """
        super(Get_Eventdata, self).__init__()
        self.path = path
        self.wb = load_workbook(path)
        self.data = self.wb['Sheet1']

    def get_eventdata_byevent(self, name):
        """get event data by event

        Args:
            name (string): type of event

        Returns:
            list[list]: list of info in row with corresponding name
        """
        name_list = []
        for i in range(2, self.data.max_row):
            if self.data.cell(i, 1).value == name:
                name_info = []
                for j in range(1, self.data.max_column):
                    name_info.append(self.data.cell(i, j).value)
                name_list.append(name_info)
        return name_list

    def get_eventdata_bytime(self, dtime):
        """get event data by time

        Args:
            dtime (datetime.time): time, Exp: datetime.time(xx, xx, xx)

        Returns:
            list[list]: list with two sublist with closest time. Sublist: info in row
        """

        time_list = []

        for i in range(2, self.data.max_row):
            if self.data.cell(i, 2).value >= dtime:
                name_info = []
                for j in range(1, self.data.max_column):
                    name_info.append(self.data.cell(i - 1, j).value)
                time_list.append(name_info)
                name_info = []
                for j in range(1, self.data.max_column):
                    name_info.append(self.data.cell(i, j).value)
                time_list.append(name_info)
                break
        return time_list

    def get_eventdata_byplayer(self, name):
        """get event data by player name

        Args:
            name (string): player's name

        Returns:
            list[list]: list of info in row with corresponding player's name
        """

        name_list = []
        for i in range(2, self.data.max_row):
            if self.data.cell(i, 7).value.find(name) != -1:
                name_info = []
                for j in range(1, self.data.max_column):
                    name_info.append(self.data.cell(i, j).value)
                name_list.append(name_info)
        return name_list

    def get_eventdata_byteam(self, teamname):
        """ get event data by searching team name

        Args:
            teamname (string): team name

        Returns:
            list[list]: list of info in row with corresponding team name
        """

        name_list = []
        for i in range(2, self.data.max_row):
            if self.data.cell(i, 8).value.find(teamname) != -1:
                name_info = []
                for j in range(1, self.data.max_column):
                    name_info.append(self.data.cell(i, j).value)
                name_list.append(name_info)
        return name_list

    def get_position_byevent(self, event):
        """get position data by event

        Args:
            event (string): name of event

        Returns:
            list: list of position with corresponding event 
        """
        pos_list = []
        for i in range(2, self.data.max_row):
            if self.data.cell(i, 1).value == event:
                pos_info = self.data.cell(i, 9).value
                pos_list.append(pos_info)
        return pos_list


if __name__ == '__main__':
    path = 'datasets/IK Frej Täby-IF Brommapojkarna(0-1).xlsx'
    xlsx = Get_Eventdata(path)
    name = 'Shots'
    # dtime = datetime.time(0, 8, 29)
    # name = 'Christer Gustafsson'
    # name = 'IF Brommapojkarna'
    out = xlsx.get_position_byevent(name)
    print(out)
    print('=============')
    print(out[0])
