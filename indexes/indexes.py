from jieba.analyse import ChineseAnalyzer
from whoosh.fields import Schema, TEXT, ID
from tiezi.floor_content import str_to_fc
import os
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh import qparser
import json


class Indexes:
    def __init__(self):
        self.file_index = None
        self.schema = Schema(floor_id=ID(stored=True),
                             user_id=ID(stored=True),
                             user_name=ID(stored=True),
                             floor_content=TEXT(stored=True, analyzer=ChineseAnalyzer()),
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
                doc_list.append(str_to_fc(line[:-1]))
        return doc_list

    def save_schema(self, index_dir):
        """
        将索引保存到本地
        :param index_dir: str
        :return:
        """
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
        ix = create_in("indexdir", self.schema)
        self.file_index = ix

    def open_index(self):
        """
        打开已经被创建的索引
        :return:
        """
        if os.getcwd().split('\\')[-1] == "indexes":
            index_dir = os.path.join(os.getcwd(), "indexdir")
        else:
            index_dir = os.path.join(os.getcwd(), r"indexes\indexdir")
        if not os.path.exists(index_dir):
            self.save_schema(index_dir)
        else:
            self.file_index = open_dir(index_dir)

    def writer(self, doc_list):
        """
        用于向索引中写入文档
        :return:
        """
        my_writer = self.file_index.writer()
        for doc in doc_list:
            if not self.is_exist(doc.floor_id):
                my_writer.add_document(floor_id=doc.floor_id, user_id=doc.user_id, user_name=doc.user_name,
                                       floor_content=doc.floor_content, tie_id=doc.tie_id)
        my_writer.commit()

    def add_doc(self, file_path):
        """
        将单个帖子文件加入索引,file_path为绝对路径
        :param file_path: str
        :return:
        """
        doc_list = self.get_doc(file_path)
        self.writer(doc_list)

    def add_all_doc(self):
        """
        将所有帖子文档加入索引中
        :return:
        """
        if os.getcwd().split('\\')[-1] == "indexes":
            file_path = os.path.join(os.path.dirname(os.getcwd()), "爬取的文件")
        else:
            file_path = os.path.join(os.getcwd(), "爬取的文件")
        file_list = os.listdir(file_path)
        nums = len(file_list)
        index = 0
        for file_name in file_list:
            self.add_doc(os.path.join(file_path, file_name))
            index += 1
            print("索引已添加文档数" + str(index) + "/" + str(nums))

    def query(self, qus, used):
        """
        用于搜索含有该内容的文档
        :param used: set()
        :param qus: str
        :return:
        """
        result_list = []
        with self.file_index.searcher() as s:
            parser = qparser.QueryParser("floor_content", schema=self.file_index.schema)
            my_query = parser.parse(qus)
            results = s.search(my_query, limit=5)
            results_num = len(results)
            print('一共发现%d份文档。' % results_num)
            page_num = results_num // 10 + 1
            for i in range(1, page_num + 1):
                results = s.search_page(my_query, i)
                for j in results:
                    if j["floor_id"] not in used:
                        result_list.append(json.dumps(j.fields(), ensure_ascii=False))
                        used.add(j["floor_id"])
        return result_list

    def query_list(self, qus_list):
        """
        按照列表给出所有违规内容
        :param qus_list: str
        :return:
        """
        used = set()
        result_list = []
        if not qus_list:
            return None
        for que in qus_list:
            result_list.extend(self.query(que, used))
        return result_list

    def is_exist(self, floor_id):
        """
        用于查询索引中是否已经存在该文档
        :param floor_id:
        :return:
        """
        with self.file_index.searcher() as s:
            parser = QueryParser("floor_id", self.file_index.schema)
            my_query = parser.parse(floor_id)
            results = s.search(my_query, limit=1)
            results_num = len(results)
        if results_num > 0:
            return True
        else:
            return False

    def build_index(self):
        """
        用于重新创建索引并导入文件
        :return:
        """
        self.save_schema()
        self.add_all_doc()


if __name__ == '__main__':
    pass
    idx = Indexes()
    idx.add_all_doc()
    # que_list = []
    # que_list.append("大学")
    # result_list = idx.query_list(que_list)
    # result_list = idx.query("你妈", set())
    # print(result_list)
    # print(len(result_list))
