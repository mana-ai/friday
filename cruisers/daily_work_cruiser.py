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
from ..messengers.wechat.wechat_operator import WeChatOperator
import datetime
from ..abilities.post_news import NewsPoster
import threading
import time
import pickle
import numpy as np


class DailyWorkCruiser(object):
    def __init__(self):
        pass

    @staticmethod
    def seconds_left_util_tomorrow():
        now = datetime.datetime.now()
        tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        return abs(tomorrow - now).seconds

    def _main_loop(self):
        print('[CRUISER DAILY WORK] started daily work.')
        time_points_string = ['8:00', '9:30', '11:55', '12:50', '13:40', '17:40', '19:00', '23:00']

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
                    self.say_good_night('hello', '金天')
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
    @staticmethod
    def say_good_morning():
        msg = '早上好啊$$你起床了吗'
        wc_operator = WeChatOperator()
        wc_operator.send_to_all(msg)

    @staticmethod
    def say_news():
        msg = '每日新闻播报$$想知道今天有啥大新闻吗'
        wc_operator = WeChatOperator()
        wc_operator.send_to_all(msg)

    @staticmethod
    def say_eat_launch():
        msg = '下班啦$$该去吃午饭了哟'
        wc_operator = WeChatOperator()
        wc_operator.send_to_all(msg)

    @staticmethod
    def say_noon_sleep():
        msg = '大中午$$应该睡个午觉'
        wc_operator = WeChatOperator()
        wc_operator.send_to_all(msg)

    @staticmethod
    def say_noon_getup():
        msg = '午觉睡够了吗$$快起床'
        wc_operator = WeChatOperator()
        wc_operator.send_to_all(msg)

    @staticmethod
    def say_after_work():
        msg = '该下班了啊'
        wc_operator = WeChatOperator()
        wc_operator.send_to_all(msg)

    @staticmethod
    def say_night_walk():
        msg = '刚吃完晚饭$$不想出去走走吗'
        wc_operator = WeChatOperator()
        wc_operator.send_to_all(msg)

    @staticmethod
    def say_good_night(msg, name):
        msg = '该睡觉了哦 $$晚安'
        wc_operator = WeChatOperator()
        wc_operator.send_to_all(msg)
