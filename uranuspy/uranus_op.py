# -*- coding: utf-8 -*-
# file: uranus_op.py
# author: JinTian
# time: 2018/6/25 3:56 PM
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
a class for send msg through uranuspy
"""
import numpy as np
from .uranus_sdk import UranusSDK
import pickle
import os
import requests
from .uranus_sdk import UranusUserCard

from alfred.utils.log import logger as logging


class UranusOp(object):
    def __init__(self, user_acc, user_password, uranus_sdk, debug=False):
        """
        this ws must be provide
        """
        self.uranus_sdk = uranus_sdk
        self.ws_conn = None
        self.user_acc = user_acc
        self.user_password = user_password

        self.base_dir = os.path.expanduser('~/.uranuspy')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        self._subscribers_f = os.path.join(self.base_dir, '{}_subscribers.pkl'.format(user_acc))

        self.subscribers_users = []
        self._load_subscribers()
        self.has_connection = False
        self.debug = debug

    def set_ws_conn(self, ws_conn):
        self.ws_conn = ws_conn
        self.has_connection = True

    def _load_subscribers(self):
        if os.path.exists(self._subscribers_f):
            with open(self._subscribers_f, 'rb') as f:
                self.subscribers_users = pickle.load(f)

    def remove_user_from_subscribers(self, user_address):
        if os.path.exists(self._subscribers_f):
            self.subscribers_users = [i for i in self.subscribers_users if i['user_addr'] != user_address]
            with open(self._subscribers_f, 'wb') as f:
                pickle.dump(self.subscribers_users, f)

    def add_user_to_subscribers(self, user_address):
        if len([i for i in self.subscribers_users if i['user_addr'] == user_address]) >= 1:
            pass
        else:
            if os.path.exists(self._subscribers_f):
                to_add = {
                    'user_addr': user_address,
                    'level': 0
                }
                self.subscribers_users.append(to_add)
                with open(self._subscribers_f, 'wb') as f:
                    pickle.dump(self.subscribers_users, f)
            else:
                self.subscribers_users = []
                to_add = {
                    'user_addr': user_address,
                    'level': 0
                }
                self.subscribers_users.append(to_add)
                with open(self._subscribers_f, 'wb') as f:
                    pickle.dump(self.subscribers_users, f)

    def send_msg_to_subscribers(self, msg):
        """
        load subscribers and then send msg
        :param msg:
        :return:
        """
        if self.has_connection:
            if self.debug:
                logging.info('~~~~~~~~ uranuspy now send to subscribers......!!!!!!!!!!!!!!!!!!!!!')
                logging.info('now subscribers: ', self.subscribers_users)
            for item in self.subscribers_users:
                target_address = item['user_addr']
                self.uranus_sdk.send_msg(target_addr=target_address,
                                         content=msg,
                                         ws=self.ws_conn)

        else:
            logging.error('~~~~~~~~ uranuspy send failed. ............................no connection')

    def send_voice_to_subscribers(self, msg_bytes):
        if self.has_connection:
            if self.debug:
                logging.info('~~~~~~~~ uranuspy now send to subscribers......!!!!!!!!!!!!!!!!!!!!!')
                logging.info('[uranuspy] now subscribers: ', self.subscribers_users)
            for item in self.subscribers_users:
                target_address = item['user_addr']
                self.uranus_sdk.send_voice_msg(target_addr=target_address,
                                               content=msg_bytes,
                                               ws=self.ws_conn)
        else:
            logging.error('~~~~~~~~ uranuspy send failed. ............................no connection')

    def get_user_by_user_acc(self, user_acc):
        rp = requests.get(self.uranus_sdk.find_user_url + '?token={}&user_acc={}'.format(self.uranus_sdk.token,
                                                                                         user_acc))
        user = UranusUserCard()
        user.load_from_response(rp)
        return user

    def get_all_friends(self):
        """
        get all my friends
        """
        rp = requests.get(self.uranus_sdk.get_friends_url + '?token={}'.format(self.uranus_sdk.token))
        rp = rp.json()
        if rp['status'] == 'success':
            all_friends = []
            for u in rp['data']:
                user = UranusUserCard()
                user.load_from_dict(u)
                all_friends.append(user)
            return all_friends
        else:
            pass
    
    def get_all_users(self):
        """
        only for level >= 10 users
        """
        all_friends = []
        page_num = 0
        is_last = False
        while not is_last:
            rp = requests.get(self.uranus_sdk.get_allusers_url + '?token={}&page_num={}&per_page=15'.format(
                self.uranus_sdk.token, page_num))
            rp = rp.json()
            if rp['status'] == 'success':
                if rp['data'] != null:
                    for u in rp['data']:
                        user = UranusUserCard()
                        user.load_from_dict(u)
                        all_friends.append(user)
                    page_num += 1
                else:
                    is_last = True
            else:
                pass
        return all_friends

    def send_msg_by_user_acc(self, user_acc, msg):
        if self.has_connection:
            user = self.get_user_by_user_acc(user_acc)
            self.uranus_sdk.send_msg(target_addr=user.user_addr,
                                     content=msg,
                                     ws=self.ws_conn)

        else:
            logging.error('~~~~~~~~ uranuspy send failed. ............................no connection')

    def send_txt_msg(self, target_addr, msg):
        if self.has_connection:
            self.uranus_sdk.send_msg(target_addr, msg, self.ws_conn)
        else:
            logging.error('~~~~~~~~ uranuspy send failed. ............................no connection')
    
    def broadcast_txt_msg(self, msg):
        if self.has_connection:
            # get all friends, then send msg one by one
            # all_friends = self.get_all_friends()
            page_num = 0
            is_last = False
            i = 0
            while not is_last:
                rp = requests.get(self.uranus_sdk.get_allusers_url + '?token={}&page_num={}&per_page=15'.format(
                    self.uranus_sdk.token, page_num))
                rp = rp.json()
                if rp['status'] == 'success':
                    if rp['data'] != None:
                        for u in rp['data']:
                            i += 1
                            user = UranusUserCard()
                            user.load_from_dict(u)
                            # logging.info('broadcasting: {} {}'.format(user.user_addr, user.user_nick_name))
                            self.uranus_sdk.send_msg(user.user_addr, msg, self.ws_conn)
                        page_num += 1
                    else:
                        is_last = True
                else:
                    pass                
            logging.info('Now we finished broadcasting!!')
            self.uranus_sdk.send_msg('usrZK8kZTzEHC', '消息广播完毕....消息共推送到了{}位用户'.format(i), self.ws_conn)
        else:
            logging.error('~~~~~~~~ broadcast_txt_msg send failed. ............................no connection')

    def send_img_msg(self, target_addr, msg):
        if self.has_connection:
            self.uranus_sdk.send_img_msg_v2(target_addr, msg, self.ws_conn)
        else:
            logging.error('~~~~~~~~ uranuspy send failed. ............................no connection')

    def send_voice_msg(self, target_addr, msg):
        if self.has_connection:
            NotImplementedError('You need call Baidu Voice api to generate voice from message.')
        else:
            logging.error('~~~~~~~~ uranuspy send failed. ............................no connection')