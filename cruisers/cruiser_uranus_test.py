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
Uranus exactly action testing


"""
import datetime
import threading
import time
import pickle
import numpy as np
from uranuspy.uranus_op import UranusOp
from config.config import global_config
import hashlib
import requests


MSG_SPLITTER = global_config.msg_splitter


class News(object):

    def __init__(self,
                 title,
                 url,
                 news_time):
        self.title = title
        self.url = url
        self.news_time = news_time

class UranusTestCruiser(object):
    def __init__(self):
        pass

    @staticmethod
    def seconds_left_util_tomorrow():
        now = datetime.datetime.now()
        tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        return abs(tomorrow - now).seconds

    def _main_loop(self):
        print('[CRUISER URANUS TEST] started uranuspy test cruise.')
        time_points_string = ['8:00', '11:04', '11:06', '11:50', '15:47', '20:16', '23:54', '23:55']

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
            print('[DAILY TEST] intervals: ', intervals)
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
        pass

    @staticmethod
    def say_news():
        pass

    @staticmethod
    def say_eat_launch():
        pass

    @staticmethod
    def say_noon_sleep():
        pass

    @staticmethod
    def say_noon_getup():
        pass

    def say_after_work(self):
        news = self.get_news()
        if news:
            msg = '新闻新闻！'
            for n in range(len(news)):
                nw = news[n]
                msg += str(n + 1) + '、 ' + nw.title + '\n' + nw.url + '\n'
            global_uranus_op.send_msg_to_subscribers(msg)
        else:
            global_uranus_op.send_msg_to_subscribers('目前无法获取新闻，请联系lucasjin')

    @staticmethod
    def say_night_walk():
        pass

    @staticmethod
    def say_good_night(msg, name):
        pass

    @staticmethod
    def get_news():
        cat = np.random.choice(['Tech', 'Finance', 'Politics', 'Society', 'Sport'])
        size = np.random.choice(['15', '20'])
        access_key = 'sQhAwIm1baFAdmbi'
        secret_key = '944fe952283a4046a17df8835b508d1a'
        timestamp = int(round(time.time() * 1000))
        print('timestamp: ', timestamp)

        signature = hashlib.md5('{}{}{}'.format(secret_key, timestamp, access_key).encode('utf-8')).hexdigest()
        if cat == '':
            api = 'https://api.xinwen.cn/news/all?size={}&signature={}&timestamp={}&access_key={}'.format(
                size, signature, timestamp, access_key
            )
        else:
            api = 'https://api.xinwen.cn/news/all?category={}&size={}&signature={}&timestamp={}&access_key={}'.format(
                cat, size, signature, timestamp, access_key
            )
        rp = requests.get(api)

        if rp.json()['success']:
            all_news = rp.json()['data']['news']
            results = []
            for n in all_news:
                results.append(News(n['title'], n['url'], ''))
            return results
        else:
            return None
