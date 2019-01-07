"""
solve subscribe command

"""
import numpy as np
from .do import Ability


class PushSubscriber(Ability):

    def __init__(self):
        super(PushSubscriber, self).__init__()

    def act(self, from_talk, talk_to=None, msg_executor=None, session_hold_bundle=None):
        talk_to_uid = talk_to
        if isinstance(talk_to, dict):
            talk_to_uid = talk_to['user_addr']
            talk_to = talk_to['user_nick_name']

        if '取消' in from_talk:
            msg_executor.remove_user_from_subscribers(talk_to_uid)
            return np.random.choice([
                '好的, {}，已经取消了推送，你还可以随时订阅哦'.format(talk_to),
                '那我就不打扰你了，你还可以随时订阅我哦',
            ])
        else:
            msg_executor.add_user_to_subscribers(talk_to_uid)
            return np.random.choice([
                '好的，以后你可以接收到我的实时提醒',
                '订阅成功，我将会每天给你推送信息，包括新闻、大家关注的东西、日程提醒等信息',
            ])
