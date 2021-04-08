import requests
from bs4 import BeautifulSoup
from reptile.tool import Tool
import json
from tiezi.tiezi_content import TieContent


# 帖子实体
class Tie:
    def __init__(self, tie_id, author):
        self.id = tie_id
        self.author = author
        self.title = ""
        self.content = []

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

        page = self.get_page(soup)
        for i in range(page):
            response = requests.get(url.format(i+1), headers)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # 将内容放入
            user_list = self.set_user_list(soup)
            content_list = self.set_content(soup)
            for j in range(len(content_list)):
                tc = TieContent(user_list[j]['id'], user_list[j]['name'], content_list[j])
                self.content.append(tc.TC_to_dict())

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
        user_list = []
        data = soup.find_all('li', class_='d_name')
        for i in data:
            user = {}
            user_data = json.loads(i['data-field'])
            user['id'] = user_data['user_id']
            user['name'] = Tool().replace(str(i))
            user_list.append(user)
        return user_list

    def set_content(self, soup):
        """
        用于获取所有楼层内容
        :param soup: BeautifulSoup
        :return: list
        """
        content_list = []
        data = soup.find_all('div', class_='d_post_content')
        for i in data:
            content_list.append(Tool().replace(str(i)))
        return content_list


if __name__ == '__main__':
    tie = Tie("7288086844", "贴吧用户_0PCy216")
    tie.fill_info()
    print(tie.content)