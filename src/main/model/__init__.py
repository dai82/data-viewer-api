#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from main.model.dv_board_mst_model import *
from main.model.dv_column_mst_model import *
from main.model.dv_display_mst_model import *
from main.model.dv_board_data_info_model import *
from main.model.dv_board_ver_info_model import *


class DvMaster:
    """
    マスタデータの一覧情報
    """
    board_id: str
    dv_board_mst: DvBoardMst
    dv_column_mst_list: list[DvColumnMst]
    dv_display_mst_list: list[DvDisplayMst]

    def __init__(self, board_id: str, dv_board_mst: DvBoardMst,
                 dv_column_mst_list: list[DvColumnMst], dv_display_mst_list: list[DvDisplayMst]):
        self.board_id = board_id
        self.dv_board_mst = dv_board_mst
        self.dv_column_mst_list = dv_column_mst_list
        self.dv_display_mst_list = dv_display_mst_list

    def get_response_dict(self):
        return {
            'dvBoardMst': self.dv_board_mst.get_item(),
            'dvColumnMstList': list(map(lambda x: x.get_item(), self.dv_column_mst_list)),
            'dvDisplayMstList': list(map(lambda x: x.get_item(), self.dv_display_mst_list))
        }
