

import itchat

def a(data):
    def inner_func(d):
        print('fuck ', d)
    return inner_func(data)


@a
def did_receive(data):
    print(data)


if __name__ == '__main__':
    did_receive()