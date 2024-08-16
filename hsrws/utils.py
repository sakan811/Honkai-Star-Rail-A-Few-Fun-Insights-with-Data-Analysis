#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import functools
import sqlite3
import traceback
from typing import Callable

from loguru import logger


def get_version_dict() -> dict:
    return {
        1.1: ['luocha', 'silver-wolf', 'yukong'],
        1.2: ['blade', 'kafka', 'luka'],
        1.3: ['dan-heng-imbibitor-lunae', 'fu-xuan', 'lynx'],
        1.4: ['guinaifen', 'topaz-&-numby', 'jingliu'],
        1.5: ['argenti', 'hanya', 'huohuo'],
        1.6: ['dr-ratio', 'ruan-mei', 'xueyi'],
        2.0: ['black-swan', 'misha', 'sparkle'],
        2.1: ['acheron', 'aventurine', 'gallagher'],
        2.2: ['robin', 'boothill', 'trailblazer-the-harmony'],
        2.3: ['jade', 'firefly'],
        2.4: ['yunli', 'jiaoqiu', 'march-7th-the-hunt'],
        2.5: ['feixiao', 'lingsha']
    }


def handle_exception(func: Callable) -> Callable:
    """
    Decorate a function for exception handling.
    :param func: The function to be decorated.
    :return: The decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Call the original function
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error('Unexpected exception')
            raise Exception(e)

    return wrapper

