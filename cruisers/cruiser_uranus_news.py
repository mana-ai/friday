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
import json
import re
from loguru import logger as logging
from alfred.utils.log import init_logger


init_logger()


MSG_SPLITTER = global_config.msg_splitter


class News(object):

    def __init__(self,
                 title,
                 url,
                 desc,
                 pic_url,
                 news_time):
        self.title = title
        self.url = url
        self.pic_url = pic_url
        self.desc = desc
        self.news_time = news_time


class NewsCruiser(object):

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
        logging.info('[CRUISER NEWS] started daily pushing news.')
        time_points_string = ['8:00', '11:00', '11:30', '12:00', '17:50', '19:00', '20:00', '21:30', '22:46', '22:49', '23:40']

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
    def gather_news():
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

    @staticmethod
    def gather_163_news():
        """
        https://blog.csdn.net/jie310300215/article/details/50990167
        娱乐类 - BA10TA81wangning
            电视 - BD2A86BEwangning
            电影 - BD2A9LEIwangning
            明星 - BD2AB5L9wangning
            音乐 - BD2AC4LMwangning

        体育类 - BA8E6OEOwangning
        财经类 - BA8EE5GMwangning
        军事类 - BAI67OGGwangning
        军情 - DE0CGUSJwangning
        科技 - BA8D4A3Rwangning
        手机 - BAI6I0O5wangning
        数码 - BAI6JOD9wangning
        房产 - BAI6MTODwangning
        汽车 - BA8DOPCSwangning
        """
        m = {
            '娱乐类.电视': 'BD2A86BEwangning',
            '体育类': 'BA8E6OEOwangning',
            '财经类': 'BA8EE5GMwangning',
            '科技': 'BA8D4A3Rwangning',
            '数码': 'BAI6JOD9wangning',
            '房产': 'BAI6MTODwangning',
            '汽车': 'BA8DOPCSwangning',
        }
        r_c = np.random.choice(list(m.values()))
        url = 'https://3g.163.com/touch/reconstruct/article/list/{}/0-12.html'.format(r_c)
        rp = requests.get(url)
        if not rp.ok:
            return '获取新闻失败，稍后我再试一次'
        else:
            a = rp.text
            a = re.findall(r'artiList(.*)', a)[0].strip('(').strip(')')           
            all_news = json.loads(a)[r_c]
            results = []
            for n in all_news[1:]:
                results.append(News(n['title'], n['url'], n['digest'], n['imgsrc'], ''))
            return results

    def broadcast_news(self):
        news = self.gather_163_news()
        if news:
            msg = '【每日新闻推送】\n'
            for n in range(len(news)):
                nw = news[n]
                msg += str(n+1) + '、' + nw.title + '\n' + nw.url + '\n'
            msg += MSG_SPLITTER + news[1].pic_url
            msg += MSG_SPLITTER + news[2].pic_url
            self.msg_executor.send_msg_to_subscribers(msg)
            logging.info('broadcast a news.')
        else:
            logging.error('can not find news, {}'.format(news))
            self.msg_executor.send_msg_to_subscribers('目前无法获取新闻，请联系lucasjin')


if __name__ == "__main__":
    n = NewsCruiser(msg_executor=None)
    n.gather_163_news()