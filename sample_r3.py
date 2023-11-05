#coding:utf-8

from flask import Flask, render_template, redirect, url_for, send_from_directory, request,flash
import secrets , os

#model追加package
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import time

# LLM追加package
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

# assert transformers.__version__ >= "4.34.1


app = Flask(__name__)

# 画像を一時的の保存
UPLOAD_FOLDER = './uploads'
#画像の拡張子指定
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif','jpeg'}
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

    # Azureサブスクリプションキーとエンドポイントを設定
    subscription_key = "subscription_key"
    endpoint = "endpoint"

    computervision_client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(subscription_key)
    )

    # Read APIに渡すローカルファイルを開く
    local_image_path = UPLOAD_FOLDER+"/"+str(filename)
    with open(local_image_path, "rb") as image_stream:
        recognize_handwriting_results = computervision_client.read_in_stream( image_stream, raw=True )

    # 結果の取得
    operation_location_remote = recognize_handwriting_results.headers["Operation-Location"]
    operation_id = operation_location_remote.split("/")[-1]

    # 結果が得られるまで待つ
    while True:
        get_handw_text_results = computervision_client.get_read_result(operation_id)
        if get_handw_text_results.status not in ["notStarted", "running"]:
            break
        time.sleep(1)

    prompt = """USER: 以下を正しい文章にして要約して \n"""

    # 成功した場合、結果を出力する
    if get_handw_text_results.status == OperationStatusCodes.succeeded:
        # 結果をファイルに書き出す
        with open("result_text.txt", "w") as file:
            for text_result in get_handw_text_results.analyze_result.read_results:
                for line in text_result.lines:
                    # ファイルにテキスト内容を書き込む
                    file.write(line.text + "\n")
                    prompt += line.text + "\n"

    prompt += "ASSISTANT: "


    print("結果を 'result_text.txt' に書き込みました。")


    #ここにChatGPTの処理で文章を出力する予定です

    model = AutoModelForCausalLM.from_pretrained("./calm2-7b-chat", device_map="auto", torch_dtype="auto")
    tokenizer = AutoTokenizer.from_pretrained("./calm2-7b-chat")
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)


    token_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    output_ids = model.generate(
        input_ids=token_ids.to(model.device),
        max_new_tokens=300,
        do_sample=True,
        temperature=0.8,
        streamer=streamer,
    )

    #結果の出力
    return render_template('result.html', resut_text = output_ids) 





if __name__ == '__main__':
    app.debug = True
    app.run()

#デバッグモードTrueにすると変更が即反映される
#ファイルのエンコードはUTF-8で保存すること
#下記URLをブラウザに打ち込むとページが開く
# http://127.0.0.1:5000/

