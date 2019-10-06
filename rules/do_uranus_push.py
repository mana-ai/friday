'''

Push notifications in uranus
by the help of notifer

broadcast messages

'''
import gitlab
from .do import Ability
from global_session_holder import session_holder
from alfred.utils.log import logger as logging
# from uranus_solver import global_uranus_op



class UranusPusher(Ability):

    def __init__(self):
        pass
    
    def act(self, from_talk=None, talk_to=None, msg_executor=None, session_hold_bundle=None):
        session_label = None
        params_dict = None
        if session_hold_bundle is not None:
            session_label = session_hold_bundle['session_label']
            params_dict = session_hold_bundle['params_dict']

        if session_label == 'ask_content':
            talk_to_uid = talk_to
            content = from_talk
            if talk_to_uid == 'usrZK8kZTzEHC' or talk_to_uid == 'usrItug3Lj2c5':
                return content
            else:
                return '糟糕，被你发现了隐藏的功能，可这是一个高度机密操作，您的权限还不够'
        else:
            talk_to_uid = talk_to
            if isinstance(talk_to, dict):
                talk_to_uid = talk_to['user_addr']
                talk_to = talk_to['user_nick_name']
            # 添加mana会员 jintian
            # 添加strangeai会员 jintian
            if len(from_talk.split(' ')) > 1:
                content = from_talk.split(' ')[-1]
            else:
                content = None
            logging.info('push content: {}'.format(content))
            if content == '' or not content:
                session_holder.hold(talk_to_uid=talk_to_uid, session_label='ask_content',
                                    func_path='UranusPusher.act', params_dict={})
                return '请告诉我你要广播的内容'
            else:
                if talk_to_uid == 'usrZK8kZTzEHC' or talk_to_uid == 'usrItug3Lj2c5':
                    # start pushing 
                    if msg_executor != None:
                        msg_executor.broadcast_txt_msg(content)
                        return '消息已广播📢.'
                    else:
                        return 'msg_executor is None, can not perform.'
                else:
                    return '糟糕，被你发现了隐藏的功能，可这是一个高度机密操作，您的权限还不够'

