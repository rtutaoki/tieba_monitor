from flask import Flask, request, render_template
import json
from reptile.tieba_reptile import TiebaReptile
from indexes.indexes import Indexes
from banned_word import banned_word_helper

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("main.html")


@app.route('/monitor', methods=['GET'])
def monitor():
    # tieba = TiebaReptile()  # 默认name=“武汉理工大学”
    # tieba.run(10)

    word_list = banned_word_helper.get_word_list()

    idx = Indexes()
    idx.add_all_doc()
    result_list = idx.query_list(word_list)

    return json.dumps(result_list)


@app.route('/add_word', methods=['POST'])
def add_word():
    s = request.form.get('word')
    banned_word_helper.add_word(s)
    return json.dumps("添加成功！")


@app.route('/search/<word>', methods=['GET'])
def search(word):
    print(word)
    idx = Indexes()
    result_list = idx.query(word, set())

    return json.dumps(result_list)


if __name__ == '__main__':
    app.run()
