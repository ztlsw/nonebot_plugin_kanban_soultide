from nonebot import on_command, on_regex,require,get_bots
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.event import MessageEvent,Message
from nonebot.params import CommandArg,ArgPlainText
from pathlib import Path 
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, PrivateMessageEvent, GroupMessageEvent
from typing import List, Dict, Union
from .config import base_confi
from .engine_time import *
from .read_data import moe_tide
from random import randint
import asyncio
try:
    import ujson as json
except ModuleNotFoundError:
    import json


moe_cara_help = on_command(cmd="板娘帮助",priority=8)
ran_cara = on_command(cmd="随机板娘",priority=8)
now_cara = on_command(cmd="当前板娘",priority=8)
cara_list=on_command(cmd="板娘列表",priority=8)
choose_cara=on_command(cmd="选择板娘",priority=8)
open_cara =on_command(cmd="开启板娘",priority=8)
close_cara=on_command(cmd="关闭板娘",priority=8)


gp_path : Path = base_confi.base_path/"gmpersion.json"


timing = require("nonebot_plugin_apscheduler").scheduler



with open(gp_path,"r",encoding='utf-8') as e:
    json_lim=json.load(e)
    dict_used_in_group : dict[str: int]=json_lim.get("used_in_group")
    dict_used_in_member: dict[str: int]=json_lim.get("used_in_member")
    used_in_group : List[str]=json_lim.get("used_in_group")
    used_in_member : List[str]=json_lim.get("used_in_member")

async def check_id(gp_id : str , us_id :str) -> bool:                         #检测是否已经开启使用
    if gp_id=="-1":
        if us_id not in used_in_member:
            return 0
        else:
            return 1
    else:
        if gp_id not in used_in_group:
            return 0
        else :
            return 1
        
async def change_user_cara(gp_id:str,us_id:str,cs_cara:int) -> None:    #添加修改
    if gp_id=="-1":                                                     #私聊使用
        dict_used_in_member.update({us_id:cs_cara})
        json_lim["used_in_member"]= dict_used_in_member
    else :                                                              #群聊使用
        dict_used_in_group.update({gp_id:cs_cara})
        json_lim["used_in_group"]= dict_used_in_group
    with open(gp_path,"w",encoding="utf-8") as e:
        e.write(json.dumps(json_lim,indent=4))


@open_cara.handle()
async def _(bot:Bot,event:MessageEvent):
    us_id=str(event.user_id)
    gp_id="-1"
    try:
        gp_id=str(event.group_id)
    except:
        pass
   
    check_id_ok=await check_id(gp_id,us_id)

    if check_id_ok:
        await open_cara.finish(f"板娘插件已经是开启状态")
    else:
        await change_user_cara(gp_id,us_id,1)
    await open_cara.finish(f"板娘插件已开启，默认板娘为阿卡赛特")

@close_cara.handle()
async def _(bot: Bot,event:MessageEvent):
    us_id=str(event.user_id)
    gp_id="-1"
    try:
        gp_id=str(event.group_id)
    except:
        pass
   
    check_id_ok=await check_id(gp_id,us_id)
    if not check_id_ok:
        await close_cara.finish(f"板娘插件已经是关闭状态")
    else:
        if gp_id=="-1":                                                     #私聊使用
           left_id_behind=dict_used_in_member.pop(us_id)
           json_lim["used_in_member"]= dict_used_in_member
        else :                                                              #群聊使用
            left_id_behind=dict_used_in_group.pop(gp_id)
            json_lim["used_in_group"]= dict_used_in_group
    with open(gp_path,"w",encoding="utf-8") as e:
        e.write(json.dumps(json_lim,indent=4))
    await close_cara.finish(f"板娘插件已关闭")


@moe_cara_help.handle()
async def _(bot:Bot,event:MessageEvent):
    moe_help_sent : str = "0.开启/关闭板娘\n1.随机板娘（随机抽取看板娘）\n 2.当前板娘（查看当前看板娘）\n3.板娘列表（查看所有被记录的看板娘）\n4.选择板娘\n"
    await moe_cara_help.finish(moe_help_sent)


@ran_cara.handle()
async def _(bot:Bot,event:MessageEvent):
    us_id=str(event.user_id)
    gp_id="-1"
    try:
        gp_id=str(event.group_id)
    except:
        pass
   
    check_id_ok=await check_id(gp_id,us_id)
    if not check_id_ok:
        await ran_cara.finish(f"板娘插件已经是关闭状态")
    else:
        msg,cara_num_lim=await moe_tide.ran_cara()
        await change_user_cara(gp_id,us_id,cara_num_lim)
    cara_num  = cara_num_lim
    await ran_cara.send(msg)
    img_message=await moe_tide.send_img(cara_num_lim)
    await ran_cara.finish(img_message)


@ now_cara.handle()
async def _(bot:Bot,event:MessageEvent):
    us_id=str(event.user_id)
    gp_id="-1"
    try:
        gp_id=str(event.group_id)
    except:
        pass
    check_id_ok=await check_id(gp_id,us_id)
    if not check_id_ok:
        await now_cara.finish(f"板娘插件已经是关闭状态")
    if gp_id=="-1":
        now_cara_id=dict_used_in_member[us_id]
    else:
        now_cara_id=dict_used_in_group[gp_id]
    cara_name=await moe_tide.get_cara_name(now_cara_id)
    await now_cara.send(cara_name)
    img_message=await moe_tide.send_img(now_cara_id)
    await now_cara.finish(img_message)


@ cara_list.handle()
async def _(bot:Bot,envent:MessageEvent):
    str_cara_list : str = ""
    cara_lis : List[str]=[]
    cara_lis,tot_num= await moe_tide.get_cara_list()
    for i in range(tot_num):
        str_cara_list+=str(i+1)+"."+cara_lis[i]+"\n"
    await cara_list.finish(str_cara_list)
        
@choose_cara.handle()
async def _(bot:Bot,event: MessageEvent):
    us_id=str(event.user_id)
    gp_id="-1"
    try:
        gp_id=str(event.group_id)
    except:
        pass
    check_id_ok=await check_id(gp_id,us_id)
    if not check_id_ok:
        await choose_cara.finish(f"板娘插件已经是关闭状态")
    await choose_cara.send(f"请输入板娘名称")

@choose_cara.got("choose_cara_name")
async def _(bot: Bot,event: MessageEvent,choose_cara_name : str = ArgPlainText(),):
    cara_lis,tot_num= await moe_tide.get_cara_list()
    us_id=str(event.user_id)
    gp_id="-1"
    try:
        gp_id=str(event.group_id)
    except:
        pass
    try:
       cara_num=cara_lis.index(choose_cara_name)
       cara_num+=1
    except:
        await choose_cara.finish(MessageSegment.text(f"没有该板娘信息，请检查输入"))
    await change_user_cara(gp_id,us_id,cara_num)
    cara_call=await moe_tide.cara_words(cara_num)
    await choose_cara.send(cara_call)
    img_message=await moe_tide.send_img(cara_num)
    await choose_cara.finish(img_message)



#打招呼
@timing.scheduled_job("cron", hour='7', minute='00', id="good_morning",max_instances=10)
async def _():
    await time_eng.good_morning()
    await asyncio.sleep(randint(2, 5))

@timing.scheduled_job("cron", hour='14', minute='00',id="good_afternoon",max_instances=10)
async def _():
    await time_eng.good_afternoon()
    await asyncio.sleep(randint(2, 5))

@timing.scheduled_job("cron", hour='19', minute='00',id="good_evening",max_instances=10)
async def _():
    await time_eng.good_evening()
    await asyncio.sleep(randint(2, 5))

@timing.scheduled_job("cron", hour='00', minute='00', id="good_night",max_instances=10)
async def _():
    await time_eng.good_night()
    await asyncio.sleep(randint(2, 5))
