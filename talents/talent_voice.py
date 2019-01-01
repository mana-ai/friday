# -*- coding: utf-8 -*-
# file: talent_voice.py
# author: JinTian
# time: 30/04/2018 9:38 PM
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
这是发音天赋，基本操作就是，给我一句话，我读出来，就这么简单
"""
import requests
import os
from playsound import playsound
import platform
import subprocess
from threading import Thread


base_dir = os.path.dirname(os.path.abspath(__file__))
tmp_v_f = os.path.join(base_dir, 'tmp.mp3')
error_f = os.path.join(base_dir, 'error.mp3')


class VoiceBaiDu(object):
    def __init__(self):
        self.client_id = 'emTCOUp14rovGXSsSUC8yBqu'
        self.client_secret = '182fsx2wvDHdFzKjMsbql1iiGIAZafw0'
        self.auth_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}' \
                        '&client_secret={}'.format(self.client_id, self.client_secret)

        self.token = self._get_token()

    def _get_token(self):
        resp = requests.get(self.auth_url)
        if resp.ok:
            return resp.json()['access_token']

    @staticmethod
    def play_f(f):
        print('[ANNOUNCING VOICE]')
        if 'armv' in platform.platform():
            # raspberry pi
            subprocess.Popen(['nohup', 'mplayer', f])
        else:
            try:
                playsound(f)
            except Exception as e:
                print(e)
                playsound(error_f)

    def get_voice_mp3_bytes(self, msg):
        url = 'http://tsn.baidu.com/text2audio?lan=zh&ctp=1&cuid=abcdxxx&tok={}' \
              '&tex={}&vol=9&per=1&spd=5&pit=5'.format(self.token, msg)
        # 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫
        resp = requests.get(url)
        if resp.ok:
            print('RP: ', resp.content)
            return resp.content
        else:
            return open(error_f, 'rb')

    def announce(self, txt):
        url = 'http://tsn.baidu.com/text2audio?lan=zh&ctp=1&cuid=abcdxxx&tok={}' \
              '&tex={}&vol=9&per=1&spd=5&pit=5'.format(self.token, txt)
        # 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫
        resp = requests.get(url)
        if resp.ok:
            with open(tmp_v_f, 'wb') as f:
                f.write(resp.content)
            # self.play_f(tmp_v_f)

            play_thread = Thread(name='greet', target=self.play_f, args=[tmp_v_f])
            play_thread.setDaemon(True)
            play_thread.start()
            return resp.content
        else:
            play_thread = Thread(name='greet', target=self.play_f, args=[error_f])
            play_thread.setDaemon(True)
            play_thread.start()
            return None
            # self.play_f(error_f)
            # print('[VOICE]')

global_baidu_announcer = VoiceBaiDu()

