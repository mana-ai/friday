# -*- coding: utf-8 -*-
# file: config.py
# author: JinTian
# time: 30/04/2018 5:50 PM
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
Read config.json and return the configs
"""
import os
import json
import numpy as np
import pickle
from collections import namedtuple


config_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')


class Config(object):
    def __init__(self):
        with open(config_f, 'r') as f:
            a = json.load(f)
        self.msg_splitter = a['msg_splitter']
        self.supported_coins = a['supported_coins']

        self.msg_splitter = a['msg_splitter']

        self.msg_add_friend_welcome = '''我是智能推荐AI，欢迎添加我
------------------------------
你可以通过以下菜单来方便的查找任何商品的优惠券哦
【帮助】: 显示本帮助
【签到】: 每天签到都会奖励一定金额，达到10元即可随时提现，我们会直接转账现金到您支付宝
【余额】: 你每买一件商品，机器人都会为你从淘宝申请优惠，可以随时查看你的余额
【代理】: 你可以通过联系我们成为我们的代理，即可拥有自己的生意机器人吧~'''

        self.msg_yue = '''当前余额💰💰：
----------------------------
【可提现】: {}元
【未确认收货】: {}元
【预计总收入】: {}元'''

        self.ads_url = [
            'http://suo.im/2pZhWW',
            'http://suo.im/BVrSj',
        ]
        self.msg_coups_search_by_keywords = '''找到商品{}优惠券信息：
----------------------------
【原价】: {}元
【券后价格】: {}元
【省】: {}元
复制口令{}到淘宝即可领取优惠券，下单立减
来自伯爵返利机器人: ''' + np.random.choice(self.ads_url) + '\n更多商品请查看FD优惠商城：http://fd.luoli-luoli.com'

        self.sign_in = '''签到成功💰💰：
----------------------------
【获取奖励】: {}元
【可提现收入】: {}元
【累计总收入】: {}元
                '''

        self.msg_new_in_chat_room = '''
                欢迎入群，我是Jarvis，你的私人助理
                '''
        self.ratio_commission = 0.2
        self.pid_config_f = 'core/config/推广位.pkl'

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.muted_chat_room_f = os.path.join(self.base_dir, 'muted_chat_room.pkl')

        self.pid_config_f = 'core/config/推广位.pkl'
        self.pid_config_f = 'core/config/推广位.pkl'
        self.pid_config_f = 'core/config/推广位.pkl'

        config = namedtuple('config', 'name gender birth creator')

        # ================ the configuration of robot ================
        config.name = 'Friday'
        config.gender = '女'
        config.birth = '2018-12-11'
        config.creator = '金天'
        self.config = config



global_config = Config()
