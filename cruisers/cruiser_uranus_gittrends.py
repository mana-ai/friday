# -*- coding: utf-8 -*-
# file: cruiser_uranus_news.py
# author: JinTian
# time: 2018/6/25 10:25 PM
# Copyright 2018 JinTian. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
"""
scrip news from whole internet
the STRONGEST robot in the world


Sending news at certain time in a day
request the news API frequently

5 time period for news pushing

8:00
国内新闻
HackerNews

12:00
国内新闻
HackerNews

17:00
国内新闻
HackerNews

19:00
国内新闻
HackerNews

23:30
国内新闻
HackerNews

"""
import datetime
import threading
import time
import pickle
import numpy as np
from config.config import global_config
import hashlib
import time
import requests
from uranuspy.uranus_op import UranusOp

MSG_SPLITTER = global_config.msg_splitter


class GitTrending(object):

    def __init__(self, msg_executor):
        if isinstance(msg_executor, UranusOp):
            self.msg_executor = msg_executor
        else:
            ValueError('self.msg_executor must be UranusOp object.')

    @staticmethod
    def seconds_left_util_tomorrow():
        now = datetime.datetime.now()
        tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        return abs(tomorrow - now).seconds

    def _main_loop(self):
        print('[CRUISER NEWS] started daily pushing news.')
        time_points_string = ['8:00', '11:00', '11:30', '12:00', '17:50', '19:00', '20:00', '21:30', '22:54', '23:40']

        today_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
        time_points = [datetime.datetime.strptime(today_date + ' ' + i, '%Y-%m-%d %H:%M') for i in time_points_string]
        time_points_still = [i for i in time_points if i >= datetime.datetime.now()]

        if len(time_points_still) > 0:
            start_work_index = time_points.index(time_points_still[0])
            print('still need to do works: {}, the first thing start at {}, at index {}'.format(len(time_points_still),
                                                                                                time_points_still[0],
                                                                                                start_work_index))
            time_points_still.insert(0, datetime.datetime.now())
            intervals = [(time_points_still[i] - time_points_still[i - 1]).seconds for i in
                         range(1, len(time_points_still))]
            print('[SEND NEWS] intervals: ', intervals)
            for i, interval in enumerate(intervals):
                # sleep for interval i
                time.sleep(interval)
                work_index = start_work_index + i
                if work_index == 0:
                    self.broadcast_news()
                elif work_index == 1:
                    self.broadcast_news()
                elif work_index == 2:
                    self.broadcast_news()
                elif work_index == 3:
                    self.broadcast_news()
                elif work_index == 4:
                    self.broadcast_news()
                elif work_index == 5:
                    self.broadcast_news()
                elif work_index == 6:
                    self.broadcast_news()
                elif work_index == 7:
                    self.broadcast_news()
                elif work_index == 8:
                    self.broadcast_news()
                elif work_index == 9:
                    self.broadcast_news()
                    time.sleep(self.seconds_left_util_tomorrow() + 2)
        else:
            # indicates no works today, sleep until to next day
            print('[DAILY WORK CRUISER] no work to do today.')
            time.sleep(self.seconds_left_util_tomorrow() + 2)

    def cruise_daily_work(self):
        while True:
            self._main_loop()

    @staticmethod
    def get_github_trending():
        pass


    def broadcast_news(self):
        news = self.gather_news()
        if news:
            msg = '【每日新闻推送】     '
            for n in range(len(news)):
                nw = news[n]
                msg += str(n+1) + '、' + nw.title + '           ' + nw.url + '         '
            self.msg_executor.send_msg_to_subscribers(msg)
        else:
            self.msg_executor.send_msg_to_subscribers('目前无法获取新闻，请联系lucasjin')
