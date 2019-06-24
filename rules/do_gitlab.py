'''
do github add for me robot
'''
import gitlab
from .do import Ability



class GitlabAdder(Ability):

    def __init__(self):
        self.login_gitlab()
        self.gl = None

    def login_gitlab(self):
        self.gl = gitlab.Gitlab('https://gitlab.com', private_token='CnpangCjnoZXTHoRXyk2')
        self.gl.auth()
        print('auth done.')

    def check_username_exist(self, username):
        users = self.gl.users.list(search=username)
        if len(users) >= 1:
            return True, users[0]
        else:
            return False, None

    def add_new_member_to_vip_mana(self, username, is_mana=True):
        self.login_gitlab()
        res, user = self.check_username_exist(username)
        rp = ''
        if res:
            strangeaaiwizard = self.gl.groups.get(3596325)
            manavips = self.gl.groups.get(5055105)

            # check user exist or not
            try:
                member = strangeaaiwizard.members.create({'user_id': user.id,
                                    'access_level': gitlab.DEVELOPER_ACCESS})
                member.save()
                rp = '添加StrangeAI成功: {}\n'.format(username)
            except gitlab.exceptions.GitlabCreateError as e:
                rp = '添加StrangeAI失败，错误代码：{}\n'.format(e)

            if is_mana:
                try:
                    member = manavips.members.create({'user_id': user.id,
                                        'access_level': gitlab.DEVELOPER_ACCESS})
                    member.save()
                    rp += '添加MANA成功: {}\n'.format(username)
                except gitlab.exceptions.GitlabCreateError as e:
                    rp += '添加MANA失败，错误代码：{}'.format(e)
            return rp
        else:
            return '添加失败，该用户名不存在: {} not found.'.format(username)
    
    def act(self, from_talk=None, talk_to=None, msg_executor=None, session_hold_bundle=None):
        session_label = None
        params_dict = None
        if session_hold_bundle is not None:
            session_label = session_hold_bundle['session_label']
            params_dict = session_hold_bundle['params_dict']

        talk_to_uid = talk_to
        if isinstance(talk_to, dict):
            talk_to_uid = talk_to['user_addr']
            talk_to = talk_to['user_nick_name']
        # 添加mana会员 jintian
        # 添加strangeai会员 jintian
        username = from_talk.split(' ')[-1]
        if talk_to_uid == 'usrZK8kZTzEHC':
            is_mana = True
            if 'mana' not in from_talk:
                is_mana = False
            rp = self.add_new_member_to_vip_mana(username, is_mana=is_mana)
            return rp
        else:
            return '糟糕，被你发现了隐藏的功能，可这是一个高度机密操作，您的权限还不够'