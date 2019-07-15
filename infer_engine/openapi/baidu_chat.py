"""


https://unit.gz.baidubce.com/rpc/2.0/unit/bot/chat
"""
import requests
import random
import numpy as np
from alfred.utils.log import logger as logging
import urllib



class BaiduChatter(object):

    def __init__(self):
        self.access_token = None
        self.AK = 'LHfw3wg0wGQNKnj4WZKut79s'
        self.SK = 'W7HDlrMpa5wuCq32HMHabxFd1zYDRNLw'
        self.__init_token()

    def __init_token(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            self.AK, self.SK
        )
        r = requests.get(host)
        self.access_token = r.json()['access_token']

    def baidu_post(self, text):
        url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + self.access_token

        post_data = "{\"log_id\":\"UNITTEST_10000\",\"version\":\"2.0\",\"service_id\":\"S20258\",\"session_id\":\"\",\"request\":{\"query\":\"你好\",\"user_id\":\"88888\"},\"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1057\"]}}}"
        request = requests.post(url, post_data.encode('utf-8'), headers={'Content-Type': 'application/json'})

        logging.info(request.json())
        return request.json()

    def get_response(self, from_talk):
        rp = self.baidu_post(from_talk)
        logging.info(rp)
        if not rp:
            response = np.random.choice([
                '等一下，我麻麻喊我',
                '今天天气不错，要不聊一下天气吧？',
                '我现在有点顾左右而言他',
                '你喜欢看言情小说吗？',
                '我有一千种方式和你开展对话',
                '你觉得我是一个人类吗？'
            ]
            )
        else:
            response = rp
        return response
