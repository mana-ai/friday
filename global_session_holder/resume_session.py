# -*- coding: utf-8 -*-
# file: resume_session.py
# author: JinTian
# time: 16/05/2017 8:45 PM
# Copyright 2017 JinTian. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
import os
import pickle
from rules import *


def resume_session(from_talk, talk_to):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    holder_file = os.path.join(base_dir, 'global_session_holder.pkl')
    with open(holder_file, 'rb') as f:
        all_holder = pickle.load(f)

    talk_to_holder = all_holder[talk_to]
    print('-- talk to {} holder content: {}'.format(talk_to, talk_to_holder))
    session_label = talk_to_holder['session_label']
    class_name = talk_to_holder['class_name']
    func_name = talk_to_holder['func_name']
    params_dict = talk_to_holder['params_dict']
    multi_session_hold = talk_to_holder['multi_session_hold']

    session_hold_bundle = {'session_label': session_label,
                           'params_dict': params_dict}
    c_obj = globals()[class_name]()
    func = getattr(c_obj, func_name)
    response = func(from_talk=from_talk, talk_to=talk_to, session_hold_bundle=session_hold_bundle)
    print('-- session resumed and executed, got response: {}'.format(response))

    # after resume must delete current holder file
    # if force_hold set to be True will not delete, this is use for multi hold session
    if not multi_session_hold:
        all_holder = {k: v for k, v in all_holder.items() if k != talk_to}
        with open(holder_file, 'wb') as f:
            pickle.dump(all_holder, f)
    return response


def should_resume(talk_to):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    holder_file = os.path.join(base_dir, 'global_session_holder.pkl')
    if not os.path.exists(holder_file):
        return False
    else:
        with open(holder_file, 'rb') as f:
            all_holder = pickle.load(f)
        if talk_to in list(all_holder.keys()):
            print('-- should resume.')
            return True
        else:
            print('-- not resume')
            return False

