#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from datetime import datetime
from common import json_utils as ju


def today(time=False, formatter=None):
    if formatter is not None:
        return datetime.today().strftime(formatter)
    if time:
        return datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
    return datetime.today().strftime("%Y-%m-%d")


def dict_time_sort(json, field, is_reverse=False):
    def _datetime_from_aws_creation_date(str_date):
        return datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.000Z")
    return ju.dict_sort(json, _datetime_from_aws_creation_date, field, is_reverse)
