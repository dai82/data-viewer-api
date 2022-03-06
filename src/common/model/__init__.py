#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import os
from typing import Optional

from common import json_utils as ju
from common import file_utils as fu
from common import file_processor as fp
from abc import ABCMeta, abstractmethod


class BaseObj(metaclass=ABCMeta):

    def get_data(self) -> dict:
        """
        オブジェクトをjson形式に変換して返却する
        機械的にjsonに返却するので敬称元側での実装は不要
        (java で言うところのgetterにあたる)
        """
        return ju.get_dict(self)

    @abstractmethod
    def set_data(self, json: dict) -> None:
        """
        jsonで取得した変数をオブジェクトに変換して登録する
        (java で言うところのsetterにあたる)
        """
        pass

    # https://note.nkmk.me/python-args-kwargs-usage/
    @staticmethod
    def join_key_elem(*args) -> str:
        result = ''
        for key in args:
            result += '[{key}]'.format(key=str(key))
        return result


class DbObj(metaclass=ABCMeta):
    """
    dynamodbへの値の受け渡しに利用するオブジェクトの基底クラス
    dynamodbのCRUDを行うオブジェクトはすべてこれを利用する
    """
    table_name: str

    @abstractmethod
    def get_item(self) -> dict:
        """
        forntEndのフィールド変数がキャメルケースなので、camelCaseで記載する
        dynamoにセットするときはsnake_caseなので、get_snake_caseとの使い分けが必要
        """
        pass

    @abstractmethod
    def get_snake_dict(self) -> dict:
        """
        dynamodb.Table('TableName').put_item(${target})の
        ${target}に渡せるようにする
        getData()との違いはsnake_caseで記載することで、カラム方と合わせる
        """
        return ju.get_dict(self)

def make_db_obj(db_obj: DbObj, json: dict) -> Optional[DbObj]:
    """
    DbObjのインスタンスを作成して返却する
    (staticmethodで返すとfunctionとなり、Objectにできないため、@staticmethodは付けない)
    """
    if json.__len__() == 0:
        return None
    db_obj.set_data(json)
    return db_obj


class FileInfo(BaseObj):
    file_type: str
    file_path: str
    file_directory: str
    file_name: str

    def __init__(self, file_type, file_path):
        """
        :param file_type: json or csv
        :param file_path:
        """
        self.file_type = file_type
        self.file_path = file_path
        self.file_directory = os.path.dirname(file_path)
        self.file_name = os.path.basename(file_path)

    def get_data(self) -> None:
        # 使わない
        pass

    def set_data(self, json: dict) -> None:
        # 使わない
        pass


class Config(BaseObj):
    name: str
    config_file_path: str
    config_name: str
    root_directory: str
    log_dir: str

    def __init__(self, name, root_directory, config_name):
        self.name = name
        self.root_directory = root_directory
        self.config_name = config_name
        self.config_file_path = root_directory + os.sep + config_name

    def make_config(self, contents: dict = {}):
        """
        configをjson形式で出力します \r\n
        :param contents: dict
        :return: None
        """
        if contents.__len__() == 0:
            contents = ju.get_dict(self)
        if fu.file_exists(self.config_file_path):
            return
        fp.write_json(self.config_file_path, contents)

    def set_data(self, json: dict) -> None:
        # 使わない
        pass

    def set_json(self, json: dict) -> None:
        # 使わない
        pass


class ResponseData(BaseObj):
    """
    :param code レスポンスステータスの数値 (ex.404,200):
    :param status レスポンスステータス:
    :param message エラーがあった時のメッセージ:
    :param result 返信データ:
    """
    code: int
    status: str
    message: str
    result: dict

    def __init__(self, code, status="ERROR", message="[not message]", result={}):
        self.code = code
        self.status = status
        self.message = message
        self.result = result

    def set_data(self, json: dict) -> None:
        # 使わない
        pass

    def set_json(self, json: dict) -> None:
        # 使わない
        pass

    def get_response(self) -> dict:
        """
        axiosの返信時にはこのメソッドを呼び出す
        Ex. return make_response(jsonify(res.get_response()), res.get_code())
        """
        # シリアライズできないものをいったんconvertするため、子のような面倒な方法を用いている
        tmp = ju.get_dict_to_str(self.result)
        result = ju.get_str_to_json(tmp)
        return {
            "code" : str(self.code),
            "status": self.status,
            "message": self.message,
            "result": result
        }
