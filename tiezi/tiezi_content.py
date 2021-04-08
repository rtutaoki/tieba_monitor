# 帖子每层实体
class TieContent:
    def __init__(self, user_id="", user_name="", user_content=""):
        self.user_id = user_id
        self.user_name = user_name
        self.user_content = user_content

    def TC_to_dict(self):
        """
        将帖子每层实体装换成字典类型
        :return:
        """
        tc_dict = {'user_id': self.user_id, 'user_name': self.user_name, 'user_content': self.user_content}
        return tc_dict

    def dict_to_TC(self, tc_dict):
        """
        将字典类型装换成帖子每层实体
        :param tc_dict: dict
        :return:
        """
        self.user_id = tc_dict['user_id']
        self.user_name = tc_dict['user_name']
        self.user_content = tc_dict['user_content']