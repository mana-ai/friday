# -*- coding: utf-8 -*-
# file: command_reasoner.py
# author: JinTian
# time: 17/05/2017 8:21 PM
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
OK, this is the new command reasoner.

this reasoner will match all registered command regex and find the matched index of regex list

basically, this reasoner will try best let every command have only one match, but if more than one
match got, this reasoner will trigger a make sure question and apply a holder.
"""
import re
from .rules import all_rules


from .do_answer_me import *
from .do_days import *
from .do_search_pic import *
from .do_subscrib import *
from .do_tapaware import *
from .do_subscrib import *
from .do_weather import *


class RulesRouter(object):
    def __init__(self):
        pass

    @staticmethod
    def get_match_executor(from_talk):
        executors, values = zip(*all_rules.items())
        executors = list(executors)
        patterns = [i['regex'] for i in list(values)]

        matched_indices = []
        for i, pattern in enumerate(patterns):
            one_matched = 0
            for p in pattern:
                r = re.findall(p, from_talk)
                if len(r) >= 1:
                    one_matched += 1
            if one_matched > 0:
                matched_indices.append(i)
        matched_executors = [executors[i] for i in matched_indices]
        print('[rules router] matched registered executors: ', matched_executors)
        return matched_executors

    @staticmethod
    def execute_command(executor, from_talk, talk_to, msg_executor):
        class_name = executor.split('.')[0]
        func_name = executor.split('.')[1]
        c_obj = globals()[class_name]()
        func = getattr(c_obj, func_name)
        response = func(from_talk=from_talk, talk_to=talk_to, msg_executor=msg_executor)
        return response

    def reasoning_command(self, from_talk=None, talk_to=None, msg_executor=None, session_hold_bundle=None):
        matched_executors = self.get_match_executor(from_talk)
        if len(matched_executors) > 1:
            print('[ambiguous rules] got ambiguous rules, should ask for which one.')
            print('                  choosing the first one: ', matched_executors[0])
            # alias = [registered_commands_regex[i]['alias'] for i in matched_executors]
            # return ' '.join(alias) + str(len(alias)) + '件事情中你想我做哪一个'
            executor = matched_executors[0]
            response = self.execute_command(executor, from_talk, talk_to, msg_executor)
            return response
        elif len(matched_executors) == 1:
            print('[target rule] got rule: ', matched_executors[0])
            executor = matched_executors[0]
            response = self.execute_command(executor, from_talk, talk_to, msg_executor)
            return response
        else:
            return None

