#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import string_utils as su
from common import date_utils as du


from main.model import *


def check_dashboard_info(aws: AwsConfig,  file: FileInfo) -> str:
    """
    同じファイル名で登録がないか確認し以前に同じファイル名での登録があれば
    対象Itemのboard_idを返却する
    """
    # DV_BOARD_MSTのデータがそもそも空なら false
    json_list = adp.scan_all_data(aws, 'DvBoardMst')
    if json_list.__len__() == 0:
        return ''
    for json_elem in json_list:
        dv_board_mst = DvBoardMst()
        dv_board_mst.set_data(json_elem)
        if dv_board_mst.file_name == file.file_name:
            return str(dv_board_mst.board_id)
    return ''


def make_init_board_mst(aws: AwsConfig, file: FileInfo, header: list[str]) -> DvMaster:
    """
    新規のダッシュボードのmasterデータを作成する
    :param aws:
    :param file:
    :param header:
    :return:
    """
    # dv_board_mst
    board_id = su.get_uuid()
    new_sort = adp.get_count(aws, 'DvBoardMst') + 1
    dv_board_mst = DvBoardMst(
        board_id=board_id,
        active=True,
        file_name=file.file_name,
        display_sort=new_sort
    )
    adp.set_data(aws, dv_board_mst)
    # dv_column_mst
    # dv_display_mst
    dv_column_mst_list = []
    dv_display_mst_list = []
    idx = 0
    for key in header:
        idx += 1
        dv_column_mst = DvColumnMst(board_id, idx, key, 'str')
        adp.set_data(aws, dv_column_mst)
        dv_column_mst_list.append(dv_column_mst)
        dv_display_mst = DvDisplayMst(board_id, 'normal', idx, key, 'str', 'label')
        adp.set_data(aws, dv_display_mst)
        dv_display_mst_list.append(dv_display_mst)
    adp.set_all_data(aws, dv_column_mst_list)
    adp.set_all_data(aws, dv_display_mst_list)
    return DvMaster(
        board_id=board_id,
        dv_board_mst=dv_board_mst,
        dv_column_mst_list=dv_column_mst_list,
        dv_display_mst_list=dv_display_mst_list
    )


def get_all_board_mst(aws: AwsConfig, board_id: str) -> DvMaster:
    dv_board_mst = adp.get_data(aws, DvBoardMst(), {'board_id': board_id})
    dv_column_mst_list = query_dv_column_mst_list(aws, board_id)
    dv_display_mst_list = query_dv_display_mst_list(aws, board_id, 'normal')
    return DvMaster(
        board_id=board_id,
        dv_board_mst=dv_board_mst,
        dv_column_mst_list=dv_column_mst_list,
        dv_display_mst_list=dv_display_mst_list
    )


def clear_dashboard_data(aws: AwsConfig, dv_board_mst: dv_board_mst_model):
    board_id = dv_board_mst.board_id
    # dv_board_data_info (info側から消す)
    dv_board_data_info_list = query_dv_board_data_info_list(aws, board_id)
    adp.delete_all_data(aws, dv_board_data_info_list, 'board_version_column_row_mix')
    # dv_board_ver_info
    dv_board_ver_info_list = query_dv_board_ver_info_list(aws, board_id)
    adp.delete_all_data(aws, dv_board_ver_info_list, 'board_id', 'version')
    # dv_display_mst
    dv_display_mst_list = query_dv_display_mst_list(aws, board_id)
    adp.delete_all_data(aws, dv_display_mst_list, 'board_type_column_mix')
    # dv_column_mst
    dv_column_mst_list = query_dv_column_mst_list(aws, board_id)
    adp.delete_all_data(aws, dv_column_mst_list, 'board_id', 'column_id')
    # dv_board_mst (メインは最後に消す)
    adp.delete_data(aws, dv_board_mst, 'board_id')


def make_info(logger, aws: AwsConfig, master: DvMaster, body: list[list[str]]) -> bool:
    """
    mst情報を基に取得データからダッシュボードデータを作成
    """
    def _extract_elem(_master: DvMaster, _cell: str) -> Optional[DvColumnMst]:
        """
        ファイルのindexと合致するdv_column_mstを取得する
        """
        _target = list(filter(lambda x: x.column_id == _cell, _master.dv_column_mst_list))
        if _target.__len__() == 0:
            logger.info("[${cell}] is not defined in DvColumnMst".format(cell=cell))
            return None
        else:
            return _target[0]

    def _pre_register_check(_master: DvMaster, _data_info_line: list[DvBoardDataInfo]):
        """
        エラーがないかどうかをチェックする
        """
        result = True
        if _data_info_line.__len__() != _master.dv_column_mst_list.__len__():
            logger.warn("Column Mst size is [{mst}]. but line is [{list}]".format(
                mst=_master.dv_column_mst_list.__len__(),
                list=_data_info_line.__len__()
            ))
            return False
        return True

    try:
        # dv_board_ver_infoの更新
        dv_board_ver_info: DvBoardVerInfo = query_latest_board_ver_info(aws, master.board_id)
        if dv_board_ver_info is None:
            dv_board_ver_info = DvBoardVerInfo(
                board_id=master.board_id,
                version=1,
                active=True,
                upload_date=du.today()
            )
        else:
            dv_board_ver_info.version += 1
        adp.set_data(aws, dv_board_ver_info)
        db_obj_data = []
        row = 0
        for line in body:
            row += 1
            db_obj_line = []
            for col, cell in enumerate(line):
                elem = _extract_elem(master, col+1)
                logger.debug("row:{row},col:{col} -> {contents}".format(row=row, col=col+1, contents=cell))
                if elem is None:
                    continue
                else:
                    db_obj_line.append(DvBoardDataInfo(
                        board_id=master.board_id,
                        version=dv_board_ver_info.version,
                        col_id=col+1,
                        col_nm=elem.column_name,
                        row_id=row,
                        content=cell,
                        create_date=du.today(),
                        prc_date=du.today()
                    ))
            if _pre_register_check(master, db_obj_line):
                db_obj_data.extend(db_obj_line)
        adp.set_all_data(aws, db_obj_data)
        return True
    except Exception as e:
        raise e