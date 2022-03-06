#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from boto3.dynamodb.conditions import Key
from common.model import *
from common.aws import AwsConfig
from common.aws import aws_dynamodb_processor as adp


class DvBoardMst(BaseObj, DbObj):
    """
    ダッシュボードデータを保持します
    """
    board_id: str
    board_name: str
    active: bool
    file_name: str
    display_sort: int

    def __init__(self, board_id: str = "", board_name: str = "(未設定)", active: bool = False,
                 file_name: str = "", display_sort: int = 0):
        self.table_name = 'DvBoardMst'
        self.board_id = board_id
        self.board_name = board_name
        self.active = active
        self.file_name = file_name
        self.display_sort = display_sort

    def set_data(self, json: dict) -> None:
        self.table_name = 'DvBoardMst'
        self.board_id = json.get('board_id')
        self.board_name = json.get('board_name')
        self.active = json.get('active')
        self.file_name = json.get('file_name')
        self.display_sort = json.get('display_sort')

    def get_snake_dict(self) -> dict:
        return {
            'board_id': self.board_id,
            'board_name': self.board_name,
            'active': self.active,
            'file_name': self.file_name,
            'display_sort': self.display_sort
        }

    def get_item(self) -> dict:
        return {
            'boardId': self.board_id,
            'boardName': self.board_name,
            'active': self.active,
            'fileName': self.file_name,
            'displaySort': self.display_sort
        }


def get_dv_board_mst_list(aws: AwsConfig) -> list[Optional[DvBoardMst]]:
    dv_column_mst_list = []
    json_list = adp.scan_all_data(aws, 'DvBoardMst')
    for elem in json_list:
        dv_column_mst_list.append(make_db_obj(
            db_obj=DvBoardMst(),
            json=elem
        ))
    return dv_column_mst_list
