"""
father class of abilities
"""
from config.config import global_config


class Ability(object):

    def __init__(self, msg_executor=None):
        self.msg_executor = msg_executor

    def act(self, from_talk, talk_to=None, msg_executor=None, session_hold_bundle=None):
        pass
