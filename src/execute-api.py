#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import logging

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from common.aws import *
from common import file_utils as fu
from common import json_utils as ju
from main.initial import DataViewerConfig
import execute as ex

app = Flask(__name__)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/init-app')
def init_app(inner_exec: bool = False):
    logger = logging.getLogger('[INIT-APP]')
    ex.initialize(logger, True)
    if inner_exec:
        logger.info("[init_app] is normal end")
        return
    return make_response(jsonify({'success': 'Is OK !'}), 200)


@app.route('/all-dv-board-mst')
def all_dv_board_mst(inner_exec: bool = False):
    """
    全ての db_board_mstのデータを取得する
    """
    # 実行ユーザーのログイン情報を取得
    aws = get_exec_user_config()
    logging.basicConfig(level=config.log_level)
    logger = logging.getLogger('[GET-DV-BOARD-MST]')
    if inner_exec:
        logger.info("[GET-DV-BOARD-MST] is normal end")
        return
    res = ex.all_dv_board_mst(logger, aws)
    return make_response(jsonify(res.get_response()), res.code)


@app.route('/clear-all-dashboard-data', methods=["POST"])
def clear_all_dashboard_data(inner_exec: bool = False):
    """
    全ての db_board_mstのデータを取得する
    """
    # 実行ユーザーのログイン情報を取得
    aws = get_exec_user_config()
    logging.basicConfig(level=config.log_level)
    logger = logging.getLogger('[CLEAR-ALL-DASHBOARD-DATA]')
    if inner_exec:
        logger.info("[CLEAR-ALL-DASHBOARD-DATA] is normal end")
        return
    res = ex.clear_all_dashboard_data(logger, aws)
    return make_response(jsonify(res.get_response()), res.code)


# 参考
# https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/patterns/fileuploads.html
@app.route("/init-register", methods=["POST"])
def init_register():
    try:
        # 実行ユーザーのログイン情報を取得
        aws = get_exec_user_config()
        logging.basicConfig(level=config.log_level)
        logger = logging.getLogger('[INIT-REGISTER]')
        res = ex.file_register(logger, config, aws, request)
        return make_response(jsonify(res.get_response()), res.code)
    except Exception as e:
        return make_response(jsonify({'result': True, 'message': e}), 500)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found ...'}), 404)


sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))

# setting.json(configファイル)を読み込みます
config_path = os.path.dirname(os.getcwd()) + os.sep + 'setting.json'
prop_path = os.path.dirname(os.getcwd()) + os.sep + 'property'

# configファイルを読み込む
config: DataViewerConfig = ''
if fu.file_exists(config_path):
    config = ju.convert_obj(fp.read_json(config_path))


def execute(arg: list[str]):
    # configファイルが読み込めない場合は処理しない
    if config == '' and sys.argv[1] != 'init':
        raise Exception('config file cannot read ...')
    # (Error) typeパラメータ未定義
    elif arg.__len__() < 1:
        raise Exception('type parameter is not defined ...')
        exit(1)
    #
    # 初期ディレクトリやsetting.jsonの作成
    #
    elif sys.argv[1] == 'init':
        init_app(inner_exec=True)
    #
    # apiを起動する
    #
    elif sys.argv[1] == 'api':
        print('################################')
        print('### Data Viewer API Start !! ###')
        print('################################')
        app.run(debug=True, host="0.0.0.0", port=8010)
    else:
        raise Exception('type parameter [${type}] is not defined...'.format(sys.argv[1]))
        exit(1)


if __name__ == '__main__':
    execute(sys.argv)


