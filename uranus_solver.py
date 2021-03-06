from uranuspy.core import UranusCore

from infer_engine.infer import InferEngine
from rules.rules_router import RulesRouter
from global_session_holder import resume_session
from config.config import global_config
from utils.regex_verify import is_image_url
import time
from alfred.utils.log import logger as logging
import numpy as np


MSG_SPLITTER = global_config.msg_splitter
infer_engine = InferEngine(bot_config=global_config.config)
global_uranus_op = None

NOTI_ADDR = 'usrfNzS5ZYIzo'
FRID_ADDR = 'usrh8hqEpSWLG'

bot2_op = None
bot2_grafting_container = dict()
bot2_master_replies = ['今天天气真不错']


def send_splitter_msg(msg, talk_to):
    rp_list = msg.split(MSG_SPLITTER)
    for rp in rp_list:
        if is_image_url(rp):
            global_uranus_op.send_img_msg(talk_to, rp)
        else:
            global_uranus_op.send_txt_msg(talk_to, rp)
        time.sleep(2)


# solve message arrived
def msg_callback(data):
    """
    data is a simple message structure

    sender:
    sender_name:
    content:
    content_bytes:
    target:
    target_name:
    :param data:
    :return:
    """
    try:
        from_talk = data['content']
        sender_name = data['sender_name']
        talk_to = data['sender']
        if talk_to != NOTI_ADDR and talk_to != FRID_ADDR:
            print('-- [incoming bot1] {}:  {}'.format(sender_name, from_talk))
            talk_to_dict = {
                'user_nick_name': sender_name,
                'user_addr': talk_to,
            }

            # first detect the rules
            if resume_session.should_resume(talk_to):
                rp = resume_session.resume_session(from_talk, talk_to)
                if rp is not None:
                    send_splitter_msg(rp, talk_to)
            else:
                rules_router = RulesRouter()
                rp = rules_router.reasoning_command(from_talk, talk_to_dict, global_uranus_op)
                if rp is not None:
                    logging.info('rule result: {}\n\n'.format(rp))
                    send_splitter_msg(rp, talk_to)
                else:
                    rp = infer_engine.infer(from_talk)
                    logging.info('inference result: {}\n\n'.format(rp))
                    if MSG_SPLITTER in rp:
                        send_splitter_msg(rp, talk_to)
                    else:
                        return rp
        else:
            logging.info('passing this message from myself: {} {}'.format(sender_name, talk_to))
    except Exception as e:
        # logging.info(data)
        print(e)
        # logging.error('{}'.format(e))


def msg_callback_2(data):
    """
    data is a simple message structure

    sender:
    sender_name:
    content:
    content_bytes:
    target:
    target_name:
    :param data:
    :return:
    """
    try:
        from_talk = data['content']
        sender_name = data['sender_name']
        talk_to = data['sender']
        logging.info('-- [incoming bot2] {} {}:  {}'.format(talk_to, sender_name, from_talk))
        talk_to_dict = {
            'user_nick_name': sender_name,
            'user_addr': talk_to,
        }
        if talk_to == 'usrZK8kZTzEHC' or talk_to == 'usrItug3Lj2c5':
            bot2_master_replies.append(from_talk)
            # this is me, solving my command.
            rules_router = RulesRouter()
            rp = rules_router.reasoning_command(from_talk, talk_to_dict, bot2_op)
            if rp is not None:
                logging.info('rule result: {}\n\n'.format(rp))
                return rp
            else:
                rp = infer_engine.infer(from_talk)
                logging.info('inference result: {}\n\n'.format(rp))
                if MSG_SPLITTER in rp:
                    send_splitter_msg(rp, talk_to)
                else:
                    return rp
        else:
            # sender others msg to me
            from_talk = '[{}@{}]: {}'.format(sender_name, talk_to, from_talk)
            bot2_grafting_container[sender_name] = from_talk
            bot2_op.send_txt_msg('usrZK8kZTzEHC', from_talk)
            bot2_op.send_txt_msg('usrItug3Lj2c5', from_talk)
            bot2_op.send_txt_msg(talk_to, np.random.choice(bot2_master_replies))
    except Exception as e:
        print(e)

     

# friday bot
bot1 = UranusCore('notifer', '1195889656')
bot1.run_forever()
bot1.register_callback(msg_callback)
global_uranus_op = bot1.get_global_op()


# notifer bot
bot2 = UranusCore('friday', '1195889656')
bot2.run_forever()
bot2.register_callback(msg_callback_2)
bot2_op = bot2.get_global_op()









