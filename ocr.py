from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import time

# Azureサブスクリプションキーとエンドポイントを設定
subscription_key = "b81f187d2a994b099477031763150c69"
endpoint = "https://dev-vision-api-001.cognitiveservices.azure.com/"

# 認証情報とクライアントの作成
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Read APIに渡すローカルファイルを開く
local_image_path = '/Users/ryota_k/hackathon_11/202311_hackathon/23076443_1000_0.jpeg'
with open(local_image_path, "rb") as image_stream:
    recognize_handwriting_results = computervision_client.read_in_stream(image_stream, raw=True)

# 結果の取得
operation_location_remote = recognize_handwriting_results.headers["Operation-Location"]
operation_id = operation_location_remote.split("/")[-1]

# 結果が得られるまで待つ
while True:
    get_handw_text_results = computervision_client.get_read_result(operation_id)
    if get_handw_text_results.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# 成功した場合、結果を出力する
if get_handw_text_results.status == OperationStatusCodes.succeeded:
    # 結果をファイルに書き出す
    with open('result_text.txt', 'w') as file:
        for text_result in get_handw_text_results.analyze_result.read_results:
            for line in text_result.lines:
                # ファイルにテキスト内容を書き込む
                file.write(line.text + '\n')
    print("結果を 'result_text.txt' に書き込みました。")



