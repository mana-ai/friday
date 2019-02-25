# -*- coding: utf-8 -*-
# file: main.py
# author: JinTian
# time: 23/02/2018 6:51 PM
# Copyright 2018 JinTian. All Rights Reserved.
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
main entrance of the pigeon
once run, pigeon will serve all the messages
"""
import time

from cruisers.cruiser_uranus_greet import UranusGreetCruiser
from cruisers.cruiser_uranus_news import NewsCruiser
from cruisers.cruiser_todo import ToDoCruiser
from cruisers.cruiser_uranus_host import HostMachineCruiser
from threading import Thread
from uranuspy.core import UranusCore
from uranus_solver import *


def start_cruise_threads(op):
    uranus_greet_cruiser = UranusGreetCruiser(msg_executor=op)
    uranus_greet_thread = Thread(name='uranus_greet_thread', target=uranus_greet_cruiser.cruise_daily_work)
    uranus_greet_thread.setDaemon(True)
    uranus_greet_thread.start()

    uranus_news_cruiser = NewsCruiser(msg_executor=op)
    uranus_news_thread = Thread(name='uranus_news_thread', target=uranus_news_cruiser.cruise_daily_work)
    uranus_news_thread.setDaemon(True)
    uranus_news_thread.start()

    todo_cruiser = ToDoCruiser(msg_executor=op)
    todo_cruiser_thread = Thread(name='todo_cruiser_thread', target=todo_cruiser.cruise_todo)
    todo_cruiser_thread.setDaemon(True)
    todo_cruiser_thread.start()

    hm_cruiser = HostMachineCruiser(msg_executor=op)
    hm_cruiser_thread = Thread(name='hm_cruiser_thread', target=hm_cruiser.cruise_daily_work)
    hm_cruiser_thread.setDaemon(True)
    hm_cruiser_thread.start()

    # uranus_test_cruiser = UranusTestCruiser()
    # uranus_test_thread = Thread(name='uranus_test_thread', target=uranus_test_cruiser.cruise_daily_work)
    # uranus_test_thread.setDaemon(True)
    # uranus_test_thread.start()


def main_loop():
    try:
        start_cruise_threads(global_uranus_op)
    except Exception as e:
        if e is not KeyboardInterrupt:
            print('!! Got exception: {}'.format(e))
            time.sleep(1)
        else:
            exit(0)


if __name__ == '__main__':
    main_loop()
