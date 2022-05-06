from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent
from nonebot.log import logger
from kirico.utils.file_utils import check_dir, check_file
from .config import kirico_segai_config
from typing import Counter, List
from math import floor
from cmath import log
import time
import random
import os
import json



# 文字格式化
def race_text_format(race):
    '''
    方便地获得种族中文名。
    '''
    if race=="人类" or race=="Human" or race=="human":race="Human"
    elif race=="精灵" or race=="Elf" or race=="elf":race="Elf"
    elif race=="龙裔" or race=="Dragonborn" or race=="dragonborn":race="Dragonborn"
    elif race=="半精灵" or race=="Half_Elf" or race=="half_elf":race="Half_Elf"
    elif race=="半兽人" or race=="Half_Orc" or race=="half_orc":race="Half_Orc"
    elif race=="恶魔" or race=="Tiefling" or race=="tiefling":race="Tiefling"
    else :race="Unknown"
    return race

def race_text_trans(race):
    '''
    将标准的英语种族名转化为文件内的译名。
    '''
    try:
        race_info = get_race_info(race)
        return race_info["transrace"]
    except:
        return "未翻译"

def job_text_format(job):
    '''
    方便地进行职业称呼标准化。
    '''
    if job=="初心者" or job=="Novice" or job=="novice":job="Novice"
    elif job=="精灵" or job=="Elf" or job=="elf":job="Elf"
    return job

def job_text_trans(race):
    '''
    将标准的英语职业名转化为文件内的译名。
    '''
    try:
        job_info = get_job_info(race)
        return job_info["transrace"]
    except:
        return "未翻译"

def skill_text_trans(skill) -> list:
    '''
    将标准的英语种族名转化为文件内的译名。
    :param skill: 技能标准英文名的str或list
    :rtype: 返回译名列表
    '''
    if not isinstance(skill,list):
        skill = [skill]
    need = list()
    for key in skill:
        main_path = os.path.abspath(os.path.dirname(__file__))+f"/resources/skill/{key}.json"
        try:
            with open(main_path,"r",encoding="utf-8-sig") as f:
                skill_info = json.load(f)
        except:
            skill_info = {}
        need.append(skill_info.get("detail",{}).get("transname","未翻译"))
    return need


# 角色文件读取

def role_exist(qq) -> bool:
    '''
    通过检查用户文件夹是否存在来判断是否已注册
    :param qq: 需要查询的QQ号.
    :rtype bool: 返回QQ是否已注册角色.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    if os.path.isdir(main_path):
        return True
    else:return False


def read_basic(qq) -> dict:
    '''
    获取所输入QQ的角色basic信息.
    :param qq: 需要查询的QQ号.
    :rtype dict: 包含basic文件内各项信息.获取失败则返回空字典.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    try:
        with open(main_path+"basic.json","r",encoding="utf-8-sig") as f:
            basic = json.load(f)
    except:
        return {}
    return basic

def read_statu(qq) -> dict:
    '''
    获取所输入QQ的角色statu信息.
    :param qq: 需要查询的QQ号.
    :rtype dict: 包含statu文件内各项信息.获取失败则返回空字典.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    try:
        with open(main_path+"statu.json","r",encoding="utf-8-sig") as f:
            statu = json.load(f)
    except:
        return {}
    return statu

def read_profession(qq) -> dict:
    '''
    获取所输入QQ的角色profession信息.
    :param qq: 需要查询的QQ号.
    :rtype dict: 包含profession文件内各项信息.获取失败则返回空字典.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    try:
        with open(main_path+"profession.json","r",encoding="utf-8-sig") as f:
            profession = json.load(f)
    except:
        return {}
    return profession

def read_bag(qq) -> dict:
    '''
    获取所输入QQ的角色bag信息.
    :param qq: 需要查询的QQ号.
    :rtype dict: 包含bag文件内各项信息.获取失败则返回空字典.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    try:
        with open(main_path+"bag.json","r",encoding="utf-8-sig") as f:
            bag = json.load(f)
    except:
        return {}
    return bag

def read_honor(qq) -> dict:
    '''
    获取所输入QQ的角色honor信息.
    :param qq: 需要查询的QQ号.
    :rtype dict: 包含honor文件内各项信息.获取失败则返回空字典.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    try:
        with open(main_path+"honor.json","r",encoding="utf-8-sig") as f:
            honor = json.load(f)
    except:
        return {}
    return honor


# 角色文件保存

def save_basic(qq,new:dict):
    '''
    保存所输入QQ的角色新的basic信息.
    :param qq: 需要查询的QQ号.
    :rtype bool: 保存成功则返回True，反之False.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    basic_path = main_path+"basic.json"
    try:
        check_dir(main_path)
        check_file(basic_path)
        with open(basic_path,"w",encoding="utf-8-sig") as f:
            json.dump(new,f)
    except:
        return False
    return True

def save_statu(qq,new:dict):
    '''
    保存所输入QQ的角色新的statu信息.
    :param qq: 需要查询的QQ号.
    :rtype bool: 保存成功则返回True，反之False.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    statu_path = main_path+"statu.json"
    try:
        check_dir(main_path)
        check_file(statu_path)
        with open(statu_path,"w",encoding="utf-8-sig") as f:
            json.dump(new,f)
    except:
        return False
    return True

def save_profession(qq,new:dict):
    '''
    保存所输入QQ的角色新的profession信息.
    :param qq: 需要查询的QQ号.
    :rtype bool: 保存成功则返回True，反之False.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    profession_path = main_path+"profession.json"
    try:
        check_dir(main_path)
        check_file(profession_path)
        with open(profession_path,"w",encoding="utf-8-sig") as f:
            json.dump(new,f)
    except:
        return False
    return True

def save_bag(qq,new:dict):
    '''
    保存所输入QQ的角色新的bag信息.
    :param qq: 需要查询的QQ号.
    :rtype bool: 保存成功则返回True，反之False.
    '''
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    bag_path = main_path+"bag.json"
    try:
        check_dir(main_path)
        check_file(bag_path)
        with open(bag_path,"w",encoding="utf-8-sig") as f:
            json.dump(new,f)
    except:
        return False
    return True

def save_honor(qq,new:dict):
    '''
    保存所输入QQ的角色新的honor信息.
    :param qq: 需要查询的QQ号.
    :rtype bool: 保存成功则返回True，反之False.
    '''
    # 根据配置处理记录长度
    kirico_sagai_fight_record_length = kirico_segai_config("kirico_sagai_fight_record_length",5)
    if len(new["fight_record"]) > kirico_sagai_fight_record_length:
        new["fight_record"] = new["fight_record"][:kirico_sagai_fight_record_length]
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    honor_path = main_path+"honor.json"
    try:
        check_dir(main_path)
        check_file(honor_path)
        with open(honor_path,"w",encoding="utf-8-sig") as f:
            json.dump(new,f)
    except:
        return False
    return True

# 系统文件读取

def get_race_info(race:str) -> dict:
    '''
    获取所输入种族的系统信息.
    :param race: 需要查询的种族名，可为中文.人类|精灵|龙裔|半精灵|半兽人|恶魔
    :rtype dict: 包含该种族文件内各项信息.获取失败则返回空字典.
    '''
    race = race_text_format(race)
    main_path = os.path.abspath(os.path.dirname(__file__))+f"/resources/race/{race}.json"
    try:
        with open(main_path,"r",encoding="utf-8-sig") as f:
            race_info = json.load(f)
    except:
        return {}
    return race_info

def get_job_info(job:str) -> dict:
    '''
    获取所输入职业的系统信息.
    :param job: 需要查询的职业名，可为中文.
    :rtype dict: 包含该种族文件内各项信息.获取失败则返回空字典.
    '''
    job = job_text_format(job)
    main_path = os.path.abspath(os.path.dirname(__file__))+f"/resources/job/{job}.json"
    try:
        with open(main_path,"r",encoding="utf-8-sig") as f:
            job_info = json.load(f)
    except:
        return {}
    return job_info

def get_equipment_info(equipment) -> list:
    '''
    获取所输入武器编号的系统信息.
    :param equipment: 需要查询的装备编号，可为list,str,int.
    :rtype dict: 包含所查询装备文件内各项信息，查询出错的项为空字典.
    '''
    if not isinstance(equipment,list):
        equipment = [str(equipment)]
    need = list()
    for key in equipment:
        main_path = os.path.abspath(os.path.dirname(__file__))+f"/resources/equipment/{key}.json"
        try:
            with open(main_path,"r",encoding="utf-8-sig") as f:
                equipment_info = json.load(f)
        except:
            equipment_info = {}
        need.append(equipment_info)
    return need

def get_item_info(item) -> list:
    '''
    获取所输入物品编号的系统信息.
    :param item: 需要查询的物品编号，可为list,str,int.
    :rtype dict: 包含所查询物品文件内各项信息，查询出错的项为空字典.
    '''
    if not isinstance(item,list):
        item = [str(item)]
    need = list()
    for key in item:
        main_path = os.path.abspath(os.path.dirname(__file__))+f"/resources/item/{key}.json"
        try:
            with open(main_path,"r",encoding="utf-8-sig") as f:
                item_info = json.load(f)
        except:
            item_info = {}
        need.append(item_info)
    return need

def get_skill_info(item) -> list:
    '''
    获取所输入技能编号的系统信息.
    :param item: 需要查询的技能编号，可为list,str,int.
    :rtype dict: 包含所查询技能文件内各项信息，查询出错的项为空字典.
    '''
    if not isinstance(item,list):
        item = [str(item)]
    need = list()
    for key in item:
        main_path = os.path.abspath(os.path.dirname(__file__))+f"/resources/skill/{key}.json"
        try:
            with open(main_path,"r",encoding="utf-8-sig") as f:
                item_info = json.load(f)
        except:
            item_info = {}
        need.append(item_info)
    return need




# 游戏系统

## 属性值计算
def attribute_count(qq) -> dict:
    '''
    计算所输入QQ的角色属性值，战斗和查询都从这里。
    :param qq: 需要计算的QQ号.
    :rtype dict: 包含各项计算数值.计算失败则各项属性为0.
    '''
    statu_dic = read_statu(qq)
    profession_dic = read_profession(qq)

    equipment_info = get_equipment_info(profession_dic["equipment"])
    skill_info = get_skill_info(profession_dic["skill"])
    job_info = get_job_info(profession_dic["job"])

    attribute_dic = {"HP":0,"SP":0,"cAtk":0,"dAtk":0,"Matk":0,"Hit":0,"Cri":0,"Def":0,"Mdef":0,"Flee":0,"Aspd":0}
    addition_dic = Counter({"HP":0,"SP":0,"cAtk":0,"dAtk":0,"Matk":0,"Hit":0,"Cri":0,"Def":0,"Mdef":0,"Flee":0,"Aspd":0})
    addition_percent_dic = Counter({"HP":100,"SP":100,"cAtk":100,"dAtk":100,"Matk":100,"Hit":100,"Cri":100,"Def":100,"Mdef":100,"Flee":100,"Aspd":100})

    for equip in equipment_info:
        addition_dic += Counter(equip.get("addition",{}))
        addition_percent_dic += Counter(equip.get("addition_percent",{}))

    for skill in skill_info:
        addition_dic += Counter(skill.get("addition",{}))
        addition_percent_dic += Counter(equip.get("addition_percent",{}))

    addition_dic += Counter(job_info["initial_addition"])


    try:
        attribute_dic["HP"] = (floor(200+profession_dic["level"]**2//9+profession_dic["level"]*(statu_dic["Vit"]+100)/100) + addition_dic["HP"]) * addition_percent_dic["HP"] // 100
        attribute_dic["SP"] = (floor(30+profession_dic["level"]*(100+statu_dic["Int"])/100) + addition_dic["SP"]) * addition_percent_dic["SP"] // 100
        attribute_dic["cAtk"] = (floor(statu_dic["Str"]+(statu_dic["Str"]//10)**2+statu_dic["Dex"]//5+statu_dic["Luk"]//5) + addition_dic["cAtk"]) * addition_percent_dic["cAtk"] // 100
        attribute_dic["dAtk"] = (floor(statu_dic["Dex"]+(statu_dic["Dex"]//10)**2+statu_dic["Str"]//5+statu_dic["Luk"]//5) + addition_dic["dAtk"]) * addition_percent_dic["dAtk"] // 100
        attribute_dic["Matk"] = (floor(statu_dic["Int"]+(statu_dic["Int"]//8)**2+statu_dic["Dex"]//5+statu_dic["Luk"]//5) + addition_dic["Matk"]) * addition_percent_dic["Matk"] // 100
        attribute_dic["Hit"] = (floor((100+statu_dic["Luk"])/100*(100+statu_dic["Dex"]//5)) + addition_dic["Hit"]) * addition_percent_dic["Hit"] // 100
        attribute_dic["Cri"] = (floor(statu_dic["Luk"]*0.3+100) + addition_dic["Cri"]) * addition_percent_dic["Cri"] // 100
        attribute_dic["Def"] = (floor((statu_dic["Vit"]+statu_dic["Vit"]**2//100)*(100+statu_dic["Agi"])/100) + addition_dic["Def"]) * addition_percent_dic["Def"] // 100
        attribute_dic["Mdef"] = (floor((statu_dic["Vit"]+statu_dic["Vit"]**2//100)*(100+statu_dic["Int"])/100) + addition_dic["Mdef"]) * addition_percent_dic["Mdef"] // 100
        attribute_dic["Flee"] = (floor((100+statu_dic["Agi"])/100*(100+statu_dic["Luk"]//5)) + addition_dic["Flee"]) * addition_percent_dic["Flee"] // 100
        attribute_dic["Aspd"] = (floor(100+(statu_dic["Agi"]+statu_dic["Dex"]//4)) + addition_dic["Aspd"]) * addition_percent_dic["Aspd"] // 100
    except:
        pass
    return attribute_dic
    
## 获得经验值
def gain_exp(qq,avg,de):
    '''
    增加该QQ角色经验值并自动升级。
    :param qq: 目标QQ号
    :param avg: 经验增加水平值
    :param de: 经验增加偏差值
    :rtype list:返回[增长经验int,升级次数int,升级获得点数int,剩余点数int,角色profession信息dict,新获得技能list,可转职职业list].
    '''
    profession = read_profession(qq)
    statu = read_statu(qq)

    increase_exp = random.randint(avg-de,avg+de)
    exp = increase_exp+profession["exp"]
    needexp = profession["needexp"]
    level = profession["level"]
    up_cnt = 0
    gain_point = 0
    while exp >= 60*(level+10)**2:
        exp -= 60*(level+10)**2
        level += 1
        up_cnt += 1
        gain_point += floor(log(level,3).real + 2)
    needexp = 60*(level+10)**2-exp

    profession["exp"],profession["needexp"],profession["level"],statu["point"] = exp,needexp,level,statu["point"]+gain_point

    bag = read_bag(qq)
    race_info = get_race_info(profession["race"])
    job_info = get_job_info(profession["job"])
    new_skill, can_jobchange = [],[]
    for i,j in race_info["skill"]:
        if profession["level"] < i:
            break
        elif j not in bag["skill"]:
            new_skill.append(j)
            bag["skill"].append(j)
    for i,j in job_info["skill"]:
        if profession["level"] < i:
            break
        elif j not in bag["skill"]:
            new_skill.append(j)
            bag["skill"].append(j)
    for i in job_info["jobchange"]:
        info = get_job_info(i)
        if profession["level"]>=info["accept_level"] and profession["race"] not in info["unaccept_rage"] and profession["job"] in info["accept_job"]:
            can_jobchange.append(i)

    save_bag(qq,bag)
    save_profession(qq,profession)
    save_statu(qq,statu)
    return [increase_exp, up_cnt, gain_point, statu["point"], profession, new_skill, can_jobchange]

## 转职
def jobchange_to(qq,job:str,sure:bool = False) -> list:
    '''
    对输入的QQ号角色进行转职。
    :param qq: 需要转职的QQ
    :param job: 需要转职的职业
    :param sure: 是否确定转职
    :rtype list:满足要求或转职成功则返回[True]，此时列表第二项为新增技能，第三项为当前装备；否则返回False，此时列表第二项为原因.
    '''
    job = job_text_format(job)
    profession_dic = read_profession(qq)
    bag_dic = read_bag(qq)
    job_info = get_job_info(job)
    if profession_dic["job"] not in job_info["accept_job"]:
        return [False,"你的职业不支持转职为该职业哦~"]
    if profession_dic["level"] < job_info["accept_level"]:
        return [False,"你的等级暂时不够转职为该职业~"]
    if profession_dic["race"] in job_info["unaccept_rage"]:
        return [False,"你的种族决定了你不能转职为该职业！"]
    if not sure:
        return [True]
    
    profession_dic["job"] = job
    add_skill = list()
    for i,j in job_info["skill"]:
        if profession_dic["level"] >= i and j not in bag_dic["skill"]:
            bag_dic["skill"].append(j)
            add_skill.append(j)
        else:
            break
    for i in range(5):
        if job_info["initial_equipments"][i] != "None":
            profession_dic["equipment"][i] = job_info["initial_equipments"][i]
        if job_info["initial_equipments"][i] not in bag_dic["equipment"]:
            bag_dic["equipment"].append(job_info["initial_equipments"][i])
    profession_dic["skill"] = [] # 清空已装备技能
    save_bag(qq,bag_dic)
    save_profession(qq,profession_dic)
    return [True,add_skill,profession_dic["equipment"]]

## 元素克制
def elements_react(one:str,two:str) -> int:
    '''
    对传入的两个元素进行反应判断
    前者克制后者返回1，前者对后者弱化返回2，不反应返回0
    若传入元素错误，则返回0
    '''
    elements = ('Earth','Water','Wind','Fire','Dark','Light','Normal')
    if one not in elements or two not in elements:
        return 0 # 单纯把这个情况独立出来
    elements_restrain = (('Earth','Water'),('Water','Fire'),('Fire','Wind'),('Wind','Earth'),('Light','Dark'),('Dark','Light'))
    if (one,two) in elements_restrain: # 光暗互克，直接返回
        return 1
    elif (two,one) in elements_restrain:
        return 2
    else:
        return 0

