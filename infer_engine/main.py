from precise_chat.precise_chat import PreciseChatter



if __name__ == '__main__':

    chatter = PreciseChatter()
    while 1:
        a = input('> ')
        b = chatter.get_response(a)
        print(b)

