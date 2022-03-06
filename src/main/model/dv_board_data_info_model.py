#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from boto3.dynamodb.conditions import Key
from common.model import *
from common.aws import AwsConfig


class DvBoardDataInfo(BaseObj, DbObj):
    """
    ダッシュボードデータのbodyを制御します \n
    file_key: board_id, version \n
    key: board_id, version, row_id, col_id \n
    """
    board_version_column_row_mix: str
    board_id: str
    version: int
    col_id: int
    col_nm: str
    row_id: int
    content: str
    create_date: str
    prc_date: str

    def __init__(self, board_id="", version=None, col_id=-1, col_nm="", row_id=-1, content=None,
                 create_date="", prc_date=""):
        self.table_name = 'DvBoardDataInfo'
        self.board_version_column_row_mix = self.join_key_elem(board_id, version, col_id, row_id)
        self.board_id = board_id
        self.version = version
        self.col_id = col_id
        self.col_nm = col_nm
        self.row_id = row_id
        self.content = content
        self.create_date = create_date
        self.prc_date = prc_date

    def set_data(self, json: dict) -> None:
        self.table_name = 'DvBoardDataInfo'
        self.board_id = json.get('board_id')
        self.version = json.get('version')
        self.col_id = json.get('col_id')
        self.col_nm = json.get('col_nm')
        self.row_id = json.get('row_id')
        self.board_version_column_row_mix = self.join_key_elem(self.board_id, self.version, self.col_id, self.row_id)
        self.content = json.get('content')
        self.create_date = json.get('create_date')
        self.prc_date = json.get('prc_date')

    def get_item(self) -> dict:
        return {
            'boardVersionColumnRowMix': self.board_version_column_row_mix,
            'boardId': self.board_id,
            'version': self.version,
            'colId': self.col_id,
            'colNm': self.col_nm,
            'rowId': self.row_id,
            'content': self.content,
            'createDate': self.create_date,
            'prcDate': self.prc_date
        }

    def get_snake_dict(self) -> dict:
        return {
            'board_version_column_row_mix': self.board_version_column_row_mix,
            'board_id': self.board_id,
            'version': self.version,
            'col_id': self.col_id,
            'col_nm': self.col_nm,
            'row_id': self.row_id,
            'content': self.content,
            'create_date': self.create_date,
            'prc_date': self.prc_date
        }


def query_dv_board_data_info_list(aws: AwsConfig, board_id) -> list[DvBoardDataInfo]:
    """
    DvBoardVerInfo
    board_idでフィルタリング
    """
    dynamodb = aws.get_resource('dynamodb')
    table = dynamodb.Table('DvBoardDataInfo')
    res = table.query(
        IndexName="GSI",
        KeyConditionExpression=Key('board_id').eq(board_id)
    )
    dv_board_ver_info_list = []
    for elem in res.get('Items'):
        dv_board_ver_info_list.append(make_db_obj(
            db_obj=DvBoardDataInfo(),
            json=elem
        ))
    return dv_board_ver_info_list
