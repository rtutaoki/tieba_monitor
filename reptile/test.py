import json
from tiezi.tiezi import Tie
from tool import Tool
from bs4 import BeautifulSoup

if __name__ == '__main__':
    path = r'C:\Users\xd\Desktop\tieba_monitor\爬取的html文件\武汉理工大学吧第3页.html'
    htmlfile = open(path, 'r', encoding='utf-8')
    htmlhandle = htmlfile.read()
    soup = BeautifulSoup(htmlhandle, 'html.parser')
    data = soup.find_all('span', class_='red')
    print(Tool().replace(str(data[1])))