# -*- coding: utf-8 -*-
# file: todo_cruiser.py
# author: JinTian
# time: 28/04/2017 3:07 PM
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
this file implement a cruiser class,
in this cruiser class is a while true loop,
it will read local todo.pkl and find things need to do
Once it find, he will execute it.

Via this class Jarvis will have a cruise brain indicates him what going to do
in the future
"""
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import numpy as np
import datetime
import os
import pickle
import time

from rules import *


class ToDoCruiser(object):

    def __init__(self, msg_executor):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.check_interval = 2
        self.todo_local_file = os.path.join(self.base_dir, 'todo.pkl')
        self.changes_event_handler = ChangesHandler()
        self.msg_executor = msg_executor

    @staticmethod
    def is_today_todo(todo_time):
        """
        judge todo time is within today or not
        :param todo_time:
        :return:
        """
        today_date = datetime.datetime.now().date()
        todo_date = todo_time.date()
        if today_date == todo_date:
            return True
        else:
            return False

    @staticmethod
    def seconds_left_util_tomorrow():
        now = datetime.datetime.now()
        tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        return abs(tomorrow - now).seconds

    def solve_one_day_todo_events(self, todo_items_list):
        """
        this method will solve all events in one day
        the principle is very simple, get todo event that
        time is ahead of now time, then sorted todo items,
        get the interval of very todo event time, for instance:
        now time is 6:10, we have 3 events ahead of now:
        8:20, 9:30, 13:20
        the we will get 3 intervals:
        interval_1 = 8:20 - now
        interval_2 = 9:30 - 8:20
        interval_3 = 13:20 - 9:30
        then we will time sleep interval_1 execute event_1
        time sleep interval_2 execute event_2
        time sleep interval_3 execute event_3
        then All the todo event today are all done!!!
        :param todo_items_list:
        :return:
        """
        seconds_until_tomorrow = self.seconds_left_util_tomorrow()
        if len(todo_items_list) < 1:
            # indicates that today has no todo events, then cruise will sleep until tomorrow
            # time.sleep(seconds_until_tomorrow + 1)
            # seems can not directly sleep to tomorrow, directly continue
            time.sleep(10)
        else:
            # add now time to calculate intervals
            now = datetime.datetime.now().replace(microsecond=0, second=0)
            now_item = {
                'time': now
            }
            todo_items_list.append(now_item)
            todo_items_list = sorted(todo_items_list, key=lambda x: x['time'])
            todo_still_items = [i for i in todo_items_list if i['time'] >= now]
            if len(todo_still_items) > 1:
                intervals = [(todo_still_items[i]['time'] - todo_still_items[i - 1]['time']).seconds for i in
                             range(1, len(todo_still_items))]
                print('[TODO CRUISER] still todo intervals: ', intervals)
                for i, interval in enumerate(intervals):
                    print('[TODO CRUISER] start solve event {}, interval {}'.format(i, interval))

                    # I am changing  time.sleep(interval) into following one, which make sense more
                    # so that sleep will interrupt when local_file changed,
                    for t in range(interval):
                        if self.changes_event_handler.CHANGE_FLAG:
                            # if detected changes, then return and reset flag to False
                            self.changes_event_handler.CHANGE_FLAG = False
                            print('[IMPORTANT] changes detected, solve today return.')
                            return
                        else:
                            time.sleep(1)
                    todo_item = todo_still_items[i + 1]
                    try:
                        print(' ... try to execute mission.')
                        class_name = todo_item['class']
                        func = todo_item['func']
                        args = todo_item['args']

                        c_obj = globals()[class_name](self.msg_executor)
                        func = getattr(c_obj, func)
                        func(*args)
                        print('[CHEER] time mission executed!!!!!!')
                    except KeyError:
                        pass
                    # sleep more 1 minute
                    time.sleep(61)
            else:
                pass
                time.sleep(50)
                # time.sleep(seconds_until_tomorrow + 1)

    def _main_loop(self):
        """
        [UPDATE] all the time object are have no seconds!!!!!!!!!!

        this loop method will keep a breathe check of local file, only when
        the now minutes is event number, that is to say, when it is 8:22 8:24 8:26...
        Cruiser will continues check local file, get all the time object that is
        within 2 minutes from now, and get the function out, execute it.
        todo.pkl file contains object like this:
        [
            {
            'class': 'WeChatSender',
            'func': 'explicit_send_wc',
            'time': datetime.datetime.datetime.datetime.now(),
            'args': (arg1, arg2)
            },

            {
            'class': 'WeChatSender',
            'func': 'explicit_send_wc',
            'time': datetime.datetime.datetime.datetime.now(),
            'args': (arg1, arg2)
            }
        ]
        :return:
        """
        observer = Observer()
        observer.schedule(self.changes_event_handler, path=self.base_dir, recursive=False)
        observer.start()
        while True:
            if os.path.exists(self.todo_local_file):
                with open(self.todo_local_file, 'rb') as f:
                    obj_list = pickle.load(f)

                today_todo_list = [i for i in obj_list if self.is_today_todo(i['time'])]
                self.solve_one_day_todo_events(todo_items_list=today_todo_list)
            else:
                time.sleep(60)
                pass

    def cruise_todo(self):
        print('[CRUISE] todo cruise start...')
        self._main_loop()

    def explicit_remind(self, talk_to_uid, remind_things):
        print('##### fuck!!! this is a todo for {} and content is {}'.format(talk_to_uid, remind_things))
        # send message to talk_to_uid
        remind_msg = random.choice([
            '【提醒】 我是来提醒你{}的'.format(remind_things),
            '【提醒】 是时候{}了啊'.format(remind_things),
            '【提醒】 敲敲，提醒你{}'.format(remind_things)
        ])
        for i in range(4):
            self.msg_executor.send_txt_msg(talk_to_uid, remind_msg)
            time.sleep(1.5)
        self.msg_executor.send_txt_msg(talk_to_uid, '咳咳，重要的事情说三遍。')
        time.sleep(1.5)
        self.msg_executor.send_txt_msg(talk_to_uid, '收到了吗？')
        time.sleep(1.5)


class ChangesHandler(FileSystemEventHandler):
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.todo_local_file = os.path.join(self.base_dir, 'todo.pkl')
        self.CHANGE_FLAG = False

    def on_modified(self, event):
        print("Got it!")
        print('!!!!!!!!!!!!!!!!!!!!file changed!!!!!!detected!!!!!!!!!!!!')
        self.CHANGE_FLAG = True






