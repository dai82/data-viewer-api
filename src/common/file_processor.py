#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import json
import re

from common.model.__init__ import FileInfo


def console_out_json(contents: dict = "dummy"):
    print(json.dumps(contents, indent=4, sort_keys=True, default=str, ensure_ascii=False))


def read_json(file_path: str) -> dict:
    """
    jsonファイルを読み込んで jsonのdict objectを返します
    :param file_path:
    :return: dict
    """
    try:
        f = open(file_path, 'r', encoding="utf-8")
        json_dict: dict = json.load(f)
        return json_dict
    except Exception as e:
        print(e)
        raise e


def write_json(file_path: str, contents: any) -> None:
    json_contents = json.dumps(contents, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    with open(file_path, mode="w", encoding="utf-8", errors="ignore") as f:
        f.write(json_contents)


def read_file(file_path) -> str:
    try:
        f = open(file_path, 'r', encoding="utf-8", errors="ignore")
        content = ""
        for line in f:
            content += line
        return content
    except Exception as e:
        print(e)
        raise e
    finally:
        f.close()


def write_file(file_path, content):
    with open(file_path, mode="w", encoding="utf-8", errors="ignore") as f:
        f.write(content)


def get_obj(file: FileInfo) -> dict or str:
    if file.file_type == 'json':
        return read_json(file.file_path)
    else:
        return read_file(file.file_path)


REPLACE_BLOCK = '[dv-block]'
REGEX = "\\\".*?\\\""


def convert_head_and_body(file: FileInfo) -> [list[str], list[list[str]]]:
    """
    csvタイプのファイルを1行目をヘッダ、2行目以降をbodyとみなして取得する
    :param file:
    :return:
    """
    def _double_quote_escape(_line: str) -> list[str]:
        """
        カンマ区切りで文字列を切り取る
        ただし、シングルクォーテーションで区切られた文字列がある場合は、その中にカンマがあっても区切り文字とはみなさない
        【正規表現】 https://note.nkmk.me/python-re-match-search-findall-etc/
        """
        match_result = re.findall(REGEX, _line)
        replace_line = re.sub(REGEX, REPLACE_BLOCK, _line)
        _result = []
        index = 0
        for elem in replace_line.split(","):
            if elem == REPLACE_BLOCK:
                _result.append(match_result[index])
                index += 1
            else:
                _result.append(elem)
        return _result

    result = get_obj(file)
    header = result.split("\n")[0].split(",")
    body = list(map(lambda x: _double_quote_escape(x), result.split("\n")[1:]))
    return header, body
