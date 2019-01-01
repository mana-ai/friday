# -*- coding: utf-8 -*-
# file: talent_hear.py
# author: JinTian
# time: 01/05/2018 11:55 AM
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
听觉能力，对语音进行识别，给出文字
"""
import requests
import os
from playsound import playsound
from aip import AipSpeech
from pydub import AudioSegment
import numpy as np
import wave

base_dir = os.path.dirname(os.path.abspath(__file__))
tmp_v_f = os.path.join(base_dir, 'tmp.mp3')
error_f = os.path.join(base_dir, 'error.mp3')


class HearBaiDu(object):
    def __init__(self):
        self.app_id = ''
        self.app_key = 'emTCOUp14rovGXSsSUC8yBqu'
        self.secret_secret = '182fsx2wvDHdFzKjMsbql1iiGIAZafw0'
        self.client = AipSpeech(self.app_id, self.app_key, self.secret_secret)

    @staticmethod
    def get_f_content(f):
        with open(f, 'rb') as fp:
            return fp.read()

    def hear(self, mp3_f):
        sound = AudioSegment.from_mp3(mp3_f)
        tmp_wav_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp_hear.wav')
        tmp_pcm_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp_hear.pcm')
        sound.export(tmp_wav_f, format="wav")

        # with wave.open(tmp_wav_f) as fd:
        #     params = fd.getparams()
        #     _, _, rate, n_frames = params[:4]
        #     str_data = fd.readframes(n_frames)
        #     print(rate)

        rp = self.client.asr(self.get_f_content(tmp_wav_f), 'pcm', 16000, {
            'dev_pid': '1536',
        })
        print('[语音识别结果] ', rp)
        if rp['err_msg'] == 'success.':
            results = rp['result']
            return results[0]
        else:
            return '没有识别出这句话的意思'
