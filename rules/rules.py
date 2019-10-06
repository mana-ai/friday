# -*- coding: utf-8 -*-
# file: order_regex.py
# author: JinTian
# time: 17/05/2017 8:24 PM
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
Here is the registered command repository, all commands wants to get
called must register a regex to match that unique command executor function

Basically, commands and regex if a dictionary, like this:

{
    'ClassName.execute_method': [r'regex1', r'regex2'],
    ...
}

"""

# todo: every time add one command add in router and resume_session.py

all_rules = {
    # 'JokeTeller.tell_joke': {
    #     'regex': [r'.*讲.*笑话'],
    #     'alias': '讲笑话'
    # },
    # 'WhoAnswer.act': {
    #     'regex': [r'.*[^主人你爸爸]是谁', r'.*是什么人', r'.*知道.*是谁吗'],
    #     'alias': '查找人物'
    # },
    'SelfAnswer.act': {
        'regex': [r'.*你叫[啥什么]', r'.*你是谁.?^', r'.*你多大', r'.*你.?多少岁', r'.*你.*主人是[谁哪个]',
                  r'.*[谁哪个].*[创造做发明].*[了的].*你', r'.*你.*爸爸是[谁哪个]', r'你.*谁[做创造制作]',
                  r'.*你.*[会能可以].*[做干].*[什么啥]', r'.*你.*[有会具备具有][哪些什么啥].*[功能能力]',
                  r'[做作].*自我介绍.?', r'.?自我介绍.?',
                  r'.*介绍.*你自己', r'.*你是男.*女?.*', r'.*你的?性别是[啥什么]?'],
        'alias': '问关于我的事情'
    },
    'TapAware.act': {
        'regex': [r'^[Jj]arvis$', r'^小jj$', r'^小Jar$', r'^小jar$', r'^jj$', r'^贾维斯$'],
        'alias': '唤醒我'
    },
    'WeatherAnswer.act': {
        'regex': [r'^.*天气$', r'^.*天气.*[怎么咋]样', r'^.*天气如何', r'^.*天气是什么', r'^.*天气吗'],
        'alias': '查天气'
    },
    'DaysAnswer.act': {
        'regex': [r'^.*天.*[几多少]号', r'^.*[是有]?[什么啥].*日子', r'^.*[天号].*[星期礼拜周]几',
                  r'^.*是?[什么啥]时候', r'^.*还有[多少多][天久]'],
        'alias': '问我日期'
    },
    'PictureSearcher.act': {
        'regex': [r'^.*[发].*[图片照片]', r'^.*[发张].*[图]'],
        'alias': '给你发图片'
    },
    # 'WbSubscriber.subscribe_wb': {
    #     'regex': [r'^.*(?:关注|订阅).*微博', r'^.*微博.*通知.*[一下]?', r'^.*最近.*微博',
    #               r'^.*[最]?新.*微博', r'^.*最[新近].*微博动态'],
    #     'alias': '拿到任何用户的最新微博'
    # },
    'PushSubscriber.act': {
        'regex': [r'^订阅推送$', r'^订阅消息', r'^我要订阅推送', r'^取消推送', r'^取消推送消息',
                  r'^取消订阅推送'],
        'alias': '订阅推送'
    },

    'ThingsReminder.act': {
        'regex': [r'^.*[提醒].*[我俺哥姐姐爸爸老子].*'],
        'alias': '提醒你做事情'
    },
    # 'NameChanger.change_name': {
    #     'regex': [r'^.*[取换].*个.*[名字]'],
    #     'alias': '给我取名字'
    # },
    # 'MailSender.send_mail': {
    #     'regex': [r'^.*[发].*[邮件]', r'^.*[发].*[mail]'],
    #     'alias': '发送邮件'
    # },

    # 'DeviceAdder.add_device': {
    #     'regex': [r'^.*[添加加入].*(?:设备|终端)', r'^.*[把].*(?:设备|终端).*[添加加入]'],
    #     'alias': '添加物联网设备'
    # },
    # 'IoTController.control_iot': {
    #     'regex': [r'^.*[打开].*灯.*', r'^.*把.*灯[打开].*', r'^.*[熄关].*灯.*', r'^.*把.*灯[熄关掉].*',
    #               r'^.*[打开].*电脑', r'^.*把.*电脑[打开].*',
    #               r'^.*[关].*电脑.*', r'^.*把.*电脑[关掉].*机?.*',
    #               r'^.*[打开].*电风扇', r'^.*把.*电风扇[打开].*',
    #               r'^.*[关].*电风扇.*', r'^.*把.*电风扇[关掉].*',
    #               r'^.*我.*有哪些.*[设备终端].*', r'^.*把我的.*[设备终端].*[列举展示].*', r'^.*列举.*我的[设备终端]',
    #               r'^.*我.*[设备终端].*有[哪些什么]'],
    #     'alias': '在世界上任何一个角落控制你的物联网设备'
    # },
    # 'WebSniffer.sniff_web': {
    #     'regex': [r'^.*[有出现]?.*[什么哪些]?.*[项目仓库]'],
    #     'alias': '告诉你当下最牛逼的开源项目'
    # },

    # 'PaperSniffer.sniff_paper': {
    #     'regex': [r'^.*[最]?新.*论文.*', r'^.*把最新.*论文发.*我', r'^.*发一下最新.*论文', r'^.*有什么[最]?新.*论文吗',
    #               r'^.*有什么.*论文吗', r'^.*领域[最]?[新]?.*论文'],
    #     'alias': '告诉你从量子物理到金融学的最新论文'
    # },
    # 'GoodsSearcher.act': {
    #     'regex': [r'.*[找]', r'.*[买]', r'.*有.*优惠券吗'],
    #     'alias': '找商品'
    # },
    # 'YueSearcher.act': {
    #     'regex': [r'.*[查余额]', r'.*[余额]'],
    #     'alias': '查余额'
    # },
    # 'ShowHelp.act': {
    #     'regex': [r'.*[显示帮助]', r'.*[帮助]', r'^菜单$', r'显示菜单'],
    #     'alias': '查余额'
    # },

    # =========== WeChat Group Sender ===========
    # 'GroupSender.act': {
    #     'regex': [r'^群发', r'^群发一下', r'^帮我群发一条消息'],
    #     'alias': '群发'
    # },
    # 'OfferItems.act': {
    #     'regex': [r'^优惠商品$', r'^优惠商城$'],
    #     'alias': '获取优惠商品'
    # },
    # 'AdminSet.act': {
    #     'regex': [r'^设置权限$', r'^设置主人$'],
    #     'alias': '设置权限'
    # },
    # 'SignIn.act': {
    #     'regex': [r'^签到$', r'.*签到$'],
    #     'alias': '签到'
    # },
    # 'GoodsSubscriber.act': {
    #     'regex': [r'^订阅商品$', r'^订阅优惠券$', r'^我要订阅商品$', r'^取消订阅', r'^取消订阅商品',
    #               r'^取消订阅优惠券'],
    #     'alias': '订阅商品'
    # },

    # -------- Add translate function ---------------
    'Translator.act': {
        'regex': [r'^.*翻译 '],
        'alias': '翻译'
    },
    # -------- Add gitlab related function ---------------
    'GitlabAdder.act': {
        'regex': [r'.*[添加|开通|加入].*会员'],
        'alias': '添加奇异gitlab会员'
    },
    # -------- Add uranus notification pusher -------------
    'UranusPusher.act': {
        'regex': [r'.*[推送|广播|发送].*[消息|通知]'],
        'alias': '推送uranus系统通知'
    },


    # -------- Add translate function ---------------






    # -------- Add translate function ---------------



}
