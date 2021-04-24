import requests
from bs4 import BeautifulSoup
import json
from tiezi.tie import Tie
import os


class TiebaReptile:
    def __init__(self, name):
        self.tb_name = name  # 贴吧名
        self.url = "https://tieba.baidu.com/f?kw=" + name + "&ie=utf-8&pn={}"  # 创建url，pn是页数，{}方便后续填充

    def get_url(self, item_nums):
        """
        用于得到所有想要爬取的页的url地址
        :param item_nums: int
        :return: list[str]
        """
        url_list = []
        page = item_nums // 50 + 1
        for i in range(page):
            url_list.append(self.url.format(i * 50))
        return url_list

    def pass_url(self, url):
        """
        获取网页响应
        :param url: str
        :return: BeautifulSoup
        """
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/89.0.4389.114 Safari/537.36 ",
        }
        response = requests.get(url, headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def save_file(self, tie):
        """
        将爬取的html文件保存到本地
        :param tie: Tie
        :return:
        """
        file_path = os.path.join(os.path.dirname(os.getcwd()), "爬取的文件")
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = file_path + r"\{}.txt".format(tie.tie_id)
        with open(file_name, mode='w', encoding='utf-8') as f:
            if tie.title:
                tie_str = str(tie.tie_id) + "||" + str(tie.author_id) + "||" + str(tie.author) + "||" + \
                          str(tie.title) + "||" + str(tie.tie_id)
                f.write(tie_str)
                f.write('\n')
            for i in tie.content:
                f.write(i.fc_to_str())
                f.write('\n')

    def get_tiezi(self, soup, item_nums):
        """
        从html文件中提取到各个帖子的位置
        :param item_nums: int
        :param soup: BeautifulSoup
        :return: list[Tie]
        """
        url_list = soup.find_all('li', class_='j_thread_list')
        tie_list = []
        n = 0   # 用于控制获取指定个数的帖子
        for i in url_list:
            if n >= item_nums:
                break
            json_dict = json.loads(i['data-field'])
            tie_id = str(json_dict['id'])
            if json_dict['author_nickname']:
                user_name = json_dict['author_nickname']
            else:
                user_name = json_dict['author_name']

            tie_list.append(Tie(tie_id, user_name))
            n += 1
        return tie_list

    def run(self, item_nums):
        """
        主要运行程序，完成整个爬取操作
        :param item_nums: int
        :return:
        """
        item_nums_temp = item_nums  # 用于控制获取的帖子数
        url_list = self.get_url(item_nums_temp)
        for i in range(len(url_list)):
            soup = self.pass_url(url_list[i])
            tie_list = self.get_tiezi(soup, item_nums_temp)
            for j in range(len(tie_list)):
                tie_list[j].fill_info()
                self.save_file(tie_list[j])
                print("爬取进度：" + str(i * 50 + j + 1) + "/" + str(item_nums))
            item_nums_temp -= 50


if __name__ == '__main__':
    test = TiebaReptile("武汉理工大学")
    test.run(10)
    # # url = r"https://tieba.baidu.com/f?kw=武汉理工大学&ie=utf-8&pn=0"
    # url = r"https://tieba.baidu.com/p/7288086844"
    # soup_test = test.pass_url(url)
    # test.save_file(soup_test.prettify(), 4)
    # print(soup_test.prettify())
    # res = soup_test.find_all('div', class_='d_post_content')
    # # # print(res[0]['data-field'])
    #print(res)
