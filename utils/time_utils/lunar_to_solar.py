# -*- coding: utf-8 -*-
# file: lunar_to_solar.py
# author: JinTian
# time: 31/05/2017 2:04 PM
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
this file simply convert lunar to solar:
2017年十月初五 -> datetime(2017-12-01)
"""
import numpy as np
import datetime

LUNAR_CALENDAR_TABLE = [
    0x04AE53, 0x0A5748, 0x5526BD, 0x0D2650, 0x0D9544, 0x46AAB9, 0x056A4D, 0x09AD42, 0x24AEB6, 0x04AE4A,
    # //*1901-1910*/
    0x6A4DBE, 0x0A4D52, 0x0D2546, 0x5D52BA, 0x0B544E, 0x0D6A43, 0x296D37, 0x095B4B, 0x749BC1, 0x049754,
    # //*1911-1920*/
    0x0A4B48, 0x5B25BC, 0x06A550, 0x06D445, 0x4ADAB8, 0x02B64D, 0x095742, 0x2497B7, 0x04974A, 0x664B3E,
    # //*1921-1930*/
    0x0D4A51, 0x0EA546, 0x56D4BA, 0x05AD4E, 0x02B644, 0x393738, 0x092E4B, 0x7C96BF, 0x0C9553, 0x0D4A48,
    # //*1931-1940*/
    0x6DA53B, 0x0B554F, 0x056A45, 0x4AADB9, 0x025D4D, 0x092D42, 0x2C95B6, 0x0A954A, 0x7B4ABD, 0x06CA51,
    # //*1941-1950*/
    0x0B5546, 0x555ABB, 0x04DA4E, 0x0A5B43, 0x352BB8, 0x052B4C, 0x8A953F, 0x0E9552, 0x06AA48, 0x6AD53C,
    # //*1951-1960*/
    0x0AB54F, 0x04B645, 0x4A5739, 0x0A574D, 0x052642, 0x3E9335, 0x0D9549, 0x75AABE, 0x056A51, 0x096D46,
    # //*1961-1970*/
    0x54AEBB, 0x04AD4F, 0x0A4D43, 0x4D26B7, 0x0D254B, 0x8D52BF, 0x0B5452, 0x0B6A47, 0x696D3C, 0x095B50,
    # //*1971-1980*/
    0x049B45, 0x4A4BB9, 0x0A4B4D, 0xAB25C2, 0x06A554, 0x06D449, 0x6ADA3D, 0x0AB651, 0x093746, 0x5497BB,
    # //*1981-1990*/
    0x04974F, 0x064B44, 0x36A537, 0x0EA54A, 0x86B2BF, 0x05AC53, 0x0AB647, 0x5936BC, 0x092E50, 0x0C9645,
    # //*1991-2000*/
    0x4D4AB8, 0x0D4A4C, 0x0DA541, 0x25AAB6, 0x056A49, 0x7AADBD, 0x025D52, 0x092D47, 0x5C95BA, 0x0A954E,
    # //*2001-2010*/
    0x0B4A43, 0x4B5537, 0x0AD54A, 0x955ABF, 0x04BA53, 0x0A5B48, 0x652BBC, 0x052B50, 0x0A9345, 0x474AB9,
    # //*2011-2020*/
    0x06AA4C, 0x0AD541, 0x24DAB6, 0x04B64A, 0x69573D, 0x0A4E51, 0x0D2646, 0x5E933A, 0x0D534D, 0x05AA43,
    # //*2021-2030*/
    0x36B537, 0x096D4B, 0xB4AEBF, 0x04AD53, 0x0A4D48, 0x6D25BC, 0x0D254F, 0x0D5244, 0x5DAA38, 0x0B5A4C,
    # //*2031-2040*/
    0x056D41, 0x24ADB6, 0x049B4A, 0x7A4BBE, 0x0A4B51, 0x0AA546, 0x5B52BA, 0x06D24E, 0x0ADA42, 0x355B37,
    # //*2041-2050*/
    0x09374B, 0x8497C1, 0x049753, 0x064B48, 0x66A53C, 0x0EA54F, 0x06B244, 0x4AB638, 0x0AAE4C, 0x092E42,
    # //*2051-2060*/
    0x3C9735, 0x0C9649, 0x7D4ABD, 0x0D4A51, 0x0DA545, 0x55AABA, 0x056A4E, 0x0A6D43, 0x452EB7, 0x052D4B,
    # //*2061-2070*/
    0x8A95BF, 0x0A9553, 0x0B4A47, 0x6B553B, 0x0AD54F, 0x055A45, 0x4A5D38, 0x0A5B4C, 0x052B42, 0x3A93B6,
    # //*2071-2080*/
    0x069349, 0x7729BD, 0x06AA51, 0x0AD546, 0x54DABA, 0x04B64E, 0x0A5743, 0x452738, 0x0D264A, 0x8E933E,
    # //*2081-2090*/
    0x0D5252, 0x0DAA47, 0x66B53B, 0x056D4F, 0x04AE45, 0x4A4EB9, 0x0A4D4C, 0x0D1541, 0x2D92B5  # //*2091-2099*/
]

# 下面的三个表格是农历数据表 LunarCalendarTable 的结构。总共使用了32位整数的0～23位。
#
# 6 5                4 3 2 1 0
# 表示春节的公历月份 表示春节的公历日期
#
# 19 18 17 16 15 14 13 12 11 10  9  8  7
# 1   2  3  4  5  6  7  8  9 10 11 12 13
# 农历1-13 月大小 。月份对应位为1，农历月大(30 天),为0 表示小(29 天)
#
# 23 22 21 20
# 表示当年闰月月份，值为0 为则表示当年无闰月。

# 存储阳历月份天数
MONTH_DAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# 返回阳历年所给月份的总天数
def get_syear_total_month_days(syear, smonth):
    days = MONTH_DAYS[smonth]  # 每月总天数
    if (syear % 4 == 0 and syear % 100 != 0) or (syear % 400 == 0):
        if smonth == 2:  # 闰年2月总天数为29天,平年为28天
            days += 1
    return days


def get_syear_total_days(syear):
    total_days = 0
    for i in range(1, 13):
        d = get_syear_total_month_days(syear=syear, smonth=i)
        total_days += d
    return total_days


# 返回给定年1月1日到给定日期的总天数
def get_days_of_syear(syear, smonth, sday):
    days = sday
    for m in range(1, smonth):
        days += get_syear_total_month_days(syear, m)
    return days


# 判断是否为闰月，是，返回True，否，返回False
def is_leap_lmonth(lyear, lmonth):
    leap_month = (LUNAR_CALENDAR_TABLE[lyear - 1901] >> 20) & 0xF  # 为0表示无闰月
    if leap_month != 0 and lmonth == leap_month:
        return True
    else:
        return False


# 返回至当前农历日期的总共间隔天数
def get_lunar_days_to_lday(lyear, lmonth, lday, is_leap_month):
    lunar_days = 0  # 正月初一到给定农历日期的总天数
    lmonth_index = lday_index = 1  # 农历月份，日期遍历索引
    leap_month_days = 0  # 暂存闰月前月的天数
    bits = 19  # 遍历获取大小月索引, 大月:1, 小月:0

    # 　遍历月份至当前月，累加得到总间隔天数，若有闰月出现，则有三种情形：
    # １.给定月份小于闰月;
    # ２.给定月份就是闰月
    # ３.给定月份在闰月之后
    for lmonth_index in range(1, 14):
        l_big_month = (LUNAR_CALENDAR_TABLE[lyear - 1901] >> bits) & 0x1  # 当前月大小

        # 　农历月份所以小于给定月份，所有情况适用
        if lmonth_index < lmonth:
            lunar_days += 29 + l_big_month  # 加上当前月天数
        # 如果当前索引为闰月数字，则暂存其天数，情况２适用
        if is_leap_lmonth(lyear, lmonth_index):
            leap_month_days = 29 + l_big_month
            # 暂存当前月(其下月为闰月)天数  # 当前索引减１月份为闰月，若又闰月出现，则索引数字表示实际月份+1，所以需要特殊处理
        if is_leap_lmonth(lyear, lmonth_index - 1):
            if lmonth_index - 1 == lmonth and is_leap_month:  # 情况２，给定月为闰月
                lunar_days += leap_month_days
                break
            if lmonth_index == lmonth:
                lunar_days += 29 + l_big_month  # 加上当前月（闰月）天数
                break
            if lmonth_index - 1 < lmonth and lmonth_index != lmonth:  # 给定月大于闰月的下一月，即当前月份索引为实际月份+1
                lmonth += 1  # 索引月份+1，则lmonth＋１进行下一轮比较
        bits -= 1  # 跳至下个月
    lunar_days += lday  # 加上农历日期天数
    return lunar_days


# 根据计算处理的天数间隔和年份，求阳历月和日
def get_solar_month_day(syear, solar_days_to_calculate):
    smonth = 1
    while solar_days_to_calculate - get_syear_total_month_days(syear, smonth) > 0:
        solar_days_to_calculate -= get_syear_total_month_days(syear, smonth)
        smonth += 1
    sday = solar_days_to_calculate
    return smonth, sday


# 根据给定农历年月日及是否闰月求阳历年月日
def get_solar_date(lyear, lmonth, lday, is_leap_month=False):
    if isinstance(lyear, str):
        lyear = int(lyear)
    if isinstance(lmonth, str):
        lmonth = int(lmonth)
    if isinstance(lday, str):
        lday = int(lday)

    is_leap_month &= is_leap_lmonth(lyear, lmonth)  # 判断是否闰月
    lunar_days = get_lunar_days_to_lday(lyear, lmonth, lday, is_leap_month)  # 正月初一至当前农历日期天数间隔

    # 获取当前农历年份正月初一所在阳历日期
    spring_month = (LUNAR_CALENDAR_TABLE[lyear - 1901] & 0x60) >> 5
    spring_day = spring_day = LUNAR_CALENDAR_TABLE[lyear - 1901] & 0x1F
    solar_days_to_spring_day = get_days_of_syear(lyear, spring_month, spring_day)  # 从阳历１月１日至正月初一阳历日期的时间间隔

    solar_days_to_calculate = solar_days_to_lday = solar_days_to_spring_day + lunar_days - 1
    total_solar_year_days = get_syear_total_days(lyear)  # 365 or 366

    syear = lyear  # 阳历日期
    # 如果阳历年已翻年
    if solar_days_to_lday > total_solar_year_days:
        solar_days_to_calculate = solar_days_to_lday - total_solar_year_days
        syear += 1  # 阳历年+1

    smonth, sday = get_solar_month_day(syear, solar_days_to_calculate)
    solar_date = datetime.datetime.strptime("{}-{}-{} 8:30".format(syear, smonth, sday), "%Y-%m-%d %H:%M")
    return solar_date
