import re


class Tool:
    def __init__(self):
        # 去除img标签
        self.remove_img = re.compile('<img.*?>')
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
        # 去掉空格
        self.remove_n = re.compile(r'\n+')

    def replace(self, s):
        s = re.sub(self.remove_img, "", s)
        s = re.sub(self.remove_div, "", s)
        s = re.sub(self.remove_li, "", s)
        s = re.sub(self.remove_a, "", s)
        s = re.sub(self.remove_span, "", s)
        s = re.sub(self.remove_br, "", s)
        s = re.sub(self.remove_space, "", s)
        s = re.sub(self.remove_n, "\n", s)
        return s.strip()


