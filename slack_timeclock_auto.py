from slack import WebClient
from slackeventsapi import SlackEventAdapter
from jobcon_access import stamp # jobcon_accessモジュールからstamp関数をインポート
import threading
import json

# credentials.jsonファイルから必要な認証情報を読み込む
f = open('credentials.json')
data = json.load(f)
SLACK_SIGNING_SECRET = data["SLACK_SIGNING_SECRET"]
SLACK_CHANNEL_ID = data["SLACK_CHANNEL_ID"]
SLACK_USER_ID = data["SLACK_USER_ID"]
f.close()

# Slackイベントを受信するクラス
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/")

# メッセージイベントを処理する関数
def jobcon_access_thread(event):
    ts_and_text = {}
    # イベントが特定の条件を満たす場合に処理を実行
    if event['user'] and event['user'] == SLACK_USER_ID and event['channel'] and event['channel'] == SLACK_CHANNEL_ID:
        ts_and_text['ts'] = event['ts'] # イベントのタイムスタンプ
        ts_and_text['text'] = event['text'] # イベントのテキストメッセージ
        stamp(ts_and_text) # jobcon_accessモジュールのstamp関数を呼び出して処理を実行

# Slackワークスペースで発生したメッセージイベントを受信し、ハンドラーに渡す
@slack_events_adapter.on("message")
def handle_message_channels_event(data):
    event = data['event']  #受信したイベントを取得
    # メッセージイベントを処理するスレッドを作成
    thread = threading.Thread(target=jobcon_access_thread, kwargs={"event" : event})
    thread.start()
    print("I'm finished")

# Slackイベントアダプターは指定されたポートでリスンし、Slackからのイベントを待ち受ける
slack_events_adapter.start(port=3000)


