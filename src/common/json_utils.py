#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import json
from decimal import Decimal

from attrdict import AttrDict
from common.model.__init__ import BaseObj


def dict_sort(json_data: dict, sort_function, sort_key, is_reverse=False):
    """
    SortFunctionを定義して、キーを渡して利用してください
    実装は #aws_creation_date_sort# を確認してください
    """
    return sorted(json_data, key=lambda x: sort_function(x[sort_key]), reverse=is_reverse)


def get_dict(obj: object) -> dict:
    """
    json.dumpsを利用したときに、リストやオブジェクトがdict形式で返却されないと
    レスポンスパラメータにobjectのポインタが返されてしまうため
    """
    result = {}
    non_convert_obj = [
        int, str, float, bool
    ]
    if type(obj) in non_convert_obj:
        return obj
    _dict = obj if type(obj) == dict else obj.__dict__
    for key, value in _dict.items():
        if isinstance(value, list):
            child_result = []
            for elem in value:
                child_result.append(get_dict(elem))
            result.update({key: child_result})
        elif isinstance(value, dict):
            child_result = {}
            for k, v in value.items():
                child_result.update({k: get_dict(v)})
            result.update({key: child_result})
        elif isinstance(value, BaseObj):
            result.update({key: value.get_dict()})
        else:
            result.update({key: value})
    return result


def convert_obj(json_data: dict) -> object:
    result = AttrDict(json_data)
    return result


def get_dict_to_str(json_data: dict) -> str:
    """
    json_dataをstringに返却して返す
    """
    def default_proc(obj):
        """
        serializableではないobjectは別のオブジェクトに変換して返す。
        これによって下記のエラーを防ぐ
        Object of type Decimal is not JSON serializable
        """
        # decimal は floatにして返す
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError
    return json.dumps(json_data, default=default_proc, ensure_ascii=False)


def get_str_to_json(str_data: str) -> dict:
    return json.loads(str_data)
