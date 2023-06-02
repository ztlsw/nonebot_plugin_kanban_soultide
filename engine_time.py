#-*- coding:utf-8 _*-
from nonebot import on_command, on_regex,require,get_bot
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.event import MessageEvent,Message
from nonebot.params import ArgStr,CommandArg,Matcher
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (
    Bot, 
    MessageSegment, 
    PrivateMessageEvent, 
    GroupMessageEvent,
    MessageEvent,
    ActionFailed,
)
from typing import List, Dict, Union,Tuple
from pathlib import Path 
from .config import base_confi
from .read_data import moe_tide
import asyncio
import os
from random import randint
try:
    import ujson as json
except ModuleNotFoundError:
    import json
lim_path : Path = base_confi.base_path/"moe_cara.json"
gp_path : Path = base_confi.base_path/"gmpersion.json"

class TIME_ENG:
    def __init__(self):
        self.cara_dict:dict[str,dict[str,Union[int,str]]] ={}
        self.cara_list : List[str] =[]
        self.dict_used_in_group: dict[str:int] =[]
        self.dict_used_in_member:dict[str:int] =[]
        self.used_in_group:List[str] =[]
        self.used_in_member:List[str] =[]
        self.open_cara_file_ok:bool = 0
        self.open_group_file_ok:bool=0
    

    def open_cara_file(self):
        with open(lim_path,"r",encoding='utf-8') as f:
            json_content=json.load(f)
            self.cara_dict = json_content.get("cara")
            self.cara_list =list(json_content.get("cara"))
        self.open_cara_file_ok=1

    def open_group_file(self):
        with open(gp_path,"r",encoding='utf-8') as e:
            json_lim=json.load(e)
            self.dict_used_in_group : dict[str: int]=json_lim.get("used_in_group")
            self.dict_used_in_member: dict[str: int]=json_lim.get("used_in_member")
            self.used_in_group : List[str]=json_lim.get("used_in_group")
            self.used_in_member : List[str]=json_lim.get("used_in_member")
        self.open_group_file_ok=1
    
    async def greeting(self, call_type: str):
        bot: Bot = get_bot()
        if not self.open_cara_file_ok:
            self.open_cara_file()
            self.open_cara_file_ok=1

        if not self.open_group_file_ok:
            self.open_group_file()
            self.open_group_file_ok=1

        for gp_id in self.used_in_group:
            cara_num: int=self.dict_used_in_group.get(gp_id)
            cara_name: str=self.cara_list[cara_num-1]
            lim_dict : dict[str:str]=self.cara_dict.get(cara_name)
            lim_str : str=  lim_dict.get(call_type)
            try:
                await bot.send_group_msg(group_id=int(gp_id),message=lim_str)
            except:
                await bot.send_group_msg(group_id=int(gp_id),message="呜呜，发不出来")

        for us_id in self.used_in_member:
            cara_num: int=self.dict_used_in_member.get(us_id)
            cara_name: str=self.cara_list[cara_num-1]
            lim_dict : dict[str:str]=self.cara_dict.get(cara_name)
            lim_str : str=  lim_dict.get(call_type)
            try:
                await bot.send_private_msg(user_id=int(us_id),message=lim_str)
            except:
                await bot.send_private_msg(user_id=int(us_id),message="呜呜，发不出来")

time_eng=TIME_ENG()