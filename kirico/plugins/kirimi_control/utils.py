from typing import Union
from nonebot import on_command, on_regex, require, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin.plugin import get_loaded_plugins, get_plugin
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER
from nonebot.exception import IgnoredException
from nonebot.log import logger
from kirico.utils.basic_utils import get_config
from kirico.utils.file_utils import check_dir,check_file
import os
import json





def control_plugin_switch(name:str, status:bool, groupid:Union[str,int]) -> bool:
    '''控制插件开关
    :param name: 插件英文名
    :param status: 开关状态，True为开启
    :param groupid: 需要控制开关的群号
    :rtype: 返回是否成功改变开关状态，目前False只因为开关已经是目标状态。'''
    data_path = os.getcwd()+"/kirico/data/kirico_switch/"
    check_dir(data_path)
    check_file(data_path+f"{groupid}.json")
    try:
        with open(data_path+f"{groupid}.json","r") as f:
            switch = json.load(f)
    except:
        switch = {}
    if switch.get(name,True) == status:
        return False
    else:
        switch[name] = status
    with open(data_path+f"{groupid}.json","w") as f:
        json.dump(switch, f)
    return True
    


def control_groupchat_switch(status:bool, groupid:Union[str,int]) -> bool:
    '''控制机器人开关
    :param status: 开关状态，True为开启
    :param groupid: 需要控制开关的群号
    :rtype: 返回是否成功改变开关状态，目前False只因为开关已经是目标状态。'''
    data_path = os.getcwd()+"/kirico/data/kirico_switch/"
    check_dir(data_path)
    check_file(data_path+f"{groupid}.json")
    try:
        with open(data_path+f"{groupid}.json","r") as f:
            switch = json.load(f)
    except:
        switch = {}
    if switch.get("CHAT",True) == status:
        return False
    else:
        switch["CHAT"] = status
    with open(data_path+f"{groupid}.json","w") as f:
        json.dump(switch, f)
    return True


def get_switch_status(groupid:Union[str,int]) -> dict:
    '''
    获取对应群号的开关信息
    :param groupid: 所需信息的群号
    '''
    data_path = os.getcwd()+"/kirico/data/kirico_switch/"
    check_dir(data_path)
    check_file(data_path+f"{groupid}.json")
    try:
        with open(data_path+f"{groupid}.json","r") as f:
            switch = json.load(f)
    except:
        switch = {}
    return switch


def if_groupchat_on(groupid:Union[str,int]) -> bool:
    '''
    获取对应群号是否开启机器人群聊
    :param groupid: 需要判断的群号
    '''
    switch_info = get_switch_status(groupid)
    return switch_info.get("CHAT",True)

def if_plugin_on(groupid:Union[str,int],name:str) -> bool:
    '''
    获取对应群号是否开启某插件
    :param groupid: 需要判断的群号
    :param name: 需要判断的插件英文名
    '''
    switch_info = get_switch_status(groupid)
    return switch_info.get(name,True)