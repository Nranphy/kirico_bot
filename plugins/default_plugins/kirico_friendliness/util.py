from pathlib import Path
from typing import Union
import json

from utils.basic_utils import kirico_logger
from utils.friendliness_utils import KiricoFriendliness


root_path = Path(__file__).parent / "resource/"
'''好感度回复根目录'''

greeting_path = root_path / "greeting/"
'''问候回复目录'''

interactivity_path = root_path / "interactivity/"
'''交互回复目录'''



def use_nickname(sentence:str, nickname:str) -> str:
    '''将句子sentence中的[NICK]与[NICKS]替换为爱称'''
    return sentence.replace("[NICK]",nickname).replace("[NICKS]", nickname+"的")

def get_interactivity_data(qq:Union[str,int]) -> dict:
    '''返回该qq号的交互次数记录'''
    friendliness_info = KiricoFriendliness(qq)
    return friendliness_info.interactivity_count

_interactivity_trans = {}
def _load_interactivity_trans():
    for path in interactivity_path.iterdir():
        if not path.name.endswith(".json"):
            continue
        try:
            with open(path, "r", encoding="UTF-8-sig") as f:
                temp_data:dict = json.load(f)
        except:
            continue
        _interactivity_trans[temp_data.get("name", "Unkown")] = temp_data.get("name_tran", "未定义")
_load_interactivity_trans()
        

def get_transname(name:str) -> str:
    '''返回标准英文交互名的中文翻译'''
    return _interactivity_trans.get(name, "未定义")

default_interactivity_reply = {}
def _get_default_interactivity_reply():
    try:
        with open(interactivity_path/"_default", "r", encoding="UTF-8-sig") as f:
            default_data:dict = json.load(f)
    except:
        kirico_logger("warning", "雾子交互", "默认交互回复文件配置有误或不存在。")
        default_data = {}
    default_interactivity_reply["success"] = default_data.get("success", [""])
    default_interactivity_reply["fail"] = default_data.get("fail", [""])
    default_interactivity_reply["over"] = default_data.get("over", [""])
_get_default_interactivity_reply()