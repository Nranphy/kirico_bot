from typing import Tuple, Union
import json

from kirico.utils.basic_utils import if_plugin_exists, get_plugin_metadata
from kirico.utils.file_utils import check_dir, check_file, kirico_data_path, save_data, load_data


_switch_data_pathname = "kirico_switch"
'''开关相关文件目录名'''

_return_code = {
    100 : "成功",
    201 : "插件不存在",
    202 : "插件已为目标状态"
}




def control_plugin_switch(name:str, status:bool, groupid:Union[str,int]) -> Tuple[bool, int]:
    '''控制插件开关
    :param name: 插件英文名
    :param status: 将要设置的开关状态，True为开启
    :param groupid: 需要控制开关的群号
    :rtype: 返回是否成功改变开关状态及状态码
    '''
    if not if_plugin_exists(name):
        return (False, 201)

    switch = load_data(_switch_data_pathname, groupid)
    
    if name in switch and switch[name] == status:
        return (False, 202)
    else:
        switch[name] = status
    
    save_data(_switch_data_pathname, groupid, switch)
    return (True, 100)
    


def control_groupchat_switch(status:bool, groupid:Union[str,int]) -> Tuple[bool, int]:
    '''
    控制机器人说话开关
    :param status: 开关状态，True为开启
    :param groupid: 需要控制开关的群号
    :rtype: 返回是否成功改变开关状态及状态码
    '''
    switch = load_data(_switch_data_pathname, groupid)
    
    if "CHAT" in switch and switch["CHAT"] == status:
        return (False, 202)
    else:
        switch["CHAT"] = status
    
    save_data(_switch_data_pathname, groupid, switch)
    return (True, 100)


def get_switch_status(groupid:Union[str,int]) -> dict:
    '''
    获取对应群号的开关配置信息
    :param groupid: 所需信息的群号
    '''
    return load_data(_switch_data_pathname, groupid)


def if_groupchat_on(groupid:Union[str,int]) -> bool:
    '''
    获取对应群号是否开启机器人群聊
    :param groupid: 需要判断的群号
    '''
    switch_info = get_switch_status(groupid)
    return switch_info.get("CHAT",True)

def if_plugin_on(groupid:Union[str,int], name:str) -> bool:
    '''
    获取对应群号是否开启某插件
    :param groupid: 需要判断的群号
    :param name: 需要判断的插件英文名
    '''
    switch_info = get_switch_status(groupid)
    if name not in switch_info:
        metadata = get_plugin_metadata(name)
        if metadata and metadata.default_enable:
            return True
        else:
            return False
    
    else:
        return switch_info[name]