# -*- coding: utf-8 -*-
# file: session_holder.py
# author: JinTian
# time: 16/05/2017 6:00 PM
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
"""
this class is the global session holder,

session_holder.hold(session_label='ask_for_purpose', class_name='ImageReasoner', func_name='reasoning_image',
params_dict={
'params_1': params_1})

"""
import os
import pickle


def hold(talk_to_uid, session_label, func_path, params_dict, multi_session_hold=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    holder_file = os.path.join(base_dir, 'global_session_holder.pkl')
    class_name = func_path.split('.')[0]
    func_name = func_path.split('.')[1]
    dump_obj = {
        'session_label': session_label,
        'class_name': class_name,
        'func_name': func_name,
        'params_dict': params_dict,
        'multi_session_hold': multi_session_hold
    }

    if os.path.exists(holder_file):
        with open(holder_file, 'rb') as f:
            all_holder = pickle.load(f)
        all_holder[talk_to_uid] = dump_obj
        with open(holder_file, 'wb') as f:
            pickle.dump(all_holder, f)
    else:
        all_holder = dict()
        all_holder[talk_to_uid] = dump_obj
        with open(holder_file, 'wb') as f:
            pickle.dump(all_holder, f)
    print('-----> session hold success. belong to {}, session label {}'.format(talk_to_uid, session_label))


def resign_holder(talk_to):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    holder_file = os.path.join(base_dir, 'global_session_holder.pkl')
    if os.path.exists(holder_file):
        with open(holder_file, 'rb') as f:
            all_holder = pickle.load(f)
        all_holder = {k: v for k, v in all_holder.items() if k != talk_to}
        with open(holder_file, 'wb') as f:
            pickle.dump(all_holder, f)
    else:
        pass



