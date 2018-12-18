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

Official FairyDiary goods pushing
A tool for promoting people to spread goods


"""
from ..messengers.wechat.wechat_operator import WeChatOperator
import datetime
from ..abilities.post_news import NewsPoster
import threading
import time
import pickle
import numpy as np
from ..messengers.uranus.uranus_op import global_uranus_op
from core.config import global_config


MSG_SPLITTER = global_config.msg_splitter


class News(object):

    def __init__(self,
                 title,
                 url,
                 news_time):
        self.title = title
        self.url = url
        self.news_time = news_time


class UranusFDCruiser(object):

    def __init__(self):
        pass

    @staticmethod
    def seconds_left_util_tomorrow():
        now = datetime.datetime.now()
        tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        return abs(tomorrow - now).seconds

    def _main_loop(self):
        print('[CRUISER NEWS] started daily pushing news.')
        time_points_string = ['8:00', '11:00', '11:30', '12:00', '17:50', '19:00', '23:30']

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
                    time.sleep(self.seconds_left_util_tomorrow() + 2)
        else:
            # indicates no works today, sleep until to next day
            print('[DAILY WORK CRUISER] no work to do today.')
            time.sleep(self.seconds_left_util_tomorrow() + 2)

    def cruise_daily_work(self):
        while True:
            self._main_loop()

    @staticmethod
    def gather_news():
        return [
            News('一个placholder新闻，新闻接口还未通过审核', '', ''),
            News('假装这是一个新闻啦', '', ''),
            News('这是一个新闻', '', ''),
            News('一男子被猪杀死', '', '')
        ]

    def broadcast_news(self):
        news = self.gather_news()
        msg = '【新闻】\n'
        for n in news:
            msg += '- ' + n.title + '\n'
        global_uranus_op.send_msg_to_subscribers(msg)