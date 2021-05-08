import os


def add_word(s):
    """
    往禁用词列表中添加词语
    :param s: str
    :return:
    """
    word_path = os.getcwd()
    word_list = get_word_list()
    if s in word_list:
        return
    if word_path.split('\\')[-1] == "banned_word":
        word_path = os.path.join(word_path, "banned_word.txt")
    else:
        word_path = os.path.join(word_path, r"banned_word\banned_word.txt")
    with open(word_path, mode='a', encoding='utf-8') as f:
        f.write(s+'\n')


def get_word_list():
    """
    从文件中获取禁用词列表
    :return: str
    """
    word_path = os.getcwd()
    local = word_path.split('\\')[-1]
    if local == "banned_word":
        word_path = os.path.join(word_path, "banned_word.txt")
    elif local == "tieba_monitor":
        word_path = os.path.join(word_path, r"banned_word\banned_word.txt")
    else:
        print("路径有问题")
        return ""
    if not os.path.exists(word_path):
        return ""
    word_list = []
    with open(word_path, mode='r', encoding='utf-8') as f:
        for word in f.readlines():
            word_list.append(word.replace("\n", ""))
    return word_list


if __name__ == '__main__':
    add_word("学弟")