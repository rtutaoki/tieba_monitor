import json
from tiezi.tie import Tie
from tool import Tool
from bs4 import BeautifulSoup
import os

if __name__ == '__main__':
    parent_path = os.path.dirname(os.getcwd())
    path = os.path.join(parent_path, "爬取的文件")
    file_list = os.listdir(path)
    for i in file_list:
        print(os.path.join(parent_path, i))