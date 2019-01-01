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
from .sdk import UranusSDK
import pickle
import os
import requests
from .sdk import UranusUserCard


class UranusOp(object):
    def __init__(self, user_acc, user_password, debug=False):
        """
        this ws must be provide
        """
        self.uranus_sdk = UranusSDK()
        self.ws_conn = None
        self.user_acc = user_acc
        self.user_password = user_password

        self.base_dir = os.path.expanduser('~/.uranuspy')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        self._subscribers_f = os.path.join(self.base_dir, 'subscribers.pkl')

        self.subscribers_users = []
        self._load_subscribers()
        self.has_connection = False
        self.debug = debug

    def set_ws_conn(self, ws_conn):
        self.ws_conn = ws_conn
        self.has_connection = True

    #     self._login()
    #
    # def _login(self):
    #     if self.uranus_sdk.is_login:
    #         print('[uranuspy global op] op login and online now, ready for pushing messages.')
    #         try:
    #             self.ws_conn = websocket.create_connection(self.uranus_sdk.ws_url)
    #             self.ws_conn.send(self.uranus_sdk.hi())
    #         except Exception as e:
    #             self.ws_conn.close()
    #             print(e)
    #             print('try re-login...')
    #
    #     else:
    #         print('[Uranus Op] now login')
    #         self.uranus_sdk.login(self.user_acc, self.user_password)

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
                print('~~~~~~~~ uranuspy now send to subscribers......!!!!!!!!!!!!!!!!!!!!!')
                print('now subscribers: ', self.subscribers_users)
            for item in self.subscribers_users:
                target_address = item['user_addr']
                self.uranus_sdk.send_msg(target_addr=target_address,
                                         content=msg,
                                         ws=self.ws_conn)

        else:
            print('~~~~~~~~ uranuspy send failed. ............................no connection')

    def send_voice_to_subscribers(self, msg_bytes):
        if self.has_connection:
            if self.debug:
                print('~~~~~~~~ uranuspy now send to subscribers......!!!!!!!!!!!!!!!!!!!!!')
                print('[uranuspy] now subscribers: ', self.subscribers_users)
            for item in self.subscribers_users:
                target_address = item['user_addr']
                self.uranus_sdk.send_voice_msg(target_addr=target_address,
                                               content=msg_bytes,
                                               ws=self.ws_conn)
        else:
            print('~~~~~~~~ uranuspy send failed. ............................no connection')

    def get_user_by_user_acc(self, user_acc):
        rp = requests.get(self.uranus_sdk.find_user_url + '?token={}&user_acc={}'.format(self.uranus_sdk.token,
                                                                                         user_acc))
        user = UranusUserCard()
        user.load_from_response(rp)
        return user

    def send_msg_by_user_acc(self, user_acc, msg):
        if self.has_connection:
            user = self.get_user_by_user_acc(user_acc)
            self.uranus_sdk.send_msg(target_addr=user.user_addr,
                                     content=msg,
                                     ws=self.ws_conn)

        else:
            print('~~~~~~~~ uranuspy send failed. ............................no connection')

    def send_txt_msg(self, target_addr, msg):
        if self.has_connection:
            self.uranus_sdk.send_msg(target_addr, msg, self.ws_conn)
        else:
            print('~~~~~~~~ uranuspy send failed. ............................no connection')

    def send_img_msg(self, target_addr, msg):
        if self.has_connection:
            self.uranus_sdk.send_img_msg_v2(target_addr, msg, self.ws_conn)
        else:
            print('~~~~~~~~ uranuspy send failed. ............................no connection')

    def send_voice_msg(self, target_addr, msg):
        if self.has_connection:
            NotImplementedError('You need call Baidu Voice api to generate voice from message.')
        else:
            print('~~~~~~~~ uranuspy send failed. ............................no connection')