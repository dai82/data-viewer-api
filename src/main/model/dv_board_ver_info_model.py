#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from boto3.dynamodb.conditions import Key
from common.model import *
from common.aws import AwsConfig


class DvBoardVerInfo(BaseObj, DbObj):
    """
    ダッシュボードデータとして取り込んだ元データのversionを制御します
    """
    board_id: str
    version: int
    active: bool
    upload_date: str

    def __init__(self, board_id="", version=-1, active=False, upload_date=""):
        self.table_name = 'DvBoardVerInfo'
        self.board_id = board_id
        self.version = version
        self.active = active
        self.upload_date = upload_date

    def set_data(self, json: dict) -> None:
        self.table_name = 'DvBoardVerInfo'
        self.board_id = json.get('board_id')
        self.version = json.get('version')
        self.active = json.get('active')
        self.upload_date = json.get('upload_date')

    def get_item(self) -> dict:
        return {
            'boardId': self.board_id,
            'version': self.version,
            'active': self.active,
            'uploadDate': self.upload_date
        }

    def get_snake_dict(self) -> dict:
        return {
            'board_id': self.board_id,
            'version': self.version,
            'active': self.active,
            'upload_date': self.upload_date
        }


def query_dv_board_ver_info_list(aws: AwsConfig, board_id: str, board_type: str = None) -> list[DvBoardVerInfo]:
    """
    DvBoardVerInfo
    board_idでフィルタリング
    """
    dynamodb = aws.get_resource('dynamodb')
    table = dynamodb.Table('DvBoardVerInfo')
    res = table.query(
        KeyConditionExpression=Key('board_id').eq(board_id)
    )
    dv_board_ver_info_list = []
    for elem in res.get('Items'):
        if board_type == elem.get("board_type") and board_type is not None:
            continue
        dv_board_ver_info_list.append(make_db_obj(
            db_obj=DvBoardVerInfo(),
            json=elem
        ))
    return dv_board_ver_info_list


def query_latest_board_ver_info(aws: AwsConfig, board_id: str) -> Optional[DvBoardVerInfo]:
    """
    DvBoardVerInfo
    board_idでフィルタリングし、最新のversionのもののみ取得
    """
    dynamodb = aws.get_resource('dynamodb')
    table = dynamodb.Table('DvBoardVerInfo')
    res = table.query(
        KeyConditionExpression=Key('board_id').eq(board_id)
    )
    dv_board_ver_info = None
    for elem in res.get('Items'):
        target = make_db_obj(
            db_obj=DvBoardVerInfo(),
            json=elem
        )
        if dv_board_ver_info is None or target.version > dv_board_ver_info.version:
            dv_board_ver_info = target
    return dv_board_ver_info

