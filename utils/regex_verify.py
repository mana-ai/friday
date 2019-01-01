# -*- coding: utf-8 -*-
# file: regex_verify.py
# author: JinTian
# time: 01/03/2018 3:14 PM
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
method to verify some string to be a certain pattern
"""
import re
import validators


def is_url(txt):
    return validators.url(txt)


def is_image_url(txt):
    if validators.url(txt):
        if txt.endswith('.jpg') or txt.endswith('.png') or txt.endswith('.jpeg'):
            return True
        else:
            return False
    else:
        return False


