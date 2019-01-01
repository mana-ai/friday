# -*- coding: utf-8 -*-
# file: things_reminder.py
# author: JinTian
# time: 16/11/2017 9:31 PM
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
remind things that people specific
"""
import numpy as np

import jieba.posseg as pseg
from global_session_holder import session_holder
from utils.time_utils.time_extract import TimeExtractor
import re

from cruisers.create_todo import create_todo
import random
import time
from .do import Ability


class ThingsReminder(Ability):

    def __init__(self):
        super(ThingsReminder, self).__init__()
        self.msg_executor = None

    # @staticmethod
    # def explicit_remind(talk_to_uid, remind_things):
    #     print('##### fuck!!! this is a todo for {} and content is {}'.format(talk_to_uid, remind_things))
    #     # send message to talk_to_uid
    #     remind_msg = random.choice([
    #         '【提醒】 我是来提醒你{}的'.format(remind_things),
    #         '【提醒】 是时候{}了啊'.format(remind_things),
    #         '【提醒】 敲敲，提醒你{}'.format(remind_things)
    #     ])
    #     global_uranus_op.send_txt_msg(talk_to_uid, remind_msg)

    def act(self, from_talk, talk_to=None, msg_executor=None, session_hold_bundle=None):
        self.msg_executor = msg_executor
        session_label = None
        params_dict = None
        talk_to_uid = talk_to
        if isinstance(talk_to, dict):
            talk_to_uid = talk_to['user_addr']
            talk_to = talk_to['user_nick_name']

        if session_hold_bundle is not None:
            session_label = session_hold_bundle['session_label']
            params_dict = session_hold_bundle['params_dict']
        time_extractor = TimeExtractor()
        time_dict = time_extractor.extract(from_talk)
        if time_dict:
            time_datetime = time_dict['time']
            time_words = time_dict['time_words']
        else:
            time_datetime = None
            time_words = '不知道是什么时间'

        if session_label is None:
            seg_tag_list = pseg.lcut(from_talk)
            seg_list = [s for s, p in seg_tag_list]
            tag_list = [p for s, p in seg_tag_list]

            things = re.findall(r'.*(?:提醒|喊|叫)(.*)', from_talk)
            if len(things) >= 1:
                things = things[0].replace('我', '')
                print('-- things: ', things)

            else:
                things = from_talk

            if time_datetime is None:
                response = np.random.choice([
                    '你想让我什么时候提醒你？',
                    '什么时候提醒？',
                    '请告诉我提醒时间，比如两分钟后，下午三点'
                ])
                session_holder.hold(talk_to_uid=talk_to_uid, session_label='ask_time',
                                    func_path='ThingsReminder.remind_things',
                                    params_dict={'remind_things': things})
                return response
            else:
                response = np.random.choice([
                    '好啊，我会在{}提醒你'.format(time_words),
                    '没问题，我会在{}提醒你{}'.format(time_words, things)
                ])
                create_todo('ToDoCruiser', 'explicit_remind', args=(talk_to_uid, things),
                            time_=time_datetime)
                return response

        elif session_label == 'ask_time':
            things = params_dict['remind_things']
            response = np.random.choice([
                '好啊，我会在{}提醒你'.format(time_words),
                '没问题，我会在{}提醒你{}'.format(time_words, things, msg_executor)
            ])
            # TODO create a todo event
            create_todo('ToDoCruiser', 'explicit_remind', args=(talk_to_uid, things),
                        time_=time_datetime)
            return response
