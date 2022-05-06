from typing import Counter, List
from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.log import logger
from .utils import attribute_count, elements_react, get_equipment_info, get_skill_info, read_basic, read_profession, skill_text_trans
from kirico.utils.file_utils import check_dir, check_file
import time
import os
import json
import random

class Skill:
    def __init__(self,info):
        '''info为读取文件得到的技能配置'''
        self.__dict__.update(info)

    def count_total_hurt(self,one) -> int:
        '''
        根据配置项内的"hurt"，"hurt_increase"结合Fighter计算初始伤害值
        :rtype: 返回初始伤害值计算后int
        '''
        fighter_attribute = Counter(one.attribute()) + Counter(self.hurt)
        for i,j in self.hurt_increase.items():
            fighter_attribute[i] = int(fighter_attribute[i]*(100+j)/100)
        return fighter_attribute

    def count_total_increase(self,one):
        '''
        根据配置项内的"hurt"，"hurt_increase"结合Fighter计算加成
        :rtype: 返回加成后的Fighter
        '''
        pass
    
    def get_introduction():
        '''获取技能介绍'''
        pass





__failed_skill = ''

def find_skill(skill):
    '''
    根据提供的技能名来返回技能函数，若找不到此技能则记录该技能名返回空函数。
    '''
    global __failed_skill
    skill_book = globals()
    try:
        return skill_book[skill]
    except:
        __failed_skill = skill
        return null_skill

def null_skill(one,two):
    '''
    未找到技能时使用空技能，什么都不会发生
    '''
    return [one,two,0,[f"【{one.name}】尝试使用技能〖{__failed_skill}〗，但是失败了..."]]


def __example_skill_func(one,two):
    name = "skill_name"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values())
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，..."]]




# A

def Aid(one,two):
    name = "Aid"
    self = Skill(get_skill_info(name)[0])
    cure = sum(self.count_total_hurt(one).values())
    one.HP += cure
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，恢复自身 {cure} 点HP值..."]]

def AllMaster(one,two):
    name = "AllMaster"
    self = Skill(get_skill_info(name)[0])

    change_cAtk = int(one.Def*0.7 + one.Matk*0.3)
    one.cAtk += change_cAtk
    change_dAtk = int(one.Def*0.7 + one.Matk*0.3)
    one.dAtk += change_dAtk
    change_Matk = int(one.Mdef*0.5 + one.cAtk*0.3 + one.dAtk*0.3)
    one.Matk += change_Matk
    change_Def = int(one.cAtk*0.1+one.dAtk*0.1)
    one.Def += change_Def
    change_Mdef = int(one.Matk*0.2)
    one.Mdef += change_Mdef
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，增强了自身各项属性...\n【cAtk】{change_cAtk:+}\n【dAtk】{change_dAtk:+}\n【Matk】{change_Matk:+}\n【Def】{change_Def:+}\n【Mdef】{change_Mdef:+}"]]


# B

def BeastApotheosis(one,two):
    name = "BeastApotheosis"
    self = Skill(get_skill_info(name)[0])
    addition = self.count_total_hurt(one)
    one.__dict__.update(addition)
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，加强了各项属性，SP大量减少..."]]

def BeliefIncrease(one,two):
    name = "BeliefIncrease"
    self = Skill(get_skill_info(name)[0])
    addition = self.count_total_hurt(one)
    one.__dict__.update(addition)
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，加强了各项属性..."]]

def BlendAttack(one,two):
    name = "skill_name"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values()) - int(two.Def*0.4) - int(two.Mdef*0.4)
    two.HP -= dmg
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成了 {dmg} 点混合伤害..."]]

def BloodthirstyInstinct(one,two):
    name = "BloodthirstyInstinct"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values()) - two.Def
    two.HP -= dmg
    one.HP += int(0.4*dmg)
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成了 {dmg} 点伤害，自身回复 {int(0.4*dmg)} 点HP..."]]

# C

def CorruptMana(one,two):
    name = "CorruptMana"
    self = Skill(get_skill_info(name)[0])
    Atk_inc = int(one.Matk * 0.5)
    Matk_inc = int(one.cAtk * 0.3 + one.dAtk * 0.3)
    one.cAtk += Atk_inc
    one.dAtk += Atk_inc
    one.Matk += Matk_inc
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，三种攻击力分别增加了...\n【cAtk】{Atk_inc:+}\n【dAtk】{Atk_inc:+}\n【Matk】{Matk_inc:+}"]]

# D

def DraconicApotheosis(one,two):
    name = "DraconicApotheosis"
    self = Skill(get_skill_info(name)[0])
    increase = self.count_total_hurt(one)
    one.__dict__.update(Counter(one.attribute()) + Counter(increase))
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，大幅加强了自身各项数值。"]]

def DraconicBreath(one,two):
    name = "DraconicBreath"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values()) - two.Mdef
    two.HP -= dmg
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成 {dmg} 点伤害..."]]

def DraconicPunch(one,two):
    name = "DraconicPunch"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values()) - two.Def
    two.HP -= dmg
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成 {dmg} 点伤害..."]]

def DraconicStare(one,two):
    name = "DraconicStare"
    self = Skill(get_skill_info(name)[0])
    dmg = self.count_total_hurt(one)
    for i,j in dmg.item():
        two.__dict__[i] -= j
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，削弱了对方各项属性..."]]

# E

def ElfRecovery(one,two):
    name = "ElfRecovery"
    self = Skill(get_skill_info(name)[0])
    dmg = self.count_total_hurt(one)
    for i,j in dmg.item():
        one.__dict__[i] += j
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，恢复了HP和SP...\n【当前HP】{one.HP}\n【当前SP】{one.SP}"]]

def Enlightenment(one,two):
    name = "Enlightenment"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values())
    two.HP -= dmg
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成了 {dmg} 点伤害..."]]

def Escape(one,two):
    name = "Escape"
    self = Skill(get_skill_info(name)[0])
    return [one,two,3,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，成功逃脱了战局..."]]



# F

# G

# H

def HellFire(one,two):
    name = "HellFire"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values()) - two.Mdef
    two.HP -= dmg
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成了 {dmg} 点伤害..."]]



# I

# J

# K

# L

# M

# N

# O

def OrcResistance(one,two):
    name = "OrcResistance"
    self = Skill(get_skill_info(name)[0])
    dmg = self.count_total_hurt(one).values()
    for i,j in dmg.item():
        one.__dict__[i] += j
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，增加了防御力..."]]



# P

def PoisonMaster(one,two):
    name = "PoisonMaster"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values()) - two.Def
    two.HP -= dmg
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成了 {dmg} 点伤害..."]]



# Q

# R

# S

def SatanPossess(one,two):
    name = "SatanPossess"
    self = Skill(get_skill_info(name)[0])
    dmg = self.count_total_hurt(one).values()
    for i,j in dmg.item():
        one.__dict__[i] += j
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，各项属性大幅增加..."]]


# T

def TieflingMagic(one,two):
    name = "TieflingMagic"
    self = Skill(get_skill_info(name)[0])
    dmg = self.count_total_hurt(one).values()
    for i,j in dmg.item():
        one.__dict__[i] += j
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，各项属性大幅增加..."]]


# U

# V

def VineMagic(one,two):
    name = "VineMagic"
    return [one,two,0,["【藤蔓戏法】技能未完成。"]]

def ViolentForce(one,two):
    name = "ViolentForce"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values()) - two.Def
    two.HP -= dmg
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成了 {dmg} 点伤害..."]]

def VitalityAbsorb(one,two):
    name = "VitalityAbsorb"
    self = Skill(get_skill_info(name)[0])
    dmg = sum(self.count_total_hurt(one).values()) - two.Def
    recover = int(dmg*0.6)
    two.HP -= dmg
    one.HP += recover
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，向对方造成了 {dmg} 点伤害，并回复了自身 {int(dmg*0.6)} 点生命值..."]]



# W

def WeaponEnchantment(one,two):
    name = "WeaponEnchantment"
    self = Skill(get_skill_info(name)[0])
    Atk_inc = one.Matk*0.7
    Matk_inc = one.cAtk*0.4 + one.dAtk*0.4
    one.cAtk += Atk_inc
    one.dAtk += Atk_inc
    one.Matk += Matk_inc
    return [one,two,0,[f"【{one.name}】使用了技能〖{skill_text_trans(name)[0]}({name})〗，三种攻击力分别增加了...\n【cAtk】{Atk_inc:+}\n【dAtk】{Atk_inc:+}\n【Matk】{Matk_inc:+}"]]



# X

# Y

# Z

