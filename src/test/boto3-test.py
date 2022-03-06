#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import sys
import os

from common.aws import *

from common import file_processor as fp

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))


def execute(config: AwsConfig) -> None:
    ec2 = config.get_client('ec2')
    target = ec2.describe_instances()
    fp.console_out_json(target)


if __name__ == '__main__':
    exec_user_config = get_exec_user_config(config=aws_config)
    execute(exec_user_config)
