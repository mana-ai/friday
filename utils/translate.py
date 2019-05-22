"""

some translation help utilities
"""

import json
import requests
import hashlib
import urllib
import random
from urllib.request import quote, unquote
from alfred.utils.log import logger as logging

myurl = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i={}'


def youdao_translate(q):
    rp = requests.get(myurl.format(q))
    if rp.ok:
        rp = rp.json()
        if rp['errorCode'] == 0:
            res_list = rp['translateResult']
            res = ''
            logging.info(res_list)
            for i, item in enumerate(res_list):
                res += '{}. {}'.format(i, item[0]['tgt'])
            return res
        else:
            return '调取云翻译失败'
    else:
        return '获取服务失败'