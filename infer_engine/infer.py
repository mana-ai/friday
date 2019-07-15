# from .precise.precise_chat import PreciseChatter
from .openapi.turing_chat import TuringChatter
# from .openapi.baidu_chat import BaiduChatter
import numpy as np


class InferEngine(object):

    def __init__(self, lan='cn', bot_config=None):
        # self.chatter = PreciseChatter(lan=lan)
        self.turing_chat = TuringChatter(bot_config)
        # self.baidu_chat = BaiduChatter()

    def infer(self, text):
        # infer = np.random.choice([self.turing_chat, self.baidu_chat], p=[0.1, 0.9])
        infer = np.random.choice([self.turing_chat], p=[1.0])
        return infer.get_response(text)