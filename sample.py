#coding:utf-8

from flask import Flask, render_template, redirect, url_for, send_from_directory, request,flash

import secrets , os


app = Flask(__name__)

# 画像を一時的の保存
UPLOAD_FOLDER = './uploads'
#画像の拡張子指定
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif'}
#アップロードの設定/指定
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#ファイルアップロードのためのセキュア設定（トークン）
secret = secrets.token_urlsafe(32)
#ファイルアップロードのためのセキュア設定（設定）
app.secret_key = secret


#拡張子確認関数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    #ファイルアップロード処理
    if request.method == 'POST':

        #入力値ファイルが空かの確認
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)


        file = request.files['file']

        #ファイルが空かの確認②
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)

        #ファイル形式とファイルがある場合 = OK処理
        if file and allowed_file(file.filename):

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            return redirect(url_for('uploaded_file', filename=file.filename))

    return render_template("index.html")




@app.route('/uploads/<filename>/result')
def uploaded_file(filename):

    send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    #ここに画像認識の処理を加える予定です


    #ここにChatGPTの処理で文章を出力する予定です



    #結果の出力
    return render_template('result.html') 





if __name__ == '__main__':
    app.debug = True
    app.run()

#デバッグモードTrueにすると変更が即反映される
#ファイルのエンコードはUTF-8で保存すること
#下記URLをブラウザに打ち込むとページが開く
# http://127.0.0.1:5000/

