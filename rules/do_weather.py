# -*- coding: utf-8 -*-
# file: weather_answer.py
# author: JinTian
# time: 31/05/2017 9:01 AM
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
"""
this method answer weather of any city
使用 知心天气预报 api

"""
import numpy as np
import jieba.posseg as pseg

from global_session_holder import session_holder
from utils.time_utils.time_extract import TimeExtractor
import requests
from .do import global_config

MULTI_MSG_SPLITTER = global_config.msg_splitter


class WeatherAnswer(object):
    def __init__(self):
        pass

    @staticmethod
    def get_weather_by_city_and_time(city, time_dict):
        ask_time = time_dict['time']
        ask_time_words = time_dict['time_words']

        ask_time_string = ask_time.strftime("%Y-%m-%d")

        api_key = 'mn8eynfdnvsu2cju'
        api_token = ''
        base_url = 'https://api.seniverse.com/v3/weather/daily.json?'
        params = {
            'key': api_key,
            'location': city,
            'language': 'zh-Hans',
            'unit': 'c',
            'start': -1,
            'days': 3
        }

        result = requests.get(base_url, params)
        print(result.status_code)
        if result.status_code == 200:
            try:
                result = result.json()
                print(result['results'][0])
                data = result['results'][0]['daily']
                ask_data = [d for d in data if d['date'] == ask_time_string]

                if len(ask_data) < 1:
                    response = '我目前只能知道未来两天的天气噢'
                    return response
                else:
                    ask_data = ask_data[0]
                    weather_day = '{} 温度{}~{}度 风速{}m/s'.format(ask_data['text_day'],
                                                               ask_data['low'], ask_data['high'],
                                                               ask_data['wind_speed'])
                    weather_night = ask_data['text_night']
                    if ask_time.hour > 18:
                        # ask night
                        if '雨' in weather_night:
                            response = np.random.choice([
                                '{}{}的天气{}'.format(city, ask_time_words, weather_night)
                                + MULTI_MSG_SPLITTER + '这是晚上的天气哟' + MULTI_MSG_SPLITTER + '貌似会下雨呢, 记得带雨伞',
                                '{}{}的天气{}'.format(city, ask_time_words, weather_night) + MULTI_MSG_SPLITTER
                                + '晚上的天气就是如此, 出门记得带伞'
                            ])
                        elif '晴' in weather_night or '多云' in weather_night:
                            response = np.random.choice([
                                '{}{}的天气{}'.format(city, ask_time_words,
                                                   weather_night) + MULTI_MSG_SPLITTER + '看上去天气还可以',
                                '{}{}的天气{}'.format(city, ask_time_words,
                                                   weather_night) + MULTI_MSG_SPLITTER + '晚上天气还不错',
                                '{}{}的天气{}'.format(city, ask_time_words,
                                                   weather_night) + MULTI_MSG_SPLITTER + '晚上一起看星星',
                                '{}{}的天气{}'.format(city, ask_time_words, weather_night)
                            ])
                        else:
                            response = np.random.choice([
                                '{}{}的天气{}'.format(city, ask_time_words, weather_night)
                            ])
                    else:
                        # ask day
                        if '雨' in weather_day:
                            if '雨' in weather_night:
                                response = np.random.choice([
                                    '{}{}的天气{}'.format(city, ask_time_words, weather_day) + MULTI_MSG_SPLITTER +
                                    '出门记得带伞哦,晚上貌似也会下雨',
                                    '{}{}的天气{}'.format(city, ask_time_words,
                                                       weather_day) + MULTI_MSG_SPLITTER + '记得带伞,晚上会下大雨'
                                ])
                            elif '晴' in weather_night or '多云' in weather_night:
                                response = np.random.choice([
                                    '{}{}的天气{}'.format(city, ask_time_words, weather_day, weather_night) +
                                    MULTI_MSG_SPLITTER + '记得带伞啊, 不过晚上会转晴',
                                    '{}{}的天气{}'.format(city, ask_time_words,
                                                       weather_day,
                                                       weather_night) + MULTI_MSG_SPLITTER + '出门带伞啊, 不过晚上是多云'
                                ])
                            else:
                                response = np.random.choice([
                                    '{}{}的天气{}'.format(city, ask_time_words, weather_day)
                                ])
                        elif '晴' in weather_day or '多云' in weather_day:
                            if '雨' in weather_night:
                                response = np.random.choice([
                                    '{}{}的天气{}'.format(city, ask_time_words,
                                                       weather_day) + MULTI_MSG_SPLITTER + '看上去天气还可以但是晚上好像会下雨',
                                    '{}{}的天气{}'.format(city, ask_time_words,
                                                       weather_day) + MULTI_MSG_SPLITTER + '白天天气不错但是晚上好像会下雨'
                                ])
                            elif '晴' in weather_night or '多云' in weather_night:
                                response = np.random.choice([
                                    '{}{}的天气{}'.format(city, ask_time_words, weather_day) + MULTI_MSG_SPLITTER +
                                    '看上去天气还可以'
                                    + MULTI_MSG_SPLITTER + '晚上也是晴空万里，哦不，繁星漫天',
                                    '{}{}的天气{}'.format(city, ask_time_words,
                                                       weather_day) + MULTI_MSG_SPLITTER + '难得的好天气',
                                    '{}{}的天气{}'.format(city, ask_time_words,
                                                       weather_day) + MULTI_MSG_SPLITTER + '看上去天气还可以晚上也是'
                                ])
                            else:
                                response = np.random.choice([
                                    '{}{}的天气{}'.format(city, ask_time_words, weather_day)
                                ])
                        else:
                            response = np.random.choice([
                                '{}{}的天气{}'.format(city, ask_time_words,
                                                   weather_day) + MULTI_MSG_SPLITTER + '看上去天气还可以, 但是晚上好像会下雨'
                            ])
                    print(response)
                    return response
            except Exception as e:
                print(e)
                return 'lost connection with internet' + e

        else:
            return '貌似访问不到天气了'

    def act(self, from_talk=None, talk_to=None, msg_executor=None, session_hold_bundle=None):
        session_label = None
        params_dict = None
        if session_hold_bundle is not None:
            session_label = session_hold_bundle['session_label']
            params_dict = session_hold_bundle['params_dict']

        extractor = TimeExtractor()

        talk_to_uid = talk_to
        if isinstance(talk_to, dict):
            talk_to_uid = talk_to['user_addr']
            talk_to = talk_to['user_nick_name']

        time_dict = extractor.extract(from_talk)

        if session_label is None:
            seg_tag_list = pseg.lcut(from_talk)
            seg_list = [s for s, p in seg_tag_list]
            tag_list = [p for s, p in seg_tag_list]

            if 'ns' in tag_list or 'nr' in tag_list:
                # indicates we got city
                city = seg_list[tag_list.index('ns' if 'ns' in tag_list else 'nr')]
                if time_dict is not None:
                    response = self.get_weather_by_city_and_time(city=city, time_dict=time_dict)
                    return response
                else:
                    response = '你想知道{}哪一天的天气?'.format(city)
                    session_holder.hold(talk_to_uid=talk_to_uid, session_label='ask_date',
                                        func_path='WeatherAnswer.act',
                                        params_dict={'city': city})
                    return response
            else:
                if time_dict is not None:
                    response = '告诉我你现在在哪儿'
                    session_holder.hold(talk_to_uid=talk_to_uid, session_label='ask_city',
                                        func_path='WeatherAnswer.act',
                                        params_dict={'time_dict': time_dict})
                    return response
                else:
                    response = '你想知道哪个地方什么时候的天气呢?'
                    session_holder.hold(talk_to_uid=talk_to_uid, session_label='ask_city_and_date',
                                        func_path='WeatherAnswer.act',
                                        params_dict=None)
                    return response

        elif session_label == 'ask_date':
            if time_dict is not None:
                city = params_dict['city']
                response = self.get_weather_by_city_and_time(city, time_dict)
                return response
            else:
                response = '无法识别这个时间'
                return response
        elif session_label == 'ask_city':
            seg_tag_list = pseg.lcut(from_talk)
            seg_list = [s for s, p in seg_tag_list]
            tag_list = [p for s, p in seg_tag_list]
            if 'ns' in tag_list or 'nr' in tag_list:
                # indicates we got city
                city = seg_list[tag_list.index('ns' if 'ns' in tag_list else 'nr')]
                time_dict = params_dict['time_dict']
                response = self.get_weather_by_city_and_time(city, time_dict)
                return response
            else:
                response = '地球上貌似没有{}这个城市啊'.format(from_talk)
                return response
        elif session_label == 'ask_city_and_date':
            seg_tag_list = pseg.lcut(from_talk)
            seg_list = [s for s, p in seg_tag_list]
            tag_list = [p for s, p in seg_tag_list]
            if 'ns' in tag_list or 'nr' in tag_list:
                # indicates we got city
                city = seg_list[tag_list.index('ns' if 'ns' in tag_list else 'nr')]
                response = self.get_weather_by_city_and_time(city, time_dict)
                return response
            else:
                response = '实在不知道您说的哪个城市'
                return response
