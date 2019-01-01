# -*- coding: utf-8 -*-
# file: daily_work_cruiser.py
# author: JinTian
# time: 12/06/2017 10:30 AM
# Copyright 2017 JinTian. All Rights Reserved.
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
this file enable Robot to do daily work in set time points,
such as:

time_points = ['12:30', '11:00', '8:30']

and then for loop all time points, execute accordingly action.
"""
import datetime
import threading
import time
import pickle
import numpy as np
from config.config import global_config
from uranuspy.uranus_op import UranusOp


MSG_SPLITTER = global_config.msg_splitter


class UranusGreetCruiser(object):
    def __init__(self, msg_executor=None):
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
        print('[CRUISER URANUS GREET] started uranuspy greet.')
        time_points_string = ['8:00', '9:30', '11:55', '12:50', '15:47', '15:33', '17:00', '23:00']

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
            print('[DAILY WORK] intervals: ', intervals)
            for i, interval in enumerate(intervals):
                # sleep for interval i
                time.sleep(interval)
                work_index = start_work_index + i
                if work_index == 0:
                    self.say_good_morning()
                elif work_index == 1:
                    self.say_news()
                elif work_index == 2:
                    self.say_eat_launch()
                elif work_index == 3:
                    self.say_noon_sleep()
                elif work_index == 4:
                    self.say_noon_getup()
                elif work_index == 5:
                    self.say_after_work()
                elif work_index == 6:
                    self.say_night_walk()
                elif work_index == 7:
                    self.say_good_night()
                    # after did the last work, sleep until next day
                    # add 2 seconds, make sure it will get into next day
                    time.sleep(self.seconds_left_util_tomorrow() + 2)
        else:
            # indicates no works today, sleep until to next day
            print('[DAILY WORK CRUISER] no work to do today.')
            time.sleep(self.seconds_left_util_tomorrow() + 2)

    def cruise_daily_work(self):
        while True:
            self._main_loop()

    # ---------------------- Methods --------------------------
    def say_good_morning(self):
        msg = '早上好啊' + MSG_SPLITTER + '你起床了吗'
        self.msg_executor.send_msg_to_subscribers(msg)

    def say_news(self):
        msg = '每日新闻播报' + MSG_SPLITTER + '想知道今天有啥大新闻吗'
        self.msg_executor.send_msg_to_subscribers(msg)

    def say_eat_launch(self):
        msg = '下班啦' + MSG_SPLITTER + '该去吃午饭了哟'
        self.msg_executor.send_msg_to_subscribers(msg)

    def say_noon_sleep(self):
        msg = '大中午' + MSG_SPLITTER + '应该睡个午觉'
        self.msg_executor.send_msg_to_subscribers(msg)

    def say_noon_getup(self):
        msg = '午觉睡够了吗' + MSG_SPLITTER + '快起床'
        self.msg_executor.send_msg_to_subscribers(msg)

    def say_after_work(self):
        msg = '该下班了啊'
        self.msg_executor.send_msg_to_subscribers(msg)

    def say_night_walk(self):
        msg = '刚吃完晚饭' + MSG_SPLITTER + '不想出去走走吗'
        self.msg_executor.send_msg_to_subscribers(msg)

    def say_good_night(self):
        msg = '该睡觉了哦' + MSG_SPLITTER + '晚安'
        self.msg_executor.send_msg_to_subscribers(msg)
