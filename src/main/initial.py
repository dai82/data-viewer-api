#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import sys
import logging

from common import file_utils as fu
from common.model import *

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
LOGGER = logging.getLogger()


class DataViewerConfig(Config):
    mst_dir: str
    data_dir: str
    backup_file_dir: str
    log_level: int


def init_execute(root_directory: str, force=False) -> DataViewerConfig:
    # 必要なファイルが存在しない場合は作成する
    if not fu.file_exists(root_directory) or force:
        # setting.json作成(すでにconfigファイルが作成されていたら何もしない)
        config = DataViewerConfig('Data Viewer', os.path.dirname(os.getcwd()), 'setting.json')
        config.backup_file_dir = config.root_directory + '{sep}work{sep}backup{sep}file'.format(sep=os.sep)
        config.log_level = logging.ERROR
        config.make_config()
        # backup作成
        fu.move_directory(
            bfr_path="{root}{sep}work".format(root=config.root_directory, sep=os.sep),
            aft_path="{root}{sep}backup".format(root=config.root_directory, sep=os.sep),
            exist_error=False, recreate=True
        )
        # 【work directory 作成】
        fu.create_file("file", "{root}{sep}work{sep}backup{sep}file{sep}dummy.txt".format(root=config.root_directory, sep=os.sep), "")
        fu.create_file("file", "{root}{sep}work{sep}log{sep}dummy.txt".format(root=config.root_directory, sep=os.sep), "")
        return config
