# 帖子每层实体
class FloorContent:
    def __init__(self, user_id="", user_name="", user_content="", tie_id=""):
        self.user_id = user_id
        self.user_name = user_name
        self.floor_content = user_content
        self.tie_id = tie_id

    def fc_to_str(self):
        """
        将TieContent转换成字符串方便写入
        :return: str
        """
        return str(self.user_id) + "||" + str(self.user_name) + "||" + str(self.floor_content) + "||" + str(self.tie_id)


def str_to_fc(tc_str):
    """
    将字符串转换成TieContent实体
    :param tc_str: str
    :return: TieContent
    """
    fc_info = tc_str.split("||")
    fc = FloorContent(fc_info[0], fc_info[1], fc_info[2], fc_info[3])
    return fc


if __name__ == '__main__':
    s = "||aa||hahahah||444"
    info = s.split("||")
    print(info)