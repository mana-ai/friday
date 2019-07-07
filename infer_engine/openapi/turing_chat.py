# -*- coding: utf-8 -*-
# file: turing_chatter.py
# author: JinTian
# time: 02/05/2017 4:09 PM
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
import requests
import os
import numpy as np


class TuringChatter(object):

    def __init__(self, bot_config):
        self.api_url = "http://www.tuling123.com/openapi/api?"
        self.api_key = ['82de1ac7c22146e1815aeb546edc6159',
            '4a27247501d242e1a1a05bbdce2228ca']
        self.crt_apikey = self.api_key[0]
        self.bot = bot_config

    def change_apikey(self):
        if self.crt_apikey == self.api_key[0]:
            self.crt_apikey = self.api_key[1]
        elif self.crt_apikey == self.api_key[1]:
            self.crt_apikey = self.api_key[0]
        # elif self.crt_apikey == self.api_key[2]:
        #     self.crt_apikey = self.api_key[0]

    def get_response(self, from_talk):
        data = {
            'key': self.crt_apikey,
            'info': from_talk,
            'userid': 'nicholas_jela',
        }
        try:
            r = requests.post(self.api_url, data=data).json()
            response = r.get('text')
            if '图灵' in response:
                response = str(response).replace('图灵', self.bot.name)
            if '当天请求次数已用完' in response:
                self.change_apikey()
                response = np.random.choice([
                    '等一下，我麻麻喊我',
                    '今天天气不错，要不聊一下天气吧？',
                    '我现在有点顾左右而言他',
                    '你喜欢看言情小说吗？',
                    '我有一千种方式和你开展对话',
                    '你觉得我是一个人类吗？'
                ]
                )
            return response
        except Exception as e:
            print(e)
            return '我主人喊我回家吃饭啦'


