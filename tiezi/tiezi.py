import requests
from bs4 import BeautifulSoup
from reptile.tool import Tool
import json


# 帖子实体
class Tie:
    def __init__(self, tie_id, author):
        self.id = tie_id
        self.author = author
        self.title = ""
        self.content = []
        self.user_list = []

    def fill_info(self):
        """
        根据id爬取相应帖子并填充标题和内容到实体类
        :return:
        """
        url = r'https://tieba.baidu.com/p/' + self.id + '?pn={}'
        headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/89.0.4389.114 Safari/537.36 "
        response = requests.get(url.format(1), headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h1', class_='core_title_txt')['title']
        self.title = title

        # 先将第一页内容获取
        self.set_user_list(soup)
        self.set_content(soup)

        page = self.get_page(soup)
        for i in range(1, page):
            response = requests.get(url.format(i+1), headers)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # 将剩余页内容放入
            self.set_user_list(soup)
            self.set_content(soup)

    def get_page(self, soup):
        """
        获取帖子的总页数
        :param soup: BeautifulSoup
        :return:
        """
        data = soup.find_all('span', class_='red')
        page = int(Tool().replace(str(data[1])))
        return page

    def set_user_list(self, soup):
        """
        用于获取所有楼层发言人的用户名及id
        :param soup: BeautifulSoup
        :return: list
        """
        data = soup.find_all('li', class_='d_name')
        for i in data:
            user = {}
            user_data = json.loads(i['data-field'])
            user['id'] = user_data['user_id']
            user['name'] = Tool().replace(str(i))
            self.user_list.append(user)

    def set_content(self, soup):
        """
        用于获取所有楼层内容
        :param soup: BeautifulSoup
        :return:
        """
        data = soup.find_all('div', class_='d_post_content')
        for i in data:
            self.content.append(Tool().replace(str(i)))