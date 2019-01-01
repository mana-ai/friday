# -*- coding: utf-8 -*-
# file: tap_aware.py
# author: JinTian
# time: 22/05/2017 8:56 PM
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
import numpy as np
from .do import global_config
from .do import Ability


class TapAware(Ability):

    def __init__(self):
        super(TapAware, self).__init__()

    def act(self, from_talk=None, talk_to=None, msg_executor=None, session_hold_bundle=None):

        session_label = None
        params_dict = None
        talk_to_uid = talk_to
        if isinstance(talk_to, dict):
            talk_to_uid = talk_to['user_addr']
            talk_to = talk_to['user_nick_name']
        if session_hold_bundle is not None:
            session_label = session_hold_bundle['session_label']
            params_dict = session_hold_bundle['params_dict']

        bot = global_config
        if session_label is None:
            response = np.random.choice([
                'At your service.',
                '{}随便恭候差遣'.format(bot.config.name),
                '{}在此'.format(bot.config.name),
                '有什么可以为您服务的吗',
                '我在呢',
                '叫我干嘛',
                '我在学编程',
                'I am here',
                '有何吩咐',
                '在这里',
                '干嘛',
                '干什么',
                '来了',
                '刚才在编程',
                '来了来了'
            ])
            return response
