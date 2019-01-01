# -*- coding: utf-8 -*-
# file: uranus_agent.py
# author: JinTian
# time: 28/05/2018 10:34 AM
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
this Uranus client
"""
import threading
import ssl
import six
import websocket
import json

from uranuspy.sdk import UranusSDK
from uranuspy.sdk import global_uranus_sdk
from uranuspy.uranus_op import UranusOp


TEXT_MSG = 0
IMG_MSG = 1
VOICE_MSG = 2
CONTACT_MSG = 3


_OPCODE_DATA = (websocket.ABNF.OPCODE_TEXT, websocket.ABNF.OPCODE_BINARY)


class UranusCore(object):
    def __init__(self, user_acc, user_password, debug=False):
        self.user_acc = user_acc
        self.user_password = user_password
        self.uranus_sdk = global_uranus_sdk
        self.ws = None
        self.debug = debug
        self.uranus_op = UranusOp(user_acc, user_password, self.debug)

    def get_global_op(self):
        return self.uranus_op

    def run_forever(self):
        if self.uranus_sdk.is_login:
            try:
                self.ws = websocket.create_connection(self.uranus_sdk.ws_url)
                self.uranus_op.set_ws_conn(self.ws)
                thread = threading.Thread(target=self.recv_ws)
                # thread.daemon = True
                thread.start()
                self.ws.send(self.uranus_sdk.hi())
                print('[uranuspy] auto serving as {}'.format(self.user_acc))
            except Exception as e:
                self.ws.close()
                print(e)
                print('try re-login...')

        else:
            print('[Uranus] now login')
            self.uranus_sdk.login(self.user_acc, self.user_password)

    def recv(self):
        try:
            frame = self.ws.recv_frame()
        except websocket.WebSocketException:
            return websocket.ABNF.OPCODE_CLOSE, None
        if not frame:
            raise websocket.WebSocketException("Not a valid frame %s" % frame)
        elif frame.opcode in _OPCODE_DATA:
            return frame.opcode, frame.data
        elif frame.opcode == websocket.ABNF.OPCODE_CLOSE:
            self.ws.send_close()
            return frame.opcode, None
        elif frame.opcode == websocket.ABNF.OPCODE_PING:
            self.ws.pong(frame.data)
            return frame.opcode, frame.data
        return frame.opcode, frame.data

    def recv_ws(self):
        ws = self.ws
        while True:
            try:
                opcode, data = self.recv()
                msg = None
                if six.PY3 and opcode == websocket.ABNF.OPCODE_TEXT and isinstance(data, bytes):
                    data = str(data, "utf-8")
                if opcode in _OPCODE_DATA:
                    msg = data
                    if 'test' not in msg:
                        msg_json = json.loads(msg)
                        purpose = msg_json['purpose']
                        if purpose == 'init':
                            print('[uranuspy] init process')
                            # we only need to get those unread msg from history messages
                            all_history_msgs = msg_json['payload']
                            print('[uranuspy] got history msgs: ', len(all_history_msgs))
                            for msg in all_history_msgs:
                                if not msg['read']:
                                    rtn = self.msgs_callback(msg)
                                    if rtn:
                                        self.uranus_op.send_txt_msg(msg['sender'], rtn)

                        else:
                            rtn = self.msgs_callback(msg_json['payload'])
                            if rtn:
                                self.uranus_op.send_txt_msg(msg_json['payload']['sender'], rtn)
                else:
                    pass
            except Exception as e:
                print('!! got an exception in msg callback function, this error automatically catched '
                      'by uranuspy and send back to'
                      'us, full error trace back are: {}'.format(e))
                self.uranus_op.send_msg_by_user_acc('fanghezi', e.__str__())

    @staticmethod
    def msgs_callback(msg):
        """
        the default msg callback
        :param msg:
        :return:
        """
        return 'echo: ' + msg['content']

    def register_callback(self, func):
        self.msgs_callback = func


