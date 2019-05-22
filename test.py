import json
import requests
import hashlib
import urllib
import random
from urllib.request import quote, unquote



myurl = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i=计算'
rp = requests.get(myurl)
print(rp)
print(rp.json())

# print("翻译结果为：%s"%(target['trans_result']['data'][0]['dst']))