import re


class Tool:
    def __init__(self):
        # 去除img标签,7位长空格
        self.remove_img = re.compile('<img.*?>| {7}|')
        # 去掉div
        self.remove_div = re.compile('<div.*?>|</div>')
        # 将br改成换行符
        self.remove_br = re.compile('<br/>')
        # 去掉空白字符
        self.remove_n = re.compile('/s{2,}')

    def replace(self, s):
        s = re.sub(self.remove_img, "", s)
        s = re.sub(self.remove_div, "", s)
        s = re.sub(self.remove_br, "", s)
        s = re.sub(self.remove_n, "", s)
        return s.strip()


