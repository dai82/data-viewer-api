
import os

from flask.wrappers import Request

from common import file_utils as fu
from common.model import FileInfo


def get_param(req: Request) -> dict:
    """
    Request内のパラメータを取得 \n
    :param req:
    :return:
    """
    param = {}
    for key, value in req.values.items():
        param.update({key: value})
    return param


def save_and_get_csv_file(req: Request, save_directory: str) -> list[FileInfo]:
    """
    Request内のファイルを取得 \n
    fileはオブジェクトに変換するタイミングでローカルに保存される \n
    :param req:
    :param save_directory:
    :return:
    """
    result = []
    fu.create_directory(save_directory)
    for filename, file in req.files.items():
        filepath = save_directory + os.sep + filename
        fu.create_file("file", filepath, "", True)
        file.save(filepath)
        result.append(FileInfo('csv', filepath))
    return result
