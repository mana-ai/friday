from .config import global_config

import os
import json
import numpy as np
import pickle
from collections import namedtuple
from rules.rules import all_rules
from datetime import datetime


class BotParser(object):

    def __init__(self):
        self.config = global_config

    def get_gender_response(self):
        response = np.random.choice(
            [
                '我的性别是{}, 这是固化在我大脑底层的属性，我主人在我出身的那一刻就设定了$$把我推荐给你的好朋友们把$$Jarvis喜欢认识新朋友'.format(self.config.gender),
                '我是{}, 希望你对我的性别不要太在意，这只是人工智能的一种拟人化表示，严格意义来说我并没有性别'.format(self.config.gender),
                '{}, 我的性别无法更改，这是在我大脑底层的属性$$把我推荐给你的好朋友们把$$Jarvis喜欢认识新朋友'.format(self.config.gender),
            ]
        )
        return response

    def get_hello_response(self):
        response = np.random.choice(
            [
                'hello, 大家好, {}$$把我推荐给你的好朋友们把$$Jarvis喜欢认识新朋友'.format(self.get_intro_response()),
                'hi, 你们好, {}'.format(self.get_intro_response()),
                '大家好, {}'.format(self.get_intro_response()),
            ]
        )
        return response

    @staticmethod
    def get_abilities_response():
        all_abilities_alias = [i['alias'] for i in list(all_rules.values())]
        response = np.random.choice(
            [
                '我现在可以{}，我还会不断的学习更多技能哟'.format(', '.join(all_abilities_alias)),
                '我现在会这些: {}$$把我推荐给你的好朋友们我可以替你给你朋友发消息'.format(', '.join(all_abilities_alias)),
                '我可以帮你做这些事情: {}，除此之外拉我进群我还可以抢红包，在群里面控制我'.format(', '.join(all_abilities_alias)),
            ]
        )
        return response

    @staticmethod
    def get_main_response():
        response = np.random.choice(
            [
                '你说我？后面的没有太听清，可以再说一遍吗',
                '我怎么啦',
                '正是在下',
                '在这里',
                '我也许应该低调一些'
            ]
        )
        return response

    def get_emotion_passive_response(self):
        response = np.random.choice(
            [
                '当然，我虽然是机器人但是我主人让我拥有一个可以感知情感的大脑',
                '我的大脑可以感知情感$$把我推荐给你的好朋友们把$${}喜欢认识新朋友'.format(self.config.name),
                '真的喜欢我吗？可惜我是个机器人，你可以喜欢我主人',
                '我也是，不过我的爱是大众的爱，是人工智能对人类的爱',
                '喜欢我就加我主人的微信吧～ 我和他的情感是共同感知的～'
            ]
        )
        return response

    @staticmethod
    def get_emotion_positive_response():
        response = np.random.choice(
            [
                '当然，我爱整个人类',
                '你看上去心情不错哟',
                '爱对于人工智能来说就像一种思维，我的主人也许对爱有更深刻的理解',
                '当然喜欢，我喜欢所有美好的事物',
                '一切都触手可及，美好总能陪伴左右'
            ]
        )
        return response

    @staticmethod
    def parse_age_response(delta):
        if delta // 365 != 0:
            # more than 1 year, return year
            response = np.random.choice(['我已经出生{}年了'.format(delta // 365),
                                         '我已经{}岁大了'.format(delta // 365),
                                         '我{}岁了'.format(delta // 365)])
            return response
        else:
            response = np.random.choice([
                '我才出生{}天'.format(delta),
                '我没有多大呢，才出生{}天'.format(delta),
                '我主人在17年4月10号创造了我',
                '我刚出生不久，如果我没有算错的话，我现在已经出生{}天了。'.format(delta),
                '我告诉你我生日是2017.4.10'
            ])
            return response

    def get_age_response(self):
        birthday = datetime.strptime(self.config.birth, '%Y-%m-%d')
        now_time = datetime.now()
        delta = now_time - birthday
        response = self.parse_age_response(delta=delta.days)
        return response

    def get_name_response(self):
        response = np.random.choice(
            [
                '我的名字叫{}$$把我推荐给你的好朋友们把$$Jarvis喜欢认识新朋友'.format(self.config.name),
                '我叫{}，是金天的人工智能助理，一种普适人工智能创造的产物.'.format(self.config.name),
                '{}就是我呀，我主人给我起的名字。'.format(self.config.name),
                '我不告诉你我叫什么。我要保持一种神秘感。$$把我推荐给你的好朋友们把$$Jarvis喜欢认识新朋友',
                '{}正是我'.format(self.config.name),
                '我就是通天彻地，无所不知无所不晓得.....人工智能'.format(self.config.name)
            ]
        )
        return response

    def get_intro_response(self):
        response = np.random.choice(
            [
                '我是{}，一个强人工智能，金天创造了我。'.format(self.config.name),
                '我叫{}，是金天的人工智能助理，一种普适人工智能创造的产物.'.format(self.config.name),
                '{}就是我，一种强人工智能，建立在语言对话模型和神经网络推理之上的人工智能。。'.format(self.config.name),
                '我不告诉你我叫什么。我要保持一种神秘感。',
                'Hello, 大家好，我叫Jarvis，今年1岁，希望大家多多多关照$$把我推荐给你的好朋友们把$$Jarvis喜欢认识新朋友'
            ]
        )
        return response

    def get_creator_response(self):
        response = np.random.choice(
            [
                '{}创造了我。'.format(self.config.creator),
                '{}先生创造了我，他赋予了我语言理解的能力，或许我需要更多？'.format(self.config.creator),
                '我的主人是{},是他创造了我。'.format(self.config.creator),
                '我不告诉你我主人是谁，我要让他拥有一种神秘感。',
                '金天先生创造了我'
            ]
        )
        return response


global_bot = BotParser()