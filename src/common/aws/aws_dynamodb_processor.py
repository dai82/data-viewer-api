#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# 【How To Use】
# DynamoDbの単純なオブジェクトへのgettter setter用
# queryはこっちに書かないで、各サブ側に書く
# (docs)
# boto3 dynamodb
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html

import logging

from botocore.exceptions import ClientError

from common.model import *
from common.aws import AwsConfig

LOGGER = logging.getLogger()


def get_data(aws: AwsConfig, db_obj: DbObj, key_dict: dict) -> DbObj:
    """
    dynamodbからkeyを指定してオブジェクトを取得する
    key_dict ex) {'board_id': uuid}
    """
    try:
        dynamodb = aws.get_resource('dynamodb')
        table = dynamodb.Table(db_obj.table_name)
        res = table.get_item(Key=key_dict)
        if res.get('Item') is None:
            return None
        else:
            return make_db_obj(db_obj, res.get('Item'))
    except Exception as error:
        LOGGER.error(error)
        raise error


def delete_data(aws: AwsConfig, db_obj: DbObj, key_name, sort_key: str = None,
                index_name: str = None) -> bool:
    """
    dynamodbからkeyを指定してオブジェクトを削除する
    key_dict ex) {'board_id': uuid}
    """
    try:
        dynamodb = aws.get_resource('dynamodb')
        table = dynamodb.Table(db_obj.table_name)
        if index_name is None:
            if sort_key is None:
                res = table.delete_item(Key={
                    key_name: db_obj.__dict__.get(key_name)
                })
            else:
                res = table.delete_item(Key={
                    key_name: db_obj.__dict__.get(key_name),
                    sort_key: db_obj.__dict__.get(sort_key)
                })
        else:
            if sort_key is None:
                res = table.delete_item(
                    IndexName=index_name,
                    Key={key_name: db_obj.__dict__.get(key_name)}
                )
            else:
                res = table.delete_item(
                    IndexName=index_name,
                    Key={
                        key_name: db_obj.__dict__.get(key_name),
                        sort_key: db_obj.__dict__.get(sort_key)
                    }
                )
        if res.get('Item') is None:
            return False
        else:
            return True
    except Exception as error:
        LOGGER.error(error)
        raise error


def set_data(aws: AwsConfig, data_obj: DbObj):
    """
    Objectをdynamodbにセットする
    """
    try:
        dynamodb = aws.get_resource('dynamodb')
        res = dynamodb.Table(data_obj.table_name).put_item(
            Item=data_obj.get_snake_dict()
        )
    except Exception as error:
        LOGGER.error(error)
        raise error


def scan_all_data(aws: AwsConfig, table_name: str) -> list[dict]:
    """
    Tableのすべてのデータを取得する
    """
    try:
        dynamodb = aws.get_resource('dynamodb')
        res = dynamodb.Table(table_name).scan()
        return res.get('Items')
    except Exception as error:
        LOGGER.error(error)
        raise error


def set_all_data(aws: AwsConfig, data_obj_list: list[DbObj]):
    """
    https://dev.classmethod.jp/articles/lambda-python-dynamodb/#toc-1
    複数のObjectをdynamodbにセットする
    """
    if data_obj_list.__len__() == 0:
        return None
    try:
        dynamodb = aws.get_resource('dynamodb')
        table = dynamodb.Table(data_obj_list[0].table_name)
        with table.batch_writer() as batch:
            for item in data_obj_list:
                batch.put_item(
                    Item=item.get_snake_dict()
                )
        return 'finish'
    except ClientError as e:
        LOGGER.error(e)
        raise e


def delete_all_data(aws: AwsConfig, data_obj_list: list[DbObj], key_name,
                    sort_key: str = None, index_name: str = None):
    """
    複数のObjectを一括削除する
    """
    if data_obj_list.__len__() == 0:
        return None
    try:
        dynamodb = aws.get_resource('dynamodb')
        table = dynamodb.Table(data_obj_list[0].table_name)
        with table.batch_writer() as batch:
            for item in data_obj_list:
                if index_name is None:
                    if sort_key is None:
                        batch.delete_item(Key={
                            key_name: item.__dict__.get(key_name)
                        })
                    else:
                        batch.delete_item(Key={
                            key_name: item.__dict__.get(key_name),
                            sort_key: item.__dict__.get(sort_key)
                        })
                else:
                    if sort_key is None:
                        batch.delete_item(
                            IndexName=index_name,
                            Key={key_name: item.__dict__.get(key_name)}
                        )
                    else:
                        batch.delete_item(
                            IndexName=index_name,
                            Key={
                                key_name: item.__dict__.get(key_name),
                                sort_key: item.__dict__.get(sort_key)
                            }
                        )
        return 'finish'
    except ClientError as e:
        LOGGER.error(e)
        raise e


def get_count(aws: AwsConfig, table_name: str) -> int:
    """
    dynamodbのTableの件数を取得するにセットする
    """
    try:
        dynamodb = aws.get_resource('dynamodb')
        count = dynamodb.Table(table_name).item_count
        return count
    except ClientError as e:
        LOGGER.error(e)
        raise e
