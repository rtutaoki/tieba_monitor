import requests
from bs4 import BeautifulSoup
import json
from tiezi.tie import Tie


class TiebaReptile:
    def __init__(self, name):
        self.tb_name = name  # 贴吧名
        self.url = "https://tieba.baidu.com/f?kw=" + name + "&ie=utf-8&pn={}"  # 创建url，pn是页数，{}方便后续填充

    def get_url(self, page):
        """
        用于得到所有想要爬取的页的url地址
        :param page: int
        :return: list
        """
        url_list = []
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
        :param html_str:
        :param page_num:
        :return:
        """
        file_name = r"C:\Users\xd\Desktop\tieba_monitor\爬取的文件\{}.txt".format(tie.id)
        with open(file_name, mode='w', encoding='utf-8') as f:
            for i in tie.content:
                json.dump(i, f, ensure_ascii=False)
                f.write('\n')

    def get_tiezi(self, soup):
        """
        从html文件中提取到各个帖子的位置
        :param soup: BeautifulSoup
        :return: list
        """
        res = soup.find_all('li', class_='j_thread_list')
        list_tie = []
        for i in res:
            json_dict = json.loads(i['data-field'])
            id = str(json_dict['id'])
            if json_dict['author_nickname']:
                user_name = json_dict['author_nickname']
            else:
                user_name = json_dict['author_name']

            list_tie.append(Tie(id, user_name))
        return list_tie

    def run(self, page):
        """
        主要运行程序，完成整个爬取操作
        :param page: int
        :return:
        """
        url_list = self.get_url(page)
        for i in range(len(url_list)):
            soup = self.pass_url(url_list[i])
            tie_list = self.get_tiezi(soup)
            for j in range(len(tie_list)):
                tie_list[j].fill_info()
                self.save_file(tie_list[j])
                print("爬取进度：" + str(i * 50 + j + 1) + "/" + str(len(url_list) * 50))


if __name__ == '__main__':
    test = TiebaReptile("武汉理工大学")
    test.run(1)
    # # url = r"https://tieba.baidu.com/f?kw=武汉理工大学&ie=utf-8&pn=0"
    # url = r"https://tieba.baidu.com/p/7288086844"
    # soup_test = test.pass_url(url)
    # test.save_file(soup_test.prettify(), 4)
    # print(soup_test.prettify())
    # res = soup_test.find_all('div', class_='d_post_content')
    # # # print(res[0]['data-field'])
    #print(res)
