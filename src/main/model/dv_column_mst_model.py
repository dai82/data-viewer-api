#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from boto3.dynamodb.conditions import Key
from common.model import *
from common.aws import AwsConfig


class DvColumnMst(BaseObj, DbObj):
    """
    テーブルのカラム情報を保持します
    """
    board_id: str
    column_id: int
    column_name: str
    column_type: str

    def __init__(self, board_id: str = "", column_id: int = -1 , column_name: str = "",
                 column_type: str = None):
        self.table_name = 'DvColumnMst'
        self.board_id = board_id
        self.column_id = column_id
        self.column_name = column_name
        self.column_type = column_type

    def set_data(self, json: dict) -> None:
        self.table_name = 'DvColumnMst'
        self.board_id = json.get('board_id')
        self.column_id = json.get('column_id')
        self.column_name = json.get('column_name')
        self.column_type = json.get('column_type')

    def get_item(self) -> dict:
        return {
            'boardId': self.board_id,
            'columnId': self.column_id,
            'columnName': self.column_name,
            'columnType': self.column_type
        }

    def get_snake_dict(self) -> dict:
        return {
            'board_id': self.board_id,
            'column_id': self.column_id,
            'column_name': self.column_name,
            'column_type': self.column_type
        }


def query_dv_column_mst_list(aws: AwsConfig, board_id: str) -> list[DvColumnMst]:
    """
    DvColumnMst
    board_idでフィルタリング
    """
    dynamodb = aws.get_resource('dynamodb')
    table = dynamodb.Table('DvColumnMst')
    res = table.query(
        KeyConditionExpression=Key('board_id').eq(board_id)
    )
    dv_column_mst_list = []
    for elem in res.get('Items'):
        dv_column_mst_list.append(make_db_obj(
            db_obj=DvColumnMst(),
            json=elem
        ))
    return dv_column_mst_list

