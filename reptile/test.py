import json
from tiezi.tie import Tie
from tool import Tool
from bs4 import BeautifulSoup
import os

if __name__ == '__main__':
    if not os.path.exists("爬取的文件"):
        os.mkdir("爬取的文件")