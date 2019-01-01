# -*- coding: utf-8 -*-
# file: time_extract.py
# author: JinTian
# time: 29/04/2017 9:46 AM
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
# n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
# m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
# v/动词 a/形容词 d/副词 h/前接成分 k/后接成分 i/习语
# j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
# e/叹词 o/拟声词 g/语素 w/标点 x/其它
import numpy as np
import jieba
import jieba.posseg as pseg
import datetime
from ..chinese_digits_convert import digits_to_cn, cn_to_digits
import re
import os


class TimeExtractor(object):
    """
    this class will extract datetime object from a single
    Chinese sentence, for instance, when from talk is:
    明天早上八点喊我起床

    then, this class will return a time:
    2017-4-30 8:00 A.M in datetime format.

    Basically, this algorithm is simple too.
    First, extract all the time words. Include t and m, when seg.
    And all the noun about time, such as:
    小时，月，年，日，
    """

    def __init__(self):
        jieba.load_userdict(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jieba_user_dict'))
        self._adjust_words()

    @staticmethod
    def _adjust_words():
        jieba.suggest_freq(['今天', '上午'], True)
        jieba.suggest_freq(['今天', '下午'], True)
        jieba.suggest_freq(['今天', '晚上'], True)
        jieba.suggest_freq(['今天', '凌晨'], True)
        jieba.suggest_freq(['今天', '中午'], True)

    @staticmethod
    def _convert_cn(sentence):
        # [UPDATE]
        sentence = digits_to_cn(sentence)
        return sentence

    @staticmethod
    def is_number(uchar):
        """is number"""
        if u'\u0030' <= uchar <= u'\u0039':
            return True
        else:
            return False

    def is_cn_number(self, string):
        num_str = cn_to_digits(string)
        a = [not self.is_number(i) for i in num_str]
        if np.sum(a) < 1:
            return True
        else:
            return False

    # TODO: there something still need to do, like reasoning a time period, such as 两个小时后，两个小时五十分钟后, etc.
    def extract(self, sentence):
        """
        this function will extract time from a sentence
        it contains these process:
        1. convert sentence digits to Chinese characters.
        2. find all time words.
        3. parse month, date and exactly time, here if no date got using today as default date,
        if no month got using this month as default, if no time got using 9:30 as for morning, 2:30 as for afternoon,
        20:00 as for night.

        :param sentence:
        :return:
        """
        # drop 个
        # sentence = sentence.replace('个', '')
        # 有一些基数词比如 点 要加入，有一些不能加入，比如多少
        except_m_words = ['多少', '几', '星期']
        sentence_cn = self._convert_cn(sentence)
        seg_pos_list = pseg.lcut(sentence=sentence_cn)
        period_r = self.parse_period(seg_pos_list)
        if period_r:
            return period_r
        else:
            seg_pos_time = [(s, p) for s, p in seg_pos_list if p == 't' or p == 'm' and s not in except_m_words]
            print(seg_pos_time)
            if len(seg_pos_time) < 1:
                return None
            else:
                year = self.parse_year(sentence)
                date = self.parse_date(seg_pos_time)
                time = self.parse_time(seg_pos_time)
                extracted_time_str = year + '-' + date + ' ' + time
                extracted_time = datetime.datetime.strptime(extracted_time_str, '%Y-%m-%d %H:%M')
                return {'time': extracted_time, 'time_words': cn_to_digits(''.join([s for (s, p) in seg_pos_time]))}

    @staticmethod
    def parse_year(sentence):
        """
        this method will parse year out from a time list
        :return:
        """
        result = re.findall(r'.*\d+年?', sentence)
        print(result)
        if len(result) < 1:
            # maybe it is 明年 后年 前年 明后年
            ano_result = re.findall(r'.*[明后前去明后]年', sentence)
            if len(ano_result) < 1:
                # return current year 2017
                return datetime.datetime.now().strftime("%Y")
            elif ano_result[0] == '明年' or ano_result[0] == '来年':
                return str(datetime.datetime.now().year + 1)
            elif ano_result[0] == '后年':
                return str(datetime.datetime.now().year + 2)
            elif ano_result[0] == '明后':
                return str(datetime.datetime.now().year + 3)
            elif ano_result[0] == '去年':
                return str(datetime.datetime.now().year - 1)
            elif ano_result[0] == '前年':
                return str(datetime.datetime.now().year - 2)
            else:
                return datetime.datetime.now().strftime("%Y")
        else:
            year = result[0].split('年')[0] if '年' in result[0] else result[0]
            if len(year) == 2 and int(year) < 50:
                year = int(year) + 2000
                return str(year)
            else:
                return year

    @staticmethod
    def parse_period(seg_pos_list):
        """
        this method will parse a period time, such as:
        三个半小时后
        两个小时后
        两分钟之后
        两天以后
        --->
        统统变为： 三半小时，两小时，两分钟，两天

        this time is a interval from now, seems more simple to parse
        Algorithm is simple:
        1. judge time words contains ['后', '之后', '以后'], if True, then parse time period
        else, go to specific time parse.
        :return:
        """
        s = [s for s, p in seg_pos_list]
        p = [p for s, p in seg_pos_list]
        print(s, p)
        f_w = [s for s, p in seg_pos_list if p == 'f']
        if len(f_w) < 1:
            return None
        else:
            f_w = f_w[0]
        t_w = [s for s, p in seg_pos_list if p == 't']
        t_w_known = ['小时', '分钟', '天', '秒']
        common = [i for i in t_w if i in t_w_known]
        print(common)
        if f_w in ['后', '之后', '以后'] or len(common) >= 1:
            t_m_dict = dict()
            for w in t_w:
                w_m = []
                for i in range(s.index(w)):
                    if p[s.index(w) - i - 1] == 'm':
                        w_m.insert(0, s[s.index(w) - i - 1])
                    else:
                        break
                if len(w_m) >= 1:
                    t_m_dict[w] = w_m
            print(t_m_dict)
            seconds_digits = 0
            for k in t_m_dict.keys():
                if k == '年':
                    y_m = t_m_dict[k]
                    for m in y_m:
                        if m == '半':
                            seconds_digits += 60 * 60 * 24 * 182
                        else:
                            y_digit = cn_to_digits(m, extract=True)[0]
                            seconds_digits += y_digit * 60 * 60 * 24 * 365
                elif k == '天':
                    d_m = t_m_dict[k]
                    for m in d_m:
                        if m == '半':
                            seconds_digits += 60 * 60 * 12
                        else:
                            d_digit = cn_to_digits(m, extract=True)[0]
                            seconds_digits += d_digit * 60 * 60 * 24
                elif k == '小时':
                    h_m = t_m_dict[k]
                    print(h_m)
                    for m in h_m:
                        if m == '半':
                            seconds_digits += 30 * 60
                        else:
                            h_digit = cn_to_digits(m, extract=True)[0]
                            seconds_digits += h_digit * 60 * 60
                elif k == '分钟':
                    m_m = t_m_dict[k]
                    for m in m_m:
                        if m == '半':
                            seconds_digits += 30
                        else:
                            m_digit = cn_to_digits(m, extract=True)[0]
                            seconds_digits += m_digit * 60
                elif k == '秒钟':
                    s_m = t_m_dict[k]
                    for m in s_m:
                        if m == '半':
                            seconds_digits += 0.5
                        else:
                            m_digit = cn_to_digits(m, extract=True)[0]
                            seconds_digits += m_digit
                else:
                    continue
            print('[TIME] final seconds: ', seconds_digits)
            now = datetime.datetime.now()
            date_and_time = now + datetime.timedelta(seconds=seconds_digits)
            d = seconds_digits // (60 * 60 * 24)
            h = (seconds_digits % (60 * 60 * 24)) // (60 * 60)
            m = (seconds_digits % (60 * 60)) // 60
            d_w = (str(d) + '天') if d > 0 else ''
            h_w = (str(h) + '小时') if h > 0 else ''
            m_w = (str(m) + '分钟') if m > 0 else ''
            time_words = d_w + h_w + m_w + '后'
            return {'time': date_and_time, 'time_words': digits_to_cn(time_words)}
        else:
            return None

    @staticmethod
    def parse_date(seg_pos_time):
        """
        parse month from segmented pair of time words, etc.
        [('明天', 't'), ('早上', 't'), ('八点', 't'), ('半', 'm')]
        this will return:
        2017-4-30
        :param seg_pos_time:
        :return:
        """
        date_words = [s for (s, p) in seg_pos_time if '月' in s or '号' in s or '天' in s]
        print('date words', date_words)
        if len(date_words) < 1:
            return datetime.datetime.now().date().strftime('%m-%d')
        else:
            month_w = [i for i in date_words if '月' in i]
            day_w = [i for i in date_words if '号' in i]
            day_behalf = [i for i in date_words if '天' in i]

            if len(month_w) < 1:
                # indicates, this month
                month_digit = datetime.datetime.now().month
            else:
                if month_w[0] == '下个月':
                    month_digit = datetime.datetime.now().month + 1
                elif month_w[0] == '下下个月':
                    month_digit = datetime.datetime.now().month + 2
                else:
                    month_digit = cn_to_digits(month_w[0], extract=True)[0]

            day_digit = 0
            if len(day_w) < 1 and len(day_behalf) < 1:
                # indicates no specific date, etc. 25号, using today
                day_digit = datetime.datetime.now().day
            elif len(day_behalf) >= 1:
                # solve with day behalf, etc 今天 明天 后天
                day_digit_today = datetime.datetime.now().day
                if day_behalf[0] == '今天':
                    day_digit = datetime.datetime.now().day
                elif day_behalf[0] == '明天':
                    day_digit = (datetime.datetime.now() + datetime.timedelta(days=1)).day
                    if day_digit < day_digit_today:
                        month_digit += 1
                elif day_behalf[0] == '后天':
                    day_digit = (datetime.datetime.now() + datetime.timedelta(days=2)).day
                    if day_digit < day_digit_today:
                        month_digit += 1
                elif day_behalf[0] == '明后天':
                    day_digit = (datetime.datetime.now() + datetime.timedelta(days=3)).day
                    if day_digit < day_digit_today:
                        month_digit += 1
                elif day_behalf[0] == '昨天':
                    day_digit = (datetime.datetime.now() - datetime.timedelta(days=1)).day
                    if day_digit > day_digit_today:
                        month_digit -= 1
                elif day_behalf[0] == '前天':
                    day_digit = (datetime.datetime.now() - datetime.timedelta(days=2)).day
                    if day_digit > day_digit_today:
                        month_digit -= 2

            elif len(day_w) >= 1:
                day_digit = cn_to_digits(day_w[0], extract=True)[0]
            else:
                day_digit = 1

            date_final = str(month_digit) + '-' + str(day_digit)
            return date_final

    def parse_time(self, seg_pos_time):
        """
        this method will parse exactly time from seg_pos_time
        etc.
        [('明天', 't'), ('早上', 't'), ('八点', 't'), ('半', 'm')]
        should return 8:30
        :param seg_pos_time:
        :return:
        """
        day_words = ['上午', '下午', '早上', '早晨', '晚上', '凌晨', '中午', '傍晚', '晚间', '早间']
        time_words = [s for (s, p) in seg_pos_time if '点' in s or p == 'm' or s in day_words]
        '''
        time words must be something like:
        ['早上', '八点', '半']
        ['三点']
        that means, if:
        len(time_words) == 0, return a default time in a time which is 8:00 A.M

        if not is_cn_number(time_words[-1]) or not in ['半', '一刻', '', ''], drop this m word
        '''
        time_words = [i for i in time_words if self.is_cn_number(i) or i in ['半', '一刻'] or '点' in i or i in day_words]
        if len(time_words) < 1:
            # indicates that no exactly time, we will return default time
            return datetime.datetime.strptime('8:30', '%H:%M').time().strftime('%H:%M')
        else:
            day_behalf = [i for i in time_words if i in day_words]
            exactly_time = [i for i in time_words if self.is_cn_number(i) or i in ['半', '一刻'] or '点' in i]

            if len(day_behalf) < 1:
                if len([cn_to_digits(i, extract=True)[0] for i in exactly_time if '点' in i]) < 1:
                    return datetime.datetime.strptime('8:30', '%H:%M').time().strftime('%H:%M')
                else:
                    # indicates that no 上午 or 下午 or 晚上，directly using exactly_time
                    exactly_time_h_digit = [cn_to_digits(i, extract=True)[0] for i in exactly_time if '点' in i][0]
                    # [UPDATE] judge exactly_time_h is bigger than now hour, if it is then using it, if not
                    # using exactly_time_h + 12
                    if exactly_time_h_digit < datetime.datetime.now().hour:
                        exactly_time_h_digit += 12
                    exactly_time_m = [i for i in exactly_time if self.is_cn_number(i) or i in ['半', '一刻']]
                    if len(exactly_time_m) < 1:
                        exactly_time_m_digit = '00'
                    elif exactly_time_m[0] == '半':
                        exactly_time_m_digit = 30
                    elif exactly_time_m[0] == '一刻':
                        exactly_time_m_digit = 15
                    elif self.is_cn_number(exactly_time_m[0]):
                        exactly_time_m_digit = cn_to_digits(exactly_time_m[0], extract=True)[0]
                    else:
                        exactly_time_m_digit = '00'
                    return str(exactly_time_h_digit) + ':' + str(exactly_time_m_digit)
            else:
                if day_behalf[0] in ['上午', '早上', '早晨', '早间']:
                    if len(exactly_time) < 1:
                        # indicate only 下午 晚上 given, no other information
                        # then return 3:00 if 下午, 12:00 if 中午, 8:00 if 晚上
                        return '8:30'
                    else:
                        exactly_time_h_digit = [cn_to_digits(i, extract=True)[0] for i in exactly_time if '点' in i][0]
                        exactly_time_m = [i for i in exactly_time if self.is_cn_number(i) or i in ['半', '一刻']]
                        if len(exactly_time_m) < 1:
                            exactly_time_m_digit = '00'
                        elif exactly_time_m[0] == '半':
                            exactly_time_m_digit = 30
                        elif exactly_time_m[0] == '一刻':
                            exactly_time_m_digit = 15
                        elif self.is_cn_number(exactly_time_m[0]):
                            exactly_time_m_digit = cn_to_digits(exactly_time_m[0], extract=True)[0]
                        else:
                            exactly_time_m_digit = '00'

                        return str(exactly_time_h_digit) + ':' + str(exactly_time_m_digit)
                elif day_behalf[0] in ['下午', '中午', '晚上', '傍晚', '晚间']:
                    if len(exactly_time) < 1:
                        # indicate only 下午 晚上 given, no other information
                        # then return 3:00 if 下午, 12:00 if 中午, 8:00 if 晚上
                        if day_behalf[0] in ['下午']:
                            return '15:00'
                        elif day_behalf[0] in ['中午']:
                            return '12:00'
                        elif day_behalf[0] in ['晚上', '傍晚', '晚间', '夜晚']:
                            return '20:00'
                    else:
                        exactly_time_h_digit = [cn_to_digits(i, extract=True)[0] for i in exactly_time if '点' in i][0]
                        exactly_time_m = [i for i in exactly_time if self.is_cn_number(i) or i in ['半', '一刻']]
                        if len(exactly_time_m) < 1:
                            exactly_time_m_digit = '00'
                        elif exactly_time_m[0] == '半':
                            exactly_time_m_digit = 30
                        elif exactly_time_m[0] == '一刻':
                            exactly_time_m_digit = 15
                        elif self.is_cn_number(exactly_time_m[0]):
                            exactly_time_m_digit = cn_to_digits(exactly_time_m[0], extract=True)[0]
                        else:
                            exactly_time_m_digit = '00'

                        if exactly_time_h_digit < 12:
                            return str(exactly_time_h_digit + 12) + ':' + str(exactly_time_m_digit)
                        else:
                            return str(exactly_time_h_digit) + ':' + str(exactly_time_m_digit)
