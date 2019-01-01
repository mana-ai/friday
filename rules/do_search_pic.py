# -*- coding: utf-8 -*-
# file: picture_searcher.py
# author: JinTian
# time: 22/05/2017 9:08 PM
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


from global_session_holder import session_holder
import random
import requests
import re
from .do import Ability
from .do import global_config

MSG_SPLITTER = global_config.msg_splitter


class PictureSearcher(Ability):

    def __init__(self):
        super(PictureSearcher, self).__init__()

    @staticmethod
    def decode_url(url):
        url = url.replace("_z2C$q", ":")
        url = url.replace("_z&e3B", ".")
        url = url.replace("AzdH3F", "/")
        in_table = "wkv1ju2it3hs4g5rq6fp7eo8dn9cm0bla"
        out_table = "abcdefghijklmnopqrstuvw1234567890"
        trans_table = str.maketrans(in_table, out_table)
        url = url.translate(trans_table)
        return url

    def get_picture_url(self, search_keywords=None):
        url_pattern = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&" \
                      "ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0" \
                      "&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
        url = url_pattern.format(word=search_keywords, pn=random.randint(0, 40))
        cleaned_image_urls = []
        html = requests.get(url).text
        image_urls = re.findall('"objURL":"(.*?)",', html, re.S)
        for i, image_url in enumerate(image_urls):
            if i > random.randint(1, 6):
                break
            else:
                try:
                    print('[INFO] decoding url..')
                    image_url = self.decode_url(image_url)
                    # image = requests.get(image_url, stream=False, timeout=10).content
                    cleaned_image_urls.append(image_url)
                except requests.exceptions.ConnectionError:
                    print('[INFO] url: %s can not found image.' % image_url)
                    continue
        # this will return 3 image urls
        return cleaned_image_urls

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

        talk_to_uid = talk_to
        if session_label is None:
            # (?:)按照词语来匹配
            result = re.findall(r'.*[发张](.*)(?:图片|照片|图).*', from_talk)
            if len(result) >= 1:
                print(result)
                keywords = result[0].replace('的', '')
                print('searching image keywords: ', keywords)
                picture_urls = self.get_picture_url(keywords)[:5]

                all_pics = []
                for p_url in picture_urls:
                    all_pics.append(p_url)

                response = random.choice([
                    '看很多{}这样的图片对身体不太好哦{}{}'.format(keywords, MSG_SPLITTER, MSG_SPLITTER.join(all_pics)),
                    MSG_SPLITTER.join(all_pics),
                    '好，找到了这么一些图片' + MSG_SPLITTER + '{}'.format(MSG_SPLITTER.join(all_pics))
                ])
                return response
            else:
                response = random.choice([
                    '你想看什么样的图片',
                    '需要啥样的图片啊',
                    '想看什么图片😈'
                ])
                session_holder.hold(talk_to_uid=talk_to_uid, session_label='ask_what_image',
                                    func_path='PictureSearcher.search_picture', params_dict=None)
                return response
        elif session_label == 'ask_what_image':
            keywords = from_talk.replace('的', '')
            print('searching image keywords: ', keywords)
            picture_urls = self.get_picture_url(keywords)[:5]
            all_pics = []
            for p_url in picture_urls:
                all_pics.append(p_url)
            response = random.choice([
                '看很多{}这样的图片对身体不太好哦' + MSG_SPLITTER + '{}'.format(keywords, MSG_SPLITTER.join(all_pics)),
                MSG_SPLITTER.join(all_pics),
                '好，找到了这么一些图片{}'.format(MSG_SPLITTER.join(all_pics))
            ])
            return response
