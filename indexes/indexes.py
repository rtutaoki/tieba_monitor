from jieba.analyse import ChineseAnalyzer
from whoosh.fields import Schema, TEXT, ID
from tiezi.tiezi_content import str_to_tc
import os
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
import json


class Indexes:
    def __init__(self):
        self.file_index = None
        self.schema = Schema(user_id=ID(stored=True),
                             user_name=ID(stored=True),
                             user_content=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                             tie_id=ID(stored=True))
        # 直接将file_index初始化
        self.open_index()

    def get_doc(self, file_path):
        """
        从文件中读取到所有爬取到的文件
        :return: list[TieContent]
        """
        doc_list = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                doc_list.append(str_to_tc(line[:-1]))
        return doc_list

    def save_schema(self):
        """
        将索引保存到本地
        :return:
        """
        index_dir = "indexdir"
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
        ix = create_in(index_dir, self.schema)
        self.file_index = ix

    def open_index(self):
        """
        打开已经被创建的索引
        :return:
        """
        if not os.path.exists("indexdir"):
            self.save_schema()
        else:
            self.file_index = open_dir("indexdir")

    def writer(self, doc_list):
        """
        用于写入文档
        :return:
        """
        writer = self.file_index.writer()
        for doc in doc_list:
            writer.add_document(user_id=doc.user_id, user_name=doc.user_name, user_content=doc.user_content,
                                tie_id=doc.tie_id)
        writer.commit()

    def add_doc(self):
        """
        将文档加入索引中
        :return:
        """
        parent_path = os.path.dirname(os.getcwd())
        path = os.path.join(parent_path, "爬取的文件")
        file_list = os.listdir(path)
        nums = len(file_list)
        index = 0
        for file_name in file_list:
            doc_list = self.get_doc(os.path.join(path, file_name))
            self.writer(doc_list)
            index += 1
            print("索引已添加文档数" + str(index) + "/" + str(nums))

    def query(self, qus):
        with self.file_index.searcher() as s:
            parser = QueryParser("user_content", self.file_index.schema)
            my_query = parser.parse(qus)
            results = s.search(my_query)
            print('一共发现%d份文档。' % len(results))
            for i in range(min(10, len(results))):
                print(json.dumps(results[i].fields(), ensure_ascii=False))

    def build_index(self):
        """
        用于重新创建索引并导入文件
        :return:
        """
        self.save_schema()
        self.add_doc()


if __name__ == '__main__':
    pass
    idx = Indexes()
    # idx.build_index()
    idx.query("广告")

