#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import sys
import os
import boto3

from common import file_processor as fp

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))

# property fileのディレクトリを読み込みます
prop_path = os.path.dirname(os.getcwd()) + os.sep + 'property'
aws_config = fp.read_json(prop_path + os.sep + "aws.json")


class AwsConfig:
    """
    awsのresource,clientにアクセスするための情報をここに格納します
    """
    access_key: str
    secret_key: str
    output: str
    region: str
    log_level: int

    def __init__(self, access_key, secret_key, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.output = 'json'

    def get_client(self, service: str) -> dict:
        return boto3.client(
            service_name=service,
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    def get_resource(self, service: str) -> dict:
        return boto3.resource(
            service_name=service,
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )


def get_exec_user_config(config: dict = aws_config) -> AwsConfig:
    def _get_ssm_target_value(_res: dict, _key: str) -> str or None:
        _target = list(filter(lambda x: x.get("Name") == _key, _res))
        if _target.__len__() > 0 and _target[0].get("Value") is not None:
            return _target[0].get("Value")
        return None

    ssm = boto3.client(
        service_name="ssm",
        region_name=config["Region"],
        aws_access_key_id=config["AccessKey"],
        aws_secret_access_key=config["SecretKey"]
    )
    access_key_path = '{path}access-key'.format(path=config['ExecKeyPath'])
    secret_key_path = '{path}secret-key'.format(path=config['ExecKeyPath'])
    res = ssm.get_parameters(
        Names=[
            access_key_path,
            secret_key_path,
        ],
        WithDecryption=True
    ).get("Parameters")
    access_key = _get_ssm_target_value(res, access_key_path)
    secret_key = _get_ssm_target_value(res, secret_key_path)
    return AwsConfig(access_key, secret_key, config["Region"])
