import nonebot
from nonebot import logger
from pydantic import BaseModel, Extra
from pathlib import Path 
from typing import Set, Union
import httpx
from aiocache import cached
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class Base_config(BaseModel,extra=Extra.ignore):
    base_path: Path=Path(__file__).parent

driver = nonebot.get_driver()



base_confi=Base_config()