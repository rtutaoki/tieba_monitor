import re


class Tool:
    def __init__(self):
        # 去除img标签
        self.remove_img = re.compile('<img.*?>|</img>')
        # 去掉div标签
        self.remove_div = re.compile('<div.*?>|</div>')
        # 去掉li标签
        self.remove_li = re.compile('<li.*?>|</li>')
        # 去掉a标签
        self.remove_a = re.compile('<a.*?>|</a>')
        # 去掉span标签
        self.remove_span = re.compile('<span.*?>|</span>')
        # 将br改成换行符
        self.remove_br = re.compile('<br/>')
        # 去掉空格
        self.remove_space = re.compile(r' {2,}')
        # 去掉换行
        self.remove_n = re.compile(r'\n+')
        # 去掉其他符号
        self.remove_other = re.compile(r'[^\w\u4e00-\u9fff.,，。！!?？、；：;:\"\']+')

    def replace(self, s):
        """
        通用去除html中多余标签
        :param s: str
        :return:
        """
        s = re.sub(self.remove_img, "", s)
        s = re.sub(self.remove_div, "", s)
        s = re.sub(self.remove_li, "", s)
        s = re.sub(self.remove_a, "", s)
        s = re.sub(self.remove_span, "", s)
        s = re.sub(self.remove_br, "", s)
        s = re.sub(self.remove_space, "", s)
        s = re.sub(self.remove_n, "\n", s)
        return s.strip()

    def replace_other(self, s):
        """
        用于内容中无关表情符号之类去除，用户名中的不用去
        :param s: str
        :return:
        """
        s = re.sub(self.remove_other, "", s)
        return s.strip()
