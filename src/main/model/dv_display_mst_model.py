#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from boto3.dynamodb.conditions import Key
from common.model import *
from common.aws import AwsConfig


class DvDisplayMst(BaseObj, DbObj):
    """
    テーブルのカラム情報を保持します
    """
    board_type_column_mix: str
    board_id: str
    board_type: str
    column_id: int
    column_name: str
    column_type: str
    column_mode: str

    def __init__(self, board_id: str = "", board_type="", column_id: int = -1,
                 column_name: str = "", column_type: str = None, column_mode=""):
        self.table_name = 'DvDisplayMst'
        self.board_type_column_mix = self.join_key_elem(board_id, board_type, column_id)
        self.board_id = board_id
        self.board_type = board_type
        self.column_id = column_id
        self.column_name = column_name
        self.column_type = column_type
        self.column_mode = column_mode

    def set_data(self, json: dict) -> None:
        self.table_name = 'DvDisplayMst'
        self.board_id = json.get('board_id')
        self.board_type = json.get('board_type')
        self.column_id = json.get('column_id')
        self.column_name = json.get('column_name')
        self.column_type = json.get('column_type')
        self.column_mode = json.get('column_mode')
        self.board_type_column_mix = self.join_key_elem(self.board_id, self.board_type, self.column_id)

    def get_item(self) -> dict:
        return {
            'boardTypeColumnMix': self.board_type_column_mix,
            'boardId': self.board_id,
            'boardType': self.board_type,
            'columnId': self.column_id,
            'columnName': self.column_name,
            'columnType': self.column_type,
            'columnMode': self.column_mode
        }

    def get_snake_dict(self) -> dict:
        return {
            'board_type_column_mix': self.board_type_column_mix,
            'board_id': self.board_id,
            'board_type': self.board_type,
            'column_id': self.column_id,
            'column_name': self.column_name,
            'column_type': self.column_type,
            'column_mode': self.column_mode
        }

def query_dv_display_mst_list(aws: AwsConfig, board_id: str, board_type: str = None) -> list[DvDisplayMst]:
    """
    DvColumnMst
    board_idでフィルタリング
    """
    dynamodb = aws.get_resource('dynamodb')
    table = dynamodb.Table('DvDisplayMst')
    if board_type is None:
        res = table.query(
            IndexName="GSI",
            KeyConditionExpression=Key('board_id').eq(board_id)
        )
    else:
        res = table.query(
            IndexName="GSI",
            KeyConditionExpression=Key('board_id').eq(board_id) & Key('board_type').eq(board_type)
        )
    dv_display_mst_list = []
    for elem in res.get('Items'):
        dv_display_mst_list.append(make_db_obj(
            db_obj=DvDisplayMst(),
            json=elem
        ))
    return dv_display_mst_list
