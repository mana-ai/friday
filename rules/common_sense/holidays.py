# -*- coding: utf-8 -*-
# file: holidays.py
# author: JinTian
# time: 31/05/2017 1:07 PM
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
this first elementary knowledge: holidays
this file will write down all holidays in a year,
such as 端午节, 春节, 中秋节，劳动节，妇女节，儿童节，清明节
later on will also write down all special days in a year
世界爱眼日，世界读书日
"""
import datetime
from utils.time_utils import lunar_to_solar
import numpy as np

holidays = [
    {
        'time': '1-1',
        'name': '元旦',
        'alias': ['元旦节', '新年开始'],
        'calendar': 'solar',
        'custom': ['西方一年的起始', '西方新年到了']
    },
    {
        'time': '12-8',
        'name': '腊八节',
        'alias': ['腊八', '腊八粥'],
        'calendar': 'lunar',
        'custom': ['喝腊八粥', '吃辣条']
    },
    {
        'time': '12-23',
        'name': '大寒',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['大雪纷飞的时候', '和诸葛亮谈人生']
    },
    {
        'time': '12-23',
        'name': '小年',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['吃羹', '贴对联']
    },
    {
        'time': '12-30',
        'name': '除夕',
        'alias': ['除夕夜', '团圆', '团圆夜'],
        'calendar': 'lunar',
        'custom': ['家人团聚', '吃团圆饭']
    },
    {
        'time': '1-1',
        'name': '春节',
        'alias': ['过年', '中国年', '过大年'],
        'calendar': 'lunar',
        'custom': ['岁岁年年有今朝', '拜年去啦']
    },
    {
        'time': '1-7',
        'name': '立春',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['万物复苏的季节', '春天来了']
    },
    {
        'time': '1-15',
        'name': '元宵节',
        'alias': ['元宵'],
        'calendar': 'lunar',
        'custom': ['吃元宵', '看灯展']
    },
    {
        'time': '2-14',
        'name': '情人节',
        'alias': [''],
        'calendar': 'solar',
        'custom': ['给对象买只花', '单身狗表示收到了一万点伤害']
    },
    {
        'time': '2-8',
        'name': '惊蛰',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['春雨贵如油', '美好的季节']
    },
    {
        'time': '3-8',
        'name': '妇女节',
        'alias': [''],
        'calendar': 'solar',
        'custom': ['女人的节日', '女人放假']
    },
    {
        'time': '3-7',
        'name': '女生节',
        'alias': [''],
        'calendar': 'solar',
        'custom': ['女生的节日', '给女生送花赢好感']
    },
    {
        'time': '3-8',
        'name': '清明节',
        'alias': ['清明', '扫墓节', '扫墓'],
        'calendar': 'lunar',
        'custom': ['扫墓', '祭拜祖先']
    },
    {
        'time': '2-15',
        'name': '春分',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['马上暮春了', '小禾苗都应该长大了']
    },

    {
        'time': '5-1',
        'name': '劳动节',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['三天小长假哦', '出去玩啦']
    }
    ,
    {
        'time': '5-14',
        'name': '母亲节',
        'alias': [''],
        'calendar': 'solar',
        'custom': ['给母亲送花', '给家里打电话']
    }
    ,
    {
        'time': '4-26',
        'name': '小满',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['天气变热了', '夏天临近']
    }
    ,
    {
        'time': '5-5',
        'name': '端午节',
        'alias': ['端午', '粽子节', '粽子'],
        'calendar': 'lunar',
        'custom': ['吃粽子', '看划龙舟']
    },

    # summer --------------------------
    {
        'time': '5-11',
        'name': '芒种',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['农民伯伯开始种禾苗', '河水涨起来了']
    }
    ,
    {
        'time': '6-14',
        'name': '小暑',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['太阳当空照', '没有花了']
    },
    {
        'time': '6-1',
        'name': '儿童节',
        'alias': ['小孩子的节日', '小孩节'],
        'calendar': 'solar',
        'custom': ['儿童们的节日', '买棒棒糖吃']
    }
    ,
    {
        'time': '5-27',
        'name': '夏至',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['夏天来了', '天气越来越热']
    }
    ,
    {
        'time': '6-29',
        'name': '大暑',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['越来越热', '需要冰棒']
    }
    ,
    {
        'time': '7-7',
        'name': '七夕',
        'alias': ['中国情人节', '牛郎织女节'],
        'calendar': 'lunar',
        'custom': ['牛郎织女约会', '中国情人节']
    }
    ,
    {
        'time': '6-16',
        'name': '立秋',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['秋天到了', '开始刮风了']
    }
    ,
    {
        'time': '7-17',
        'name': '白露',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['开始打霜了', '天气变冷']
    }
    ,
    {
        'time': '8-4',
        'name': '秋分',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['秋天过了大半', '树叶开始脱落']
    }
    ,
    {
        'time': '8-15',
        'name': '中秋节',
        'alias': ['中秋', '月饼节', '嫦娥节'],
        'calendar': 'lunar',
        'custom': ['今天的月亮最圆', '看着嫦娥姐姐吃着月饼']
    }
    ,
    {
        'time': '10-1',
        'name': '国庆',
        'alias': ['国庆节'],
        'calendar': 'solar',
        'custom': ['七天长假', '出去玩络']
    }
    ,
    {
        'time': '9-19',
        'name': '立冬',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['冬天来了', '天气变冷']
    }
    ,
    {
        'time': '11-1',
        'name': '万圣节',
        'alias': ['南瓜节', '鬼节'],
        'calendar': 'solar',
        'custom': ['西方的南瓜日', '你去演鬼了吗']
    }
    ,
    {
        'time': '11-11',
        'name': '光棍节',
        'alias': [''],
        'calendar': 'solar',
        'custom': ['一年又一年光棍日', '情侣的情人节，单身狗的光棍节']
    }
    ,
    {
        'time': '8-4',
        'name': '秋分',
        'alias': [''],
        'calendar': 'lunar',
        'custom': ['秋天过了大半', '树叶开始脱落']
    }
    ,
    {
        'time': '12-24',
        'name': '平安夜',
        'alias': [''],
        'calendar': 'solar',
        'custom': ['吃个苹果平平安安', '话说平安夜吃苹果是中国的习俗么(谐音平)']
    }
    ,
    {
        'time': '12-25',
        'name': '圣诞节',
        'alias': [''],
        'calendar': 'solar',
        'custom': ['西方过年日', '圣诞老人来了吗', 'Merry Christmas!!!']
    }
    ,
    {
        'time': '12-26',
        'name': '毛主席诞辰',
        'alias': [''],
        'calendar': 'solar',
        'custom': ['毛爷爷的生日', '多少人还记得呢']
    }

]


def search_special_days_by_date(date):
    assert isinstance(date, datetime.datetime), 'must given datetime object'
    date_string = date.strftime("%Y-%m-%d")
    print('query intent date string: ', date_string)
    year = date.year

    matched_days = []
    for item in holidays:
        calendar = item['calendar']
        if calendar == 'lunar':
            month = item['time'].split('-')[0]
            day = item['time'].split('-')[1]
            normalized_date = lunar_to_solar.get_solar_date(year, month, day)
        else:
            normalized_date = datetime.datetime.strptime('{}-{}'.format(year, item['time']), '%Y-%m-%d')
        item_date_string = normalized_date.strftime("%Y-%m-%d")
        if date_string == item_date_string:
            matched_days.append(item)
        else:
            pass
    return matched_days


def search_special_days_by_name(special_day_name):
    """
    many times we need to search a holy day by a not very specific name,
    such as :
    中秋 中秋节 月饼节 嫦娥节
    all these words should indicates it is 中秋节
    so we add a alias list in each days item, we will search both name and alias to get matched object
    :param special_day_name:
    :return:
    """
    matched_days = []
    every_matched_alias_num = []

    for item in holidays:
        if special_day_name == item['name']:
            matched_days.append(item)
        else:
            # continue search
            alias_num = 0
            for a in item['alias']:
                if special_day_name == a:
                    alias_num += 1
            every_matched_alias_num.append(alias_num)
    alias_match_time_index = [every_matched_alias_num.index(i) for i in every_matched_alias_num if i >= 1]
    for i in alias_match_time_index:
        matched_days.append(holidays[i])
    print('all match days: ', matched_days)
    return matched_days

