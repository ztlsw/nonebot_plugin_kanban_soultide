#-*- coding:utf-8 _*-
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment
import random
from nonebot import logger
from pydantic import BaseModel, Extra
from io import BytesIO
from PIL import Image
from pathlib import Path 
from typing import Set, Union,Dict,List,Tuple
from .config import base_confi
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class MOE_CALL:
    def __init__(self):
        self.__get_json_ok=False     #读取json文件
        self.__cara : Dict[str,Dict[str,Union[int,str]]]={}  #角色文本
        self.cara_list:List[str]=[]
        self.cara_name : str = ""
        self.lim_cara : str=""
        self.cara_num : int = 0    #选定角色
        self.select_call : str=""
        self.tot_num :int = 0      #总个数
   
    def __init_json(self):
        lim_path : Path = base_confi.base_path/"moe_cara.json"
        with open(lim_path,"r",encoding='utf-8') as f:
            json_content=json.load(f)
            self.__cara=json_content.get("cara")
            self.cara_list =list(self.__cara)
            self.tot_num = len(self.cara_list)


        self.__get_json_ok=True
    
    async def cara_words(self,index:int)-> MessageSegment:
            if not self.__get_json_ok:
               self.__init_json()
            self.cara_name=self.cara_list[index-1]
            self.lim_cara=self.__cara.get(self.cara_name)
            self.select_call = self.lim_cara.get("select_call")
            return MessageSegment.text(self.select_call)

    async def ran_cara(self) -> Tuple[MessageSegment,int]:  #传回消息和图片序号
        #select one moe cara
        if not self.__get_json_ok:
            self.__init_json()

        self.cara_name = random.choice(self.cara_list)
        self.lim_cara=self.__cara.get(self.cara_name)   #获得随机文本内容
        self.cara_num=self.lim_cara.get("moe_number")
        self.select_call = self.lim_cara.get("select_call")

        return MessageSegment.text(self.select_call),self.cara_num
    
    async def send_img(self,index : int) ->MessageSegment:

        if not self.__get_json_ok:
            self.__init_json()

        #send the moe image
        lim_num_str: str = str(index)+".jpg"
        img_path :Path = base_confi.base_path/"img"/lim_num_str
        if not img_path.exists():
            return MessageSegment.text(f"图片加载错误...")
        else:
            imgh=Image.open(img_path)
        lisimg=BytesIO()
        imgh.save(lisimg,format='png')
        return MessageSegment.image(lisimg)
    
    async def get_cara_name(self,index : int) ->MessageSegment:
        if not self.__get_json_ok:
            self.__init_json()
        #send the moe name
        self.cara_name=self.cara_list[index-1]
        return  MessageSegment.text(f"当前板娘为{self.cara_name}")
    
    async def get_cara_list(self) -> Tuple[List[str],int]:
        if not self.__get_json_ok:
            self.__init_json()
        #send the moe list
        return self.cara_list,self.tot_num
    


'''
for moe_member in moe_choice:
    print(moe_member)
'''



moe_tide=MOE_CALL()