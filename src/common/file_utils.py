#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# ディレクトリ・ファイル操作がわかりやすくまとまっている
# https://qiita.com/supersaiakujin/items/12451cd2b8315fe7d054

import os.path
import shutil
import glob
from pathlib import Path

from common import file_processor as fp


def file_exists(full_path=None):
    """
    ファイルが存在していたらTrue, 存在しなければFalseを返します
    File Directory 両方に有効です
    :param full_path:
    :return:
    """
    p = Path(full_path)
    if not Path.is_file(p) and not Path.is_dir(p):
        return False
    return True


def move_directory(bfr_path, aft_path, exist_error=True, recreate=False):
    """
    ${bfr_path} -> ${aft_path} に対してファイル・ディレクトリを転送する処理 \r\n
    exist_error=True: ${aft_path}が既に存在すれば、 FireExistsErrorを返します \r\n
    recreate=True: ${aft_path}が既に存在すれば、${aft_path}を全削除したのちに転送します \r\n
    \r\n
    TODO 権限の制御
    """
    # 転送前のディレクトリが存在しなければ何もしない
    if not file_exists(bfr_path):
        return
    # 転送先のルートディレクトリが存在していたらエラーとする
    if file_exists(aft_path) and exist_error:
        raise FileExistsError("[ ${path} ] is exists.".format(path=aft_path))
    # 転送先のルートディレクトリをDel -> Insで作り直す
    if file_exists(aft_path) and recreate:
        shutil.rmtree(aft_path, ignore_errors=True)
    os.rename(bfr_path, aft_path)


def delete_file(file_type: str, path: str) -> None:
    """
    ディテクトリ、ファイルを強制削除します
    :param file_type:
    :param path:
    :return:
    """
    if file_exists(path):
        isdir = os.path.isdir(path)
        if isdir:
            shutil.rmtree(path)
        else:
            os.remove(path)


def create_directory(full_path):
    if file_exists(full_path):
        return
    is_dir = os.path.isdir(full_path)
    if is_dir:
        os.makedirs(full_path)
    else:
        directory = full_path.replace(full_path.split(os.sep)[-1], "")
        if not file_exists(directory):
            os.makedirs(directory)


def create_file(file_type, path, contents, is_exists=False) -> False:
    """
    ファイルを作成します。
    :param file_type:
    :param path:
    :param contents:
    :param is_exists: ファイルが存在したらFalseを返します
    :return:
    """
    if file_exists(path) and is_exists:
        return False
    if file_type == 'json':
        # ディレクトリがなかったら作成する
        create_directory(path)
        fp.write_json(path, contents)
    elif file_type == 'file':
        create_directory(path)
        fp.write_file(path, contents)
    else:
        raise Exception('{type} : type is not defined'.format(type=type))


def get_path_list(file_dir: str, filter_str: str = None) -> list:
    """
    特定のディレクトリ直下のファイルディレクトリまでのパスを返します
    :param file_dir:
    :param filter_str: この文字列を含む物だけを返します
    :return:
    """
    bfr_dir = os.getcwd()
    # ディレクトリが存在しなければ、からのリストを返す
    if not file_exists(file_dir):
        return []
    # 取得元のディレクトリへ移動
    os.chdir(file_dir)
    # 相対パス取得
    all_list = glob.glob("*")
    if filter_str is not None:
        filter_list = list(filter(lambda x: x.find(filter_str) != -1, all_list))
        return list(map(lambda x: file_dir + os.sep + x, filter_list))
    os.chdir(bfr_dir) # 元のディレクトリに戻る
    return list(map(lambda x: file_dir + os.sep + x, all_list))