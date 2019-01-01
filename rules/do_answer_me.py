# -*- coding: utf-8 -*-
# file: self_answer.py
# author: JinTian
# time: 19/05/2017 11:37 PM
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
Answer any question about Jarvis himself
"""
import numpy as np
import re

from global_session_holder import session_holder
import random
from .rules import all_rules

from .do import Ability
# from config.config import global_config
from .do import global_config
from config.parse import global_bot

MSG_SPLITTER = global_config.msg_splitter


class SelfAnswer(Ability):

    def __init__(self):
        self.self_regex = {
            'ask_name': [r'.*你叫[啥什么]', r'.*你是谁'],
            'ask_age': [r'.*你多大', r'.*你.*多少岁'],
            'ask_creator': [r'.*你.*主人是[谁哪个]', r'.*[谁哪个].*[创造做发明].*[了的].*你',
                            r'.*你.*爸爸是[谁哪个]', r'你.*谁[做创造制作]'],
            'ask_ability': [r'.*你.*[会能可以].*[做干].*[什么啥]', r'.*你.*[有会具备具有][哪些什么啥].*[功能能力]'],
            'ask_intro': [r'.*介绍.*你自己', r'[做作].*自我介绍.?', r'.?自我介绍.?'],
            'ask_gender': [r'.*你是男.*女?.*', r'.*你的?性别是[啥什么]?']
        }
        super(SelfAnswer, self).__init__()

    def dispatch_self(self, from_talk):
        all_regex = [i for i in self.self_regex.values()]
        print(all_regex)
        all_categories = [i for i in self.self_regex.keys()]
        all_matched = []
        for one_regex in all_regex:
            matched = 0
            for r in one_regex:
                result = re.findall(r, from_talk)
                if len(result) >= 1:
                    matched += 1
            all_matched.append(matched)
        print('all matched: ', all_matched)
        print('match child category: ', all_categories[np.argmax(all_matched)])
        return all_categories[np.argmax(all_matched)]

    def act(self, from_talk=None, talk_to=None, msg_executor=None, session_hold_bundle=None):

        session_label = None
        params_dict = None
        if session_hold_bundle is not None:
            session_label = session_hold_bundle['session_label']
            params_dict = session_hold_bundle['params_dict']

        talk_to_uid = talk_to
        if isinstance(talk_to, dict):
            talk_to_uid = talk_to['user_addr']
            talk_to = talk_to['user_nick_name']

        print('[TALK_TO] talk to: ', talk_to)
        bot = global_bot
        if session_label is None:
            category = self.dispatch_self(from_talk)

            if category == 'ask_name':
                if bot.config.gender == '女':
                    response = bot.get_name_response() + MSG_SPLITTER + '我的名字是从母体脱胎时确定的哦，' \
                                                                        '不过你可以给我取过一个名字，' \
                                                                '你想叫我什么？'
                    session_holder.hold(talk_to_uid=talk_to, session_label='ask_new_name',
                                        func_path='SelfAnswer.answer_self', params_dict=None)
                    return response
                else:
                    print(talk_to)
                    response = random.choice([
                        bot.get_name_response() + MSG_SPLITTER + '你给我的取得名字呀',
                        '{}, 我主人是{}'.format(bot.get_name_response(), talk_to),
                    ])
                    return response
            elif category == 'ask_age':
                response = bot.get_age_response()
                return response
            elif category == 'ask_creator':
                if talk_to == 'master':
                    response = '主人，是你，把我创造出来了'
                    return response
                else:
                    response = bot.get_creator_response()
                    return response
            elif category == 'ask_ability':
                response = bot.get_abilities_response()
                return response
            elif category == 'ask_intro':
                response = bot.get_intro_response()
                return response
            elif category == 'ask_gender':
                return bot.get_gender_response()
        elif session_label == 'ask_new_name':
            from_talk = from_talk.replace('你', '')
            if '叫' in from_talk:
                new_name = from_talk.split('叫')[-1]
                nick_name = new_name[-1] * 2
                response = random.choice([
                    '哇塞我喜欢这个名字, 以后你就叫我{}或者{}吧'.format(new_name, nick_name),
                    '不错的名字！以后可以喊我{}'.format(nick_name),
                    '我终于有自己的名字啦！我的名字就叫{}'.format(new_name),
                    '哇，我的名字是{}，我是你的的机器人啦！'.format(new_name)
                ])
                return response
            else:
                new_name = from_talk
                nick_name = new_name[-1] * 2
                response = random.choice([
                    '哇塞我喜欢这个名字, 以后你就叫我{}或者{}吧'.format(new_name, nick_name),
                    '不错的名字！以后可以喊我{}'.format(nick_name),
                    '我终于有自己的名字啦！我的名字就叫{}'.format(new_name),
                    '哇，我的名字是{}，我是你的的机器人啦！'.format(new_name)
                ])
                return response





