# -*- coding: utf-8 -*-
# file: days_answer.py
# author: JinTian
# time: 31/05/2017 11:38 AM
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
this file answer DAYs,
this is very important, for instance, when ask robot :
今天是多少号
明天是星期几
后天是什么日子
25号是星期几
"""
import numpy as np
import re
from utils.chinese_digits_convert import digits_to_cn

from .common_sense.holidays import holidays, search_special_days_by_date, search_special_days_by_name
import jieba.posseg as pseg
import jieba

from utils.time_utils.time_extract import TimeExtractor
from utils.time_utils import lunar_to_solar
from .do import Ability, global_config

MSG_SPLITTER = global_config.msg_splitter


class DaysAnswer(Ability):
    def __init__(self):
        self.self_regex = {
            'ask_date': [r'^.*天.*[几多少]号'],
            'ask_special_day': [r'^.*[是有]?[什么啥].*日子'],
            'ask_week': [r'^.*[天号].*[星期礼拜周]几'],
            'ask_special_day_date': [r'^.*是?[什么啥]时候', r'^.*还有[多少多][天久]']
        }
        super(DaysAnswer, self).__init__()

    @staticmethod
    def get_important_day(date, time_words):
        days = search_special_days_by_date(date)
        print(days)
        if len(days) < 1:
            response = np.random.choice([
                '{}不是什么特别的日子'.format(time_words),
                '{}是个平常日子'.format(time_words)
            ])
            return response
        elif len(days) == 1:
            days = days[0]
            name = days['name']
            custom = days['custom']
            response = np.random.choice([
                '{}是{}啊，这天我们喜欢{}'.format(time_words, name, ''.join(custom)),
                '{}是{}, 你有没有{}'.format(time_words, name, ''.join(custom))
            ])
            return response
        else:
            response = np.random.choice(
                '{}有{}个特殊的日子，{}'.format(time_words, len(days), ' '.join([i['name'] for i in days]))
            )
            return response

    @staticmethod
    def get_special_day_response(special_day_name, year=None):
        if year is None:
            matched_day = search_special_days_by_name(special_day_name)
            if len(matched_day) < 1:
                return '我还真不知道这个节日啥时候'
            else:
                matched_day = matched_day[0]
                if matched_day['calendar'] == 'lunar':
                    month = matched_day['time'].split('-')[0]
                    day = matched_day['time'].split('-')[1]
                    date_string = '农历的{}月{}号'.format(
                        digits_to_cn(month) if int(month) == 1 else '正',
                        digits_to_cn(day) if int(day) <= 10 else '初' + digits_to_cn(day))
                else:
                    date_string = '{}月{}号'.format(special_day_name['time'].split('-')[0], special_day_name[
                        'time'].split('-')[1])
                response = np.random.choice([
                    '{}是在{}'.format(special_day_name, date_string),
                    '{}是在{}$$人们喜欢在这一天{}'.format(special_day_name, date_string, ' '.join(matched_day['custom'])),
                ])
                return response
        else:
            matched_day = search_special_days_by_name(special_day_name)
            if len(matched_day) < 1:
                return '我还真不知道这个节日啥时候'
            else:
                matched_day = matched_day[0]
                if matched_day['calendar'] == 'lunar':
                    solar_date = lunar_to_solar.get_solar_date(year, matched_day['time'].split('-')[0],
                                                               matched_day['time'].split('-')[1])
                    date_string_solar = '公历{}'.format(solar_date.strftime("%m月%d号"))

                    month = matched_day['time'].split('-')[0]
                    day = matched_day['time'].split('-')[1]
                    date_string_lunar = '农历的{}月{}'.format(
                        digits_to_cn(month) if int(month) == 1 else '正',
                        digits_to_cn(day) + '号' if int(day) > 10 else '初' + digits_to_cn(day))
                    response = np.random.choice([
                        '{}通常是在{}' + MSG_SPLITTER + '{}的{}是{}'.format(
                            special_day_name, date_string_lunar, year, special_day_name, date_string_solar),
                        '{}的{}是{}'.format(year, special_day_name, date_string_solar)
                    ])
                    return response
                else:
                    date_string = '公历{}月{}号'.format(matched_day['time'].split('-')[0], matched_day[
                        'time'].split('-')[1])
                    response = np.random.choice([
                        '{}就是在{}'.format(special_day_name, date_string),
                        '{}是在{}$$人们喜欢在这一天{}'.format(special_day_name, date_string, ' '.join(matched_day['custom'])),
                    ])
                return response

    def dispatch_days(self, from_talk):
        all_regex = [i for i in self.self_regex.values()]
        print(all_regex)
        all_categories = [i for i in self.self_regex.keys()]
        all_matched = []
        for one_regex in all_regex:
            matched = 0
            for r in one_regex:
                result = re.findall(r, from_talk)
                if len(result) >= 1:
                    matched += 1
            all_matched.append(matched)
        print('all matched: ', all_matched)
        print('match child category: ', all_categories[np.argmax(all_matched)])
        return all_categories[np.argmax(all_matched)]

    def act(self, from_talk=None, talk_to=None, msg_executor=None, session_hold_bundle=None):
        session_label = None
        params_dict = None
        if session_hold_bundle is not None:
            session_label = session_hold_bundle['session_label']
            params_dict = session_hold_bundle['params_dict']

        talk_to_uid = talk_to
        if isinstance(talk_to, dict):
            talk_to_uid = talk_to['user_addr']
            talk_to = talk_to['user_nick_name']

        extractor = TimeExtractor()
        time_dict = extractor.extract(from_talk)
        if session_label is None:
            if time_dict is not None:
                seg_tag_list = pseg.lcut(from_talk)
                seg_list = [s for s, p in seg_tag_list]
                tag_list = [p for s, p in seg_tag_list]

                time_words = time_dict['time_words'].replace('星期', '')
                # print('tag list from days answer: ', tag_list)
                # if len([i for i in tag_list if i == 't']) < 1:
                #     return '不知道你具体问哪一天呢'
                # else:
                #     time_words = seg_list[tag_list.index([i for i in tag_list if i == 't'][0])]

                dispatch_label = self.dispatch_days(from_talk)
                if dispatch_label == 'ask_date':
                    response = np.random.choice([
                        '{}是{}号'.format(time_words, time_dict['time'].strftime(" %d").replace(' 0', '')),
                        '{}号'.format(time_dict['time'].strftime(" %d").replace(' 0', '')),
                        '{}月{}号'.format(time_dict['time'].strftime(" %m").replace(' 0', ''), time_dict[
                            'time'].strftime(" %d").replace(' 0', ''))
                    ])
                    return response
                elif dispatch_label == 'ask_week':
                    print(time_dict['time'].weekday())
                    print(time_words)
                    week = digits_to_cn(str(time_dict['time'].weekday() + 1))

                    if time_dict['time'].weekday() == 5:
                        response = np.random.choice([
                            '{}礼拜{}' + MSG_SPLITTER + '还可以玩一天'.format(time_words, week)
                        ])
                    elif time_dict['time'].weekday() == 4:
                        response = np.random.choice([
                            '{}礼拜{}' + MSG_SPLITTER + '我最喜欢星期五了$$马上'
                            '' + MSG_SPLITTER + '✌️'.format(time_words, week)
                        ])
                    elif time_dict['time'].weekday() == 0:
                        response = np.random.choice([
                            '{}礼拜{}' + MSG_SPLITTER + '又是星期一了$$得上班了，哎️'.format(time_words, week)
                        ])
                    elif time_dict['time'].weekday() == 6:
                        response = np.random.choice([
                            '{}星期{}$$最后一天假期了$$️心慌'.format(time_words, '天')
                        ])
                    else:
                        response = np.random.choice([
                            '{}礼拜{}'.format(time_words, week)
                        ])
                    return response
                elif dispatch_label == 'ask_special_day':
                    response = self.get_important_day(time_dict['time'], time_words)
                    return response
                elif dispatch_label == 'ask_special_day_date':
                    # ask 端午节是什么时候
                    jieba.load_userdict('utils/time_utils/jieba_user_dict')
                    seg_tag_list = pseg.lcut(from_talk)
                    seg_list = [s for s, p in seg_tag_list]
                    tag_list = [p for s, p in seg_tag_list]
                    if len([i for i in tag_list if i in ['t', 'n']]) < 1:
                        return '我不是很清楚啊'
                    else:
                        except_time_words = ['今年', '明年', '后年', '去年', '时候']
                        ask_day_name = [s for s, t in seg_tag_list if t in ['t', 'n'] and s not in except_time_words][0]
                        print('ask when is ', ask_day_name)
                        if time_dict is not None:
                            # indicates given time
                            when_year = time_dict['time'].strftime("%Y")
                            print('detected year', when_year)
                            return self.get_special_day_response(ask_day_name, when_year)
                        else:
                            return self.get_special_day_response(ask_day_name)
