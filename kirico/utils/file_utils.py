'''文件操作类工具'''

from pathlib import Path
from typing import Optional, Union
import json

from .basic_utils import KiricoDatetime, get_config


def check_dir(path: Union[str, Path]) -> bool:
    '''
    检查目录是否存在，并递归创建目标目录，若目录已存在则不进行更改。
    :param path: 目标目录路径
    :rtype: 返回该目录是否本就存在
    '''
    path = Path(path)
    if path.is_dir():
        return True
    else:
        check_dir(path.parent)
        path.mkdir()
        return False


def check_file(path: Union[str, Path]):
    '''
    检查文件是否存在，并递归创建父目录和该文件，若文件已存在则不进行更改。
    :param path: 目标文件路径
    :rtype: 返回该文件是否本就存在
    '''
    path = Path(path)
    if path.is_file():
        return True
    else:
        check_dir(path.parent)
        with open(path, "w"):
            pass
        return False


def rm_path(path: Union[str, Path]):
    '''
    递归删除目录或删除文件。
    :param path: 目标路径
    '''
    path = Path(path)
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        for i in path.iterdir():
            rm_path(i)


# Kirico用json存档
# 直接提供存档接口，需要接入数据库请直接修改相关接口。
kirico_data_path:Path = Path.cwd() / get_config("save_path", Path("kirico/data/"), Path)
'''雾子专有的data目录'''

def get_path(name: str) -> Path:
    '''获得传入功能名的数据目录'''
    return kirico_data_path / name

def save_data(name: str, data_id: Union[str,int], data:dict) -> bool:
    '''
    以json保存用户数据文件到Kirico专有data目录
    :param name: 保存的功能名
    :param data_id: 用户的唯一识别id
    :param data: 将保存的数据
    注意保存会覆盖原有文件信息
    '''
    with open(kirico_data_path / f"{name}/{data_id}.json", "w", encoding="UTF-8-sig") as f:
        json.dump(data, f)

def load_data(name: str, data_id: Union[str,int]) -> dict:
    '''
    以json从Kirico专有data目录读取用户数据文件
    :param name: 保存时的功能名
    :param data_id: 同一功能下唯一识别id
    文件不存在时创建文件并返回空字典
    '''
    target_path = kirico_data_path / f"{name}/{data_id}.json"
    check_file(target_path)
    with open(target_path, "r", encoding="UTF-8-sig") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    return data



# 非重要数据目录
kirico_cache_path:Path = Path.cwd() / get_config("temp_path", Path("data/temp/"), Path)
'''非重要数据目录'''


# 冷却相关
kirico_cd_cache_path:Path = kirico_cache_path / "cd/"
'''CD冷却数据存放目录'''

def set_cd(name:str, second:int, user_id:Optional[Union[str,int]] = None, group_id:Optional[Union[str,int]] = None):
    '''
    为name功能增加CD
    :param name: 用以区别的功能名
    :param second: 从此刻算起的冷却时间秒数
    :param user_id: 添加冷却的用户id
    :param group_id: 添加冷却的群id
    :若user_id与group_id均留空，则为全局冷却；两者均提供则均增加冷却
    '''
    user_id = str(user_id)
    group_id = str(group_id)
    
    now_date = KiricoDatetime().timestamp
    available_timestamp = now_date + 1000*second

    root_path = kirico_cd_cache_path / name
    global_path = root_path / "global"
    user_path = root_path / "user"
    group_path = root_path / "group"

    if not (user_id and group_id):
        with open(global_path, "w") as f:
            f.write(available_timestamp)
        return
    
    if user_id:
        if check_file(user_path):
            with open(user_path, "r") as f:
                user_cd_data = json.load(f)
        else:
            user_cd_data = {}
        user_cd_data[user_id] = available_timestamp
        with open(user_path, "w") as f:
            json.dump(user_cd_data, f)
    
    if group_id:
        if check_file(group_path):
            with open(group_path, "r") as f:
                group_cd_data = json.load(f)
        else:
            group_cd_data = {}
        group_cd_data[group_id] = available_timestamp
        with open(group_path, "w") as f:
            json.dump(group_cd_data, f)

def check_cd(name:str, user_id:Optional[Union[str,int]] = None, group_id:Optional[Union[str,int]] = None):
    '''
    检查目标name功能的CD是否到期
    :param name: 用以区别的功能名
    :param user_id: 检查冷却的用户id
    :param group_id: 检查冷却的群id
    :rtype: 返回CD是否过去，即是否建议进行后续操作
    '''
    user_id = str(user_id)
    group_id = str(group_id)

    now_date = KiricoDatetime().timestamp

    root_path = kirico_cd_cache_path / name
    global_path = root_path / "global"
    user_path = root_path / "user"
    group_path = root_path / "group"

    # 未设定过冷却
    if not root_path.is_dir():
        return True

    # 依层次检查
    if global_path.is_file():
        with open(global_path, "r") as f:
            available_timestamp = int(f.read())
        if now_date < available_timestamp:
            return False
    if group_path.is_file():
        with open(group_path, "r") as f:
            available_timestamp = json.load(f).get(group_id, 0)
        if now_date < available_timestamp:
            return False
    if user_path.is_file():
        with open(user_path, "r") as f:
            available_timestamp = json.load(f).get(user_id, 0)
        if now_date < available_timestamp:
            return False
    return True