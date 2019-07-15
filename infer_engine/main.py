
from infer_engine.openapi.baidu_chat import BaiduChatter


if __name__ == '__main__':
    chatter = BaiduChatter()
    while 1:
        a = input('> ')
        b = chatter.get_response(a)
        print(b)

