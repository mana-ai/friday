# -*- coding: utf-8 -*-
# file: create_todo.py
# author: JinTian
# time: 01/05/2017 3:09 PM
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


def create_todo(class_name, func, args, time_):
    """
    this method will create a todo event
    and save it into local, to call this method
    func name, and args and time must send
    [NOTE] time must be a datetime.datetime object
    :return:
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    todo_local_file = os.path.join(base_dir, 'todo.pkl')

    dump_obj = {
        'class': class_name,
        'func': func,
        'args': args,
        'time': time_,
    }
    if not os.path.exists(todo_local_file):
        obj_list = list()
        obj_list.append(dump_obj)
        with open(todo_local_file, 'wb') as f:
            pickle.dump(obj_list, f)
    else:
        with open(todo_local_file, 'rb') as f:
            obj_list = pickle.load(f)
            obj_list.append(dump_obj)

        with open(todo_local_file, 'wb') as f:
            pickle.dump(obj_list, f)