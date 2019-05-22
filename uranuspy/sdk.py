# -*- coding: utf-8 -*-
# file: sdk.py
# author: JinTian
# time: 28/05/2018 10:36 AM
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
Simply Uranus Python SDK

"""
import os
import json
import pickle
import requests
import websocket
import datetime
import time
import json
import validators


class UranusUserCard(object):

    def __init__(self):
        self.user_acc = ''
        self.user_nick_name = ''
        self.user_avatar = ''
        self.user_avatar_url = ''
        self.user_addr = ''
        self.user_sign = ''
        self.user_city = ''

    def load_from_response(self, rp):
        rp = rp.json()
        if rp['status'] == 'success':
            data = rp['data']
            self.user_acc = data['user_acc']
            self.user_addr = data['user_addr']
            self.user_nick_name = data['user_nick_name']
            self.user_sign = data['user_sign']
            self.user_city = data['user_city']
            self.user_avatar = data['user_avatar']
            print('## Find user: {}, {}'.format(self.user_acc, self.user_nick_name))



class UranusSDK(object):

    def __init__(self):
        self.token_store_dir = os.path.expanduser('~/.uranuspy')
        if not os.path.exists(self.token_store_dir):
            os.makedirs(self.token_store_dir)
        self.token_store_f = os.path.join(self.token_store_dir, 'uranuspy.pkl')

        self.token = None

        self.user_addr = None
        self.user_nick_name = None
        self.user_acc = None

        self.is_login = False

        self._check_token()

        self.base_url = 'loliloli.pro'
        self.ws_url = 'ws://{}:9000/v1/ws'.format(self.base_url)

        self.base_api_url = 'http://{}:9000/api/v1'.format(self.base_url)
        self.users_url = self.base_api_url + '/users'
        self.find_user_url = self.base_api_url + '/find_user'

    def _check_token(self):
        if os.path.exists(self.token_store_f):
            with open(self.token_store_f, 'rb') as f:
                u = pickle.load(f)
            self.token = u['token']
            self.user_addr = u['user_addr']
            self.user_nick_name = u['user_nick_name']
            self.user_acc = u['user_acc']
            self.is_login = True
        else:
            self.is_login = False

    def login(self, user_acc, user_password):
        login_url = "http://{}:9000/api/v1/users_login".format(self.base_url)
        data = {"user_acc": user_acc, "user_password": user_password}
        rp = requests.post(login_url, data=data)
        if rp.ok:
            rp = rp.json()
            # print(rp)
            if rp['status'] == 'success':
                token = rp["data"]["token"]
                user_addr = rp["data"]["user_addr"]
                user_nick_name = rp["data"]["user_nick_name"]

                u = {
                    'token': token,
                    'user_addr': user_addr,
                    'user_acc': user_acc,
                    'user_nick_name': user_nick_name
                }
                with open(self.token_store_f, 'wb') as f:
                    pickle.dump(u, f)
                self.is_login = True
                print('[uranuspy] login as: ', user_nick_name)
            else:
                print('login failed.')
                exit()
        else:
            print('server not response.')
            exit()

    def hi(self):
        msg = {
            "token": self.token,
            "user_addr": self.user_addr,
            "ua": "py/macos",
            "device": "mac",
            "location": "湖南长沙"
        }
        out_msg = {
            "purpose": "hi",
            "payload": msg
        }
        msg_str = json.dumps(out_msg)
        b = bytes(msg_str, 'utf-8')
        return b

    def get_send_msg(self, target_addr, sender, sender_name, content, msg_type):
        if msg_type == 0:
            msg = {
                "target": target_addr,
                "sender": sender,
                "sender_name": sender_name,
                "target_name": "kkk",
                "content": content,
                "msg_type": msg_type,
                # "time": time.time()
                "time": datetime.datetime.now().isoformat()
            }
        elif msg_type == 1:
            msg = {
                "target": target_addr,
                "sender": sender,
                "sender_name": sender_name,
                "target_name": "kkk",
                # image is bytes
                "content": content,
                # "content_bytes": content,
                "msg_type": msg_type,
                # "time": time.time()
                "time": datetime.datetime.now().isoformat()
            }
        elif msg_type == 2:
            # time to make robot send voice
            msg = {
                "target": target_addr,
                "sender": sender,
                "sender_name": sender_name,
                "target_name": "kkk",
                # voice is bytes
                "content_bytes": content,
                "msg_type": msg_type,
                # "time": time.time()
                "time": datetime.datetime.now().isoformat()
            }

        out_msg = {
            "purpose": "send",
            "payload": msg
        }
        msg_str = json.dumps(out_msg)
        return bytes(msg_str, encoding='utf-8')

    def send_msg(self, target_addr, content, ws):
        msg = self.get_send_msg(target_addr=target_addr, sender=self.user_addr,
                                sender_name=self.user_nick_name,
                                content=content, msg_type=0)
        ws.send(msg)

    def send_img_msg(self, target_addr, content, ws):
        content = list(bytearray(content))
        # print(content)
        msg = self.get_send_msg(target_addr=target_addr, sender=self.user_addr,
                                sender_name=self.user_nick_name,
                                content=content, msg_type=1)
        ws.send(msg)

    def send_img_msg_v2(self, target_addr, content, ws):
        """
        version2 image becomes a url
        :param target_addr:
        :param content:
        :param ws:
        :return:
        """
        if validators.url(content):
            msg = self.get_send_msg(target_addr=target_addr, sender=self.user_addr,
                                    sender_name=self.user_nick_name,
                                    content=content, msg_type=1)
        else:
            msg = self.get_send_msg(target_addr=target_addr, sender=self.user_addr,
                                    sender_name=self.user_nick_name,
                                    content=content, msg_type=0)

        ws.send(msg)

    def send_voice_msg(self, target_addr, content, ws):
        # just convert bytes to int list
        # voice bytes can not convert to int list????????

        content = list(bytearray(content))
        msg = self.get_send_msg(target_addr=target_addr, sender=self.user_addr,
                                sender_name=self.user_nick_name,
                                content=content, msg_type=2)
        ws.send(msg)

global_uranus_sdk = UranusSDK()


