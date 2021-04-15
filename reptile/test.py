import json
import re

from tiezi.tie import Tie
from tool import Tool
from bs4 import BeautifulSoup
import os

if __name__ == '__main__':
    remove_other = re.compile(r'[^\w\u4e00-\u9fff]+')
    s = "啥时候全国第八了😅,。、，.\\'\""
    print(s)
    s = re.sub(remove_other, "", s)
    print(s)
