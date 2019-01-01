from .precise.precise_chat import PreciseChatter
from .openapi.turing_chat import TuringChatter
import numpy as np


class InferEngine(object):

    def __init__(self, lan='cn', bot_config=None):
        self.chatter = PreciseChatter(lan=lan)
        self.turing_chat = TuringChatter(bot_config)

    def infer(self, text):
        infer = np.random.choice([self.chatter, self.turing_chat], p=[0.1, 0.9])
        return infer.get_response(text)