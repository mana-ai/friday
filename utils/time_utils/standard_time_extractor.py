# -*- coding: utf-8 -*-
# file: standard_time_extractor.py
# author: JinTian
# time: 11/11/2017 2:06 PM
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
import os
import numpy as np
import re
import datetime


class StandardTimeExtractor(object):

    def __int__(self):
        pass

    @staticmethod
    def extract_mode_1(sentence):
        """
        solve mode of 11月11号 03:40
        :param sentence:
        :return:
        """
        if '今天' in sentence or '今日' in sentence:
            month = datetime.datetime.now().strftime('%m')
            day = datetime.datetime.now().strftime('%d')
        elif '昨天' in sentence or '昨日' in sentence:
            month = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%m')
            day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d')
        elif '前天' in sentence or '前日' in sentence:
            month = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%m')
            day = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%d')
        elif '明天' in sentence or '明日' in sentence:
            month = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%m')
            day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d')
        elif '后天' in sentence or '后日' in sentence:
            month = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%m')
            day = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%d')
        elif '大后天' in sentence or '大后日' in sentence:
            month = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%m')
            day = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%d')
        else:
            month = re.findall(r'(\d+)?月', sentence)
            day = re.findall(r'(\d+)?[号日]', sentence)
            if len(month) >= 1:
                month = month[0]
            else:
                month = '11'
            if len(day) >= 1:
                day = day[0]
            else:
                day = '11'

        time = re.findall(r'(\d+:\d+)+', sentence)
        if len(time) >= 1:
            time = time[0]
        else:
            time = '00:00'

        year = datetime.datetime.now().strftime('%Y')
        return year + '-' + month + '-' + day + ' ' + time

    def extract(self, sentence):
        """
        this method extract time from some standard string extract time, such as:
        11月10号 02:30
        1.12 23:30
        :param sentence:
        :return:
        """
        if '月' in sentence or '号' in sentence or '日' in sentence or '天' in sentence:
            return self.extract_mode_1(sentence)
