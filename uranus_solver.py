from uranuspy.core import UranusCore

from infer_engine.infer import InferEngine
from rules.rules_router import RulesRouter
from global_session_holder import resume_session
from config.config import global_config
from utils.regex_verify import is_image_url

MSG_SPLITTER = global_config.msg_splitter
infer_engine = InferEngine(bot_config=global_config.config)
global_uranus_op = None


def send_splitter_msg(msg, talk_to):
    rp_list = msg.split(MSG_SPLITTER)
    for rp in rp_list:
        # print(' one of list: ', rp)
        if is_image_url(rp):
            # print('is image: ', rp)
            global_uranus_op.send_img_msg(talk_to, rp)
        else:
            global_uranus_op.send_txt_msg(talk_to, rp)


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
    from_talk = data['content']
    sender_name = data['sender_name']
    talk_to = data['sender']
    print('-- [incoming] {}:  {}'.format(sender_name, from_talk))
    print('start inference..')
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
        print('-- global_uranus_op: ', global_uranus_op)
        rp = rules_router.reasoning_command(from_talk, talk_to_dict, global_uranus_op)
        if rp is not None:
            send_splitter_msg(rp, talk_to)
        else:
            rp = infer_engine.infer(from_talk)
            if MSG_SPLITTER in rp:
                send_splitter_msg(rp, talk_to)
            print('inference result: {}\n\n'.format(rp))
        return rp


uranus = UranusCore('friday', '1195889656')
uranus.run_forever()
uranus.register_callback(msg_callback)
global_uranus_op = uranus.get_global_op()









