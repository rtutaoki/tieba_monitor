# 帖子每层实体
class TieContent:
    def __init__(self, user_id="", user_name="", user_content="", tie_id=""):
        self.user_id = user_id
        self.user_name = user_name
        self.user_content = user_content
        self.tie_id = tie_id

    def tc_to_str(self):
        """
        将TieContent转换成字符串方便写入
        :return: str
        """
        return str(self.user_id) + "||" + str(self.user_name) + "||" + str(self.user_content) + "||" + str(self.tie_id)


def str_to_tc(tc_str):
    """
    将字符串转换成TieContent实体
    :param tc_str: str
    :return: TieContent
    """
    info = tc_str.split("||")


if __name__ == '__main__':
    s = "||aa||hahahah||444"
    info = s.split("||")
    print(info)