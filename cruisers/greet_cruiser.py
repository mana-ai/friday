# -*- coding: utf-8 -*-
# file: daily_greet.py
# author: JinTian
# time: 28/04/2017 4:36 PM
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
this file all method are daemon thread. All method will execute everyday, day by day never stop
Greetings include:

Good Morning: this greeting will send Good Morning to all WeChat friends, Only when
it is 8:00 A.M every day. And will send today's news to all friends.

Good Night: this greeting will send Good Night to all WeChat friends, Only when
it is 22:30 P.M every day. And will send a joke to every one.

"""
from ..messengers.wechat.wechat_operator import WeChatOperator
from datetime import datetime
from core.abilities.post_news import NewsPoster
import threading
import time
import pickle
import numpy as np
import itchat
from numpy import random


class GreetCruiser(object):

    def __init__(self):
        pass

    def cruise_greet(self):
        """
        I think here I can not using while True and endless check time.
        Instead, I can do this algorithm:
        where run, cruiser will check now time, and calculate delta between
        2 time node(assume in the same day), if now time is ahead of time node
        1, then just pass node 1, and time for delta time, after that go straight into execution,
        no need to compare time all the time!!!
        :return:
        """
        print('[CRUISE] greet cruise start...')
        morning_time_str = '9:53:00'
        night_time_str = '23:00:00'

        while True:
            today_date = datetime.now().date().strftime('%Y-%m-%d')
            now_time = datetime.now()
            morning_time = datetime.strptime(today_date + ' ' + morning_time_str, '%Y-%m-%d %H:%M:%S')
            night_time = datetime.strptime(today_date + ' ' + night_time_str, '%Y-%m-%d %H:%M:%S')

            if now_time > morning_time:
                # if so, indicates that, morning has passed, just sleep for -delta_now_night.seconds
                # and execute night greet
                print('[CRUISE] night mode.')
                time.sleep((night_time - now_time).seconds)
                self._good_night()
            else:
                # indicates that morning is not reach, then we will sleep for delta.seconds, execute morning greet
                # after that sleep for node_delta then execute night greet
                print('[CRUISE] day mode.')
                time.sleep((morning_time - now_time).seconds)
                self._good_morning()
                time.sleep((night_time - morning_time).seconds)
                self._good_night()

    def _good_morning(self):
        """
        this method only execute when time is 8:00 A.M.
        :return:
        """
        all_friends = itchat.get_friends(update=True)
        all_friends = random.choice(all_friends, 30)
        for friend in all_friends:
            msg = next(self.get_good_morning())
            print('send to {}, msg {}'.format(friend['UserName'], msg))
            for m in msg.split('$$'):
                itchat.send(m, friend['UserName'])
                time.sleep(6)
            print('send to {}, msg {}'.format(friend['UserName'], msg))

    def _good_night(self):
        """
        this method will send good night to all friends
        :return:
        """
        all_friends = itchat.get_friends(update=True)
        all_friends = random.choice(all_friends, 10)
        for friend in all_friends:
            msg = next(self.get_good_night())
            print('send to {}, msg {}'.format(friend['UserName'], msg))
            for m in msg.split('$$'):
                itchat.send(m, friend['UserName'])
                time.sleep(5)
            print('send to {}, msg {}'.format(friend['UserName'], msg))

    @staticmethod
    def get_good_morning():
        news_poster = NewsPoster()
        news = news_poster.get_news()
        hello = np.random.choice([
            '早上好啊',
            '又是新的一天',
            'Jarvis充满活力的开始了一天的日常工作',
            '你起床了吗',
            'Good morning!',
            '今天天气不错！',
            '撸起袖子开始一天的工作！',
            '开始奋斗！',
            '早上好啊，吃早饭了吗',
            '上午好',
            '开始怀疑人生'
        ])
        good_morning = np.random.choice([
            '播报今天的Big News！',
            '播报今天的大新闻！',
            '看看今天都有什么大事发生',
            'Jarvis日常新闻播报'
        ])
        hello = hello + '$$' + good_morning + '$$' + news
        yield hello

    @staticmethod
    def get_good_night():
        f = 'reasoner/collected_questions.pkl'
        with open(f, 'rb') as file:
            a = pickle.load(file)
        all_questions_list = [v for k, v in a.items()]
        random_question = np.random.choice(all_questions_list[np.random.randint(0, len(all_questions_list))])
        hello = np.random.choice([
            '到睡觉了哟',
            'Time to go to bad.',
            '今天还开心吗',
            '马上要睡觉了，想不想让我推荐一部电影看啊',
            '快睡觉了亲爱的',
            '我知道你舍不得我但是你还是得睡觉',
            '想和我一起睡吗',
            '该睡觉了哦么么哒',
            'Time to sleep',
            '睡觉睡觉',
            '本机器人明日要早起'
        ])
        good_night = np.random.choice([
            '晚安，爱你',
            '晚安哦，亲爱的',
            '晚安宝贝',
            '晚安么么哒'
        ])
        hello = hello + '$$' + random_question + '$$' + good_night
        yield hello
