#coding:utf-8

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hallo World!"

if __name__ == '__main__':
    app.debug = True
    app.run()

#デバッグモードTrueにすると変更が即反映される
#ファイルのエンコードはUTF-8で保存すること
#下記URLをブラウザに打ち込むとページが開く
# http://127.0.0.1:5000/

