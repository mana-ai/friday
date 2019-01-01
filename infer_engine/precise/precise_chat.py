# -*- coding: utf-8 -*-
# file: test.py
# author: JinTian
# time: 18/04/2017 7:37 PM
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
from chatterbot.chatterbot import ChatBot
from chatterbot.storage import MongoDatabaseAdapter
from chatterbot.trainers import ListTrainer
from pymongo import MongoClient
import os
from .dynamic_statements import dynamic_list_train, dynamic_list_train_cn


class PreciseChatter(object):
    """
    this class using ChatterBot to precise response on chat,
    this will train on statements corpus

    Huge Plan!!!!
    in precise chatter, I got an very interesting idea that Jarvis will
    write down every ask question from users, and at night, Jarvis will using Chatter Mind
    chat with Turing to improve himself!!
    """

    def __init__(self, lan='cn'):
        self.lan = lan
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self._init_chatter()
        self._set_trainer()
        print('precise chatter init')

    def _init_chatter(self):
        self.chatter = ChatBot(
            'Victoria',
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            # logic_adapters=[
            #     "chatterbot.logic.MathematicalEvaluation",
            #     "chatterbot.logic.TimeLogicAdapter"
            # ],
            database='victoria',
        )

    def _load_train_corpus(self):
        train_corpus_path = os.path.join(self.base_dir, 'statements')
        train_list = []
        if os.path.exists(train_corpus_path):
            with open(train_corpus_path, 'r') as f:
                for l in f.readlines():
                    train_list.append(l.strip())
        if self.lan == 'cn':
            for i in dynamic_list_train_cn:
                train_list.append(i)
        else: 
            for i in dynamic_list_train_cn:
                train_list.append(i)
        return train_list

    def _set_trainer(self):
        if self.lan == 'cn':
            self.chatter.train(
                "chatterbot.corpus.chinese",
            )
        else:
            self.chatter.train(
                "chatterbot.corpus.english",
            )
        self.chatter.set_trainer(ListTrainer)
        self.chatter.train(self._load_train_corpus())

    def _collect_talk(self, q, a):
        """
        this method will automatically collect PreciseChatter talk,
        and save into local, so that this will be an good corpus to train Jarvis
        :return: 
        """
        collected_file = os.path.join(self.base_dir, 'collected_talk')

        with open(collected_file, 'a+') as f:
            f.writelines(q + '&&&&&' + a + '\n')

    def get_response(self, from_talk):
        response = self.chatter.get_response(from_talk)
        response = str(response)
        self._collect_talk(from_talk, response)
        # print('response from precise chat: ', response)
        return response

    def rival_turing(self):
        """
        this method will only work under LEARNING mode.

        in this method, Jarvis will using all collected questions chat with Turing, and collect
        the result in another talk file named Jarvis_vs_Turing.
        :return:
        """
        pass


precise_chatter = PreciseChatter()



