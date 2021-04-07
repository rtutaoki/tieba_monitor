import requests
from bs4 import BeautifulSoup
from reptile.tool import Tool


# 帖子实体
class Tie:
    def __init__(self, tie_id, author):
        self.id = tie_id
        self.author = author
        self.title = ""
        self.content = ""

    def fill_info(self):
        """
        根据id爬取相应帖子并填充标题和内容到实体类
        :return: Tie
        """
        url = r'https://tieba.baidu.com/p/' + self.id + r'?see_lz=1'
        headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/89.0.4389.114 Safari/537.36 "
        response = requests.get(url, headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', class_='core_title_txt')['title']
        content = str(soup.find('div', class_='d_post_content'))
        content = Tool().replace(content)
        self.title = title
        self.content = content
