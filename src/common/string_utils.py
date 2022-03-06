#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import uuid


def get_uuid(length: int = 32) -> str:
    """
    引数で指定した桁数分の一意な文字列を取得します
    :param length:
    :return:
    """
    if length < 32:
        return uuid.uuid4()[0:length]
    return str(uuid.uuid4())
