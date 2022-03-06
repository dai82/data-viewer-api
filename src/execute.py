#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from flask.wrappers import Request

from common import request_utils as ru

from main.processor import *
from main.initial import *

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))


class DataViewerResponse:
    """
    メインクラスの実行時の引数として受け取る
    response_dataはclassがたが入るとエラーになるから返却するときは完全なdictにする
    """
    response_code: int
    response_data: dict

    def __init__(self, response_code: int, response_data: dict):
        self.response_code = response_code
        self.response_data = response_data


def initialize(logger, force_exec: bool):
    """
    :param logger:
    :param force_exec:
    :return:
    """
    try:
        logger.info("### initialize start ###")
        root_dir = os.path.dirname(os.getcwd())
        init_execute(root_dir, force_exec)
        logger.info("### initialize end ###")
    except Exception as e:
        logger.error("### File Register Abnormal End ... ###")
        raise e


def all_dv_board_mst(logger, aws: AwsConfig) -> ResponseData:
    """
    :param logger:
    :param aws:
    :return:
    """
    try:
        logger.info("### get-dv-board-mst start ###")
        dv_board_mst_list = get_dv_board_mst_list(aws)
        dict_result = []
        for board in dv_board_mst_list:
            dict_result.append(board.get_item())
        logger.info("### get-dv-board-mst end ###")
        return ResponseData(
            code=200,
            status="SUCCESS",
            message="OK",
            result={"dvBoardMstList": dict_result}
        )
    except Exception as e:
        logger.error("### get-dv-board-mst Abnormal End ... ###")
        raise e


def clear_all_dashboard_data(logger, aws: AwsConfig) -> ResponseData:
    try:
        logger.info("### clear_all_dashboard_data start ###")
        dv_board_mst_list = get_dv_board_mst_list(aws)
        for dv_board_mst in dv_board_mst_list:
            clear_dashboard_data(aws, dv_board_mst)
        logger.info("### clear_all_dashboard_data end ###")
        return ResponseData(
            code=200,
            status="SUCCESS",
            message="OK",
            result=True
        )
    except Exception as e:
        logger.error("### get-dv-board-mst Abnormal End ... ###")
        raise e


def file_register(logger, config: DataViewerConfig, aws: AwsConfig, req: Request) -> ResponseData:
    logger.info("### File Register Start ###")
    try:
        # ファイルをローカルにコピー & object化
        save_directory = config.backup_file_dir + os.sep + du.today(time=True)
        files = ru.save_and_get_csv_file(req, save_directory)
        f = files[0]
        # ヘッダとボディーに分解
        header, body = fp.convert_head_and_body(f)
        board_id = check_dashboard_info(aws, f)
        if board_id == '':
            # 未解析のファイル情報の場合はマスタ情報を登録する
            master = make_init_board_mst(aws, f, header)
        else:
            master = get_all_board_mst(aws, board_id)
        make_info(logger, aws, master, body)
        logger.info("### File Register Normal End !!! ###")
        return ResponseData(
            code=200,
            status="SUCCESS",
            message="OK",
            result=master.get_response_dict()
        )
    except Exception as e:
        logger.info("### File Register Abnormal End ... ###")
        raise e
